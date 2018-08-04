# f1jobs-updater

**Important: This README is currently a WIP**

This is the update mechanism of [f1jobs.co](https://f1jobs.co), which runs on a separate server. It queries the careers pages of all the Formula 1 teams every `x` minutes, and updates the data at the [client repository](https://github.com/F1Jobs/client).

## Introduction

`getjobs.py` - This is the main script, which is responsible for making web requests, fetching, validating and formatting data, and writing it at the client repository.

`getcookies.js` - This is a helper script which is required only to query the Ferrari careers page, which is run as an argument to [PhantomJS](http://phantomjs.org/) executable. This is because Ferrari decided to use [XHR](https://en.wikipedia.org/wiki/XMLHttpRequest) to fetch their job listings instead of embedding them into the markup, and to those XHRs send a valid response only when valid cookies (which are set by the Ferrari careers page) are included in the request header.

## Todo

* Add descriptive comments to `getjobs.py`.
* Update README with more detailed description.
* Restructure the main directory, and add tests and Dockerfile.
