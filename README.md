# GTH-Barcelona-PenguinBots
Project submission for the `Global Travel Hackathon in Barcelona, by Penguin Bots team`.

**Write one sentence explaining what does your project.**

![Add a screenshot from your project. For example the main website page.](https://raw.githubusercontent.com/Global-Travel-Hackathon/GTH-Location-TeamName/master/screenshots/Global-Travel-Hackathon-image.png)

## :books: Description

Our project is focused on the topic of Community. Our goal was to try to find a way to connect travelers with the local culture of the cities they are visiting. We realised that a very powerful way of connecting people was through music. Therefore, we decided to create a tool that will allow travelers to discover local artists and even get the chance to see them live.

It consists on a Chrome extension that, after logging in with Spotify, whenever you are searching for a flight on Kiwi.com it detects which city you are planning to visit and which dates you plan to be there in order to immediately play you songs from local artists that will perform while you are there. You can even create a playlist with those artists to listen to them later on.

For the back-end, we used Python with Flask, which allows us to retrieve and merge information from three different APIs:
* [Songkick](https://www.songkick.com/developer), in order to get which concerts are taking place during the dates the user plans to be there.
* [MusicBrianz](https://musicbrainz.org/doc/Development/XML_Web_Service/Version_2), to filter the list of artists that are performing, in order to keep only the artists that are originally from that country.
* [Spotify](https://developer.spotify.com/documentation/web-api/), to get the main tracks from each artist and also to be able to control the user's player in order to play the songs.

We connected all this with a front-end consisting of a Google Chrome extension written in Javascript and HTML that we just learned to program throughout the hackathon.

## :hugs: Maintainers

* [Oriol Nadal - oriolnadal](https://github.com/oriolnadal)
* [Elies Delgado - eliesdt](https://github.com/eliesdt)

## :tada: Why is this so awesome?

* Discovering new artists feels great
* Getting to know the local culture is cool
* Chrome Extensions are awesome

## :hammer_and_wrench: Installation

API KEYS for Songkick and Spotify are required.
Then, you just need to run the python main.py file, and install the Chrome Extension (it is possible to load it unpacked without having to publish it to the Google Chrome store)

## :bulb: Devstack
Back-end: Python + Flask
Front-end: Javascript + HTML

## :warning: Licence

>The code in this project is licensed under MIT license. By contributing to this project, you agree that your contributions will be licensed under its MIT license.
