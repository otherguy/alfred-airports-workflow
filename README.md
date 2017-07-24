# Airports Workflow ✈️ for [Alfred 3](http://www.alfredapp.com)

[![Latest Version](https://img.shields.io/github/tag/darkwinternight/alfred-airports-workflow.svg?style=flat&label=release)](https://github.com/darkwinternight/alfred-airports-workflow/tags)
[![Software License](https://img.shields.io/badge/license-MIT-brightgreen.svg?style=flat)](LICENSE.md)

A workflow for [Alfred 3](http://www.alfredapp.com) that provides quick access to information about all airports in the world.

![Search Example](resources/screencast-1-resized.gif)

## Installation

Download the latest version of the `airports.alfredworkflow` from the [Releases](https://github.com/darkwinternight/alfred-airports-workflow/releases) page and double click the downloaded file to install it.

The workflow supports automatic updates and will perform daily update checks!

## Usage

When hitting `⏎ Return` on a selected item, the workflow tries to be helpful by opening either the airports website or its Wikpedia page if it has one. If it has neither a website nor an entry in Wikipedia, it opens the Apple Maps.app with the location of the airport.

When holding down a modifier key, the action can be specified:

| Modifier | Action                                           |
|----------|--------------------------------------------------|
| `⌥`      | Open the website of the selected airport.        |
| `ctrl`   | Open the Wikipedia page of the selected airport. |
| `⌘`      | Show the airports location in Maps.app           |

## Developers

If you want to contribute, fork this repository and submit a pull request.

To make the project work locally on your machine, clone the repository, go to the directory and issue the following commands:

    $ pip install --target=. Alfred-Workflow==1.27
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
