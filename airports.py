#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
from lib.workflow import Workflow3 as Workflow, ICON_WARNING, ICON_INFO, web, MATCH_ATOM, MATCH_SUBSTRING

def main(wf):
    # Imports go here.
    import pycountry
    import unicodedata
    import unicodecsv as csv
    from dotmap import DotMap as Map
    from cStringIO import StringIO
    from workflow.background import run_in_background, is_running

    import re

    # Function to retrieve CSV from an URL and p
    def get_web_data():
        r = web.get('http://ourairports.com/data/airports.csv')
        r.raise_for_status()

        # Read the whole CSV
        csvstring = StringIO(r.text)
        result    = csv.DictReader(csvstring, encoding='utf-8', delimiter=',', quotechar='"')

        # Skip the header row
        headers = result.fieldnames

        airports = []

        # Go over each row and cache the airport data.
        for index, row in enumerate(result, start=1):
            iata_code    = row['iata_code'].upper().strip()
            airport_type = row['type'].strip()
            airport_id   = int(row['id'])

            # We're only interested in airports with IATA code.
            if not airport_id: continue
            if len(iata_code) == 0 or iata_code == '-': continue
            if airport_type != 'large_airport' and airport_type != 'small_airport' and airport_type != 'medium_airport': continue

            airport_type     = airport_type.split("_")[0]
            airport_name     = row['name'].strip()
            airport_coords   = { 'lat': float(row['latitude_deg']), 'lon': float(row['longitude_deg']) }
            airport_city     = row['municipality'].strip()
            airport_url      = row['home_link'].strip()
            airport_wiki     = row['wikipedia_link'].strip()
            airport_icao     = row['ident'].upper().strip()

            # Add a '.' after single uppercase letters
            airport_name = re.sub( r"\b([A-Z])(?![\w\-\.])", r"\1.", airport_name)

            country_iso_code = row['iso_country'].strip().upper()[:2]
            try :
                country = pycountry.countries.get(alpha_2=country_iso_code)
                country = country.name
            except (KeyError, AttributeError) as err:
                wf.logger.error("Error: {0} (Country: {1})".format(err, country_iso_code))
                country = country_iso_code

            airport_country = country

            # Build our airport object.
            airports.append( Map( id = airport_id, iata_code = iata_code, icao_code = airport_icao,
                type = airport_type, name = airport_name, coords = airport_coords,
                country = airport_country, city = airport_city, url = airport_url, wiki = airport_wiki ) )

        # Sort the list by airport_type. Snce it's only 'Large', 'Medium' and 'Small', they should be sorted correctly.
        airports = sorted(airports, key=lambda k: (k.type, k.iata_code))
        return airports

    # Build a search key given an airport object.
    def key_for_airports(airport):
        searchkey = u'{},{},{},{},{}'.format(airport.iata_code, airport.name, airport.icao_code, airport.country, airport.city)
        wf.logger.debug('Search key: ' + searchkey)
        return searchkey

    # ==========================================================================
    # ================================= MAIN ===================================
    # ==========================================================================

    wf.magic_prefix = 'wf:'

    # Get args from Workflow, already in normalized Unicode
    if not wf.args or not len(wf.args) >= 1 : return 1
    airportquery = u' '.join(wf.args).strip().encode('utf-8')

    # If no query, return.
    if not airportquery: return 1

    # If '--update' is passed as parameter, update cached data.
    if airportquery == '--update':
        wf.logger.info('Updating airport data...')

        airportdata = get_web_data()
        wf.cache_data('airports', airportdata)

        wf.logger.info('Updated airport data in cache')
        return 0

    wf.logger.info('Searching airports for \'%s\'...' % airportquery)

    # Update workflow if a new version is available.
    if wf.update_available == True:
        wf.add_item('New version available', 'Press enter to install the update.',
            autocomplete='workflow:update',
            icon=ICON_INFO)

    # Is cache over 10 days old or non-existent?
    if not wf.cached_data_fresh('airports', max_age=60*60*24*10):
        wf.logger.info('Airport data is stale, updating in the background...')
        run_in_background('update', ['/usr/bin/env python', wf.workflowfile('airports.py'), '--update'])

    if is_running('update'):
        wf.logger.debug('Waiting for update to finish.')
        # Rerun every 1/2 second until the `update` job is complete
        wf.rerun = 0.5
        # Add a notification if the script is running
        wf.add_item('Updating airport data...', valid=False, icon=ICON_INFO)

    # Get cached airports object, max_age=0 will load any cached data regardless of age
    all_airports = wf.cached_data('airports', None, max_age=0)

    if not all_airports or len(all_airports) == 0:
        wf.send_feedback()
        return

    # Find all airports that match the filter query.
    filtered_airports = wf.filter(airportquery, all_airports, key_for_airports, min_score=70, match_on=MATCH_ATOM | MATCH_SUBSTRING, include_score=True)

    if not filtered_airports or len(filtered_airports) == 0:
        wf.add_item('No airport found that matches your query of \'%s\'!' % airportquery, icon=ICON_WARNING)
        wf.send_feedback()
        return

    # Build response
    for airport, score, wffilter in filtered_airports:

        title    = '(%s) %s' % (airport.iata_code, airport.name)
        subtitle = airport.icao_code + ' ' + ('(%s, %s)' % (airport.city, airport.country)) if airport.city != '' else airport.country

        item = wf.add_item( title, subtitle,
            autocomplete=airport.iata_code,
            icon='icon.png',
            valid=True,
            copytext=airport.name,
            largetext='(%s) %s' % (airport.iata_code, airport.name),
            uid='alfred-airport-codes-%s' % airport.id
        )

        item.setvar('WF_URL',  '')

        # CMD modifier for Maps.app
        mod = item.add_modifier('cmd', 'Show the airport in Maps.app')
        geo_url = 'http://maps.apple.com/?q=%f,%f' % ( airport.coords['lat'], airport.coords['lon'] );
        mod.setvar('WF_URL', geo_url )
        item.arg = geo_url

        # CTRL modifier for Wikipedia page.
        if airport.wiki :
            mod = item.add_modifier('ctrl', 'Open the airports Wikipedia page (%s)' % airport.wiki)
            mod.setvar('WF_URL', airport.wiki)

            # Overwrite main action.
            item.arg = airport.wiki
        else :
            mod = item.add_modifier('ctrl', 'The %s airport has no Wikipedia entry.' % airport.iata_code )

        # ALT modifier for URL.
        if airport.url :
            mod = item.add_modifier('alt', 'Open the airports website (%s)' % airport.url)
            mod.setvar('WF_URL', airport.url)

            # Overwrite main action.
            item.arg = airport.url
        else :
            mod = item.add_modifier('alt', 'The %s airport has no website.' % airport.iata_code )

    # Send output to Alfred.
    wf.send_feedback()


if __name__ == '__main__':
    # Create a global `Workflow` object
    wf = Workflow(libraries=['./lib'], update_settings={
        'github_slug': 'otherguy/alfred-airports-workflow',
        'frequency': 1
    })

    # Call your entry function via `Workflow.run()` to enable its helper
    # functions, like exception catching, ARGV normalization, magic
    # arguments etc.
    sys.exit(wf.run(main))
