# Airports Workflow ✈️ for [Alfred 3](http://www.alfredapp.com)

[![Latest Version](https://img.shields.io/github/tag/otherguy/alfred-airports-workflow.svg?style=flat-square&label=release)](https://github.com/otherguy/alfred-airports-workflow/tags)
[![Downloads](https://img.shields.io/github/downloads/otherguy/alfred-airports-workflow/total.svg?style=flat-square)](https://github.com/otherguy/alfred-airports-workflow/releases)
[![Circle CI](https://img.shields.io/circleci/project/github/otherguy/alfred-airports-workflow/master.svg?style=flat-square)](https://circleci.com/gh/otherguy/alfred-airports-workflow/tree/master)
[![Issues](https://img.shields.io/github/issues/otherguy/alfred-airports-workflow.svg?style=flat-square)](https://github.com/otherguy/alfred-airports-workflow/issues)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat-square)](LICENSE.md)
[![Beerpay](https://img.shields.io/beerpay/otherguy/alfred-airports-workflow.svg?style=flat-square)](https://beerpay.io/otherguy/alfred-airports-workflow)

A workflow for [Alfred 3](http://www.alfredapp.com) that provides quick access to information about all airports in the world.

![Search Example](resources/screencast-1-resized.gif)

The latest version can be found here as well:

* https://www.alfredforum.com/topic/10546-airports/
* http://www.packal.org/workflow/airports

## Installation

Download the latest version of the `airports.alfredworkflow` from the [Releases](https://github.com/otherguy/alfred-airports-workflow/releases) page and double click the downloaded file to install it.

The workflow supports automatic updates and will perform daily update checks!

## Usage

When hitting `⏎ Return` on a selected item, the workflow tries to be helpful by opening either the airports website or its Wikipedia page if it has one. If it has neither a website nor an entry in Wikipedia, it opens the Apple Maps.app with the location of the airport.

When holding down a modifier key, the action can be specified:

| Modifier | Action                                           |
|----------|--------------------------------------------------|
| `⌥`      | Open the website of the selected airport.        |
| `ctrl`   | Open the Wikipedia page of the selected airport. |
| `⌘`      | Show the airports location in Maps.app           |

Since version `0.1.4`, you can search for ICAO codes as well!

## Developers

If you want to contribute, fork this repository and submit a pull request.

To make the project work locally on your machine, clone the repository, go to the directory and issue the following commands:

    $ pip install --target=lib -r requirements.txt

Alternatively, if you would rather work with a virtual environment, run these commands:

    $ virtualenv --python=python2.7 .venv
    $ source .venv/bin/activate
    $ pip install -r requirements.txt

To run the script in the terminal, simply do:

    $ python airports.py <search query>

You can install `jq` from [Homebrew](https://brew.sh) and pipe the output of the workflow through this program to get nice formatting and the option to query the JSON.

## Acknowledgements

The following resources were used when creating this workflow:

* The excellent [Alfred-Workflow](https://github.com/deanishe/alfred-workflow) python library by [Dean Jackson](https://github.com/deanishe).
* The airport icon used in the workflow by [Freepik](http://www.freepik.com) and licensed under [CC 3.0 BY](http://creativecommons.org/licenses/by/3.0/).
* All the airport data from [ourairports.com](http://ourairports.com/).

A big ♥️ _thank you_ to all creators!

## Support Me

If this is useful to you in any way, you could buy me a beer 🍺! 

[![Beerpay](https://beerpay.io/otherguy/alfred-airports-workflow/badge.svg?style=beer-square)](https://beerpay.io/otherguy/alfred-airports-workflow)  [![Beerpay](https://beerpay.io/otherguy/alfred-airports-workflow/make-wish.svg?style=flat-square)](https://beerpay.io/otherguy/alfred-airports-workflow?focus=wish)
