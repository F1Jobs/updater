![top-image](https://user-images.githubusercontent.com/29029116/43997345-f10bc6a0-9df5-11e8-9212-c7e0134ce36f.png)

## Introduction

This is the update mechanism of **[f1jobs.co](https://f1jobs.co)**, which runs on a separate server. It queries the careers pages of all the Formula 1 teams every 30 minutes, and updates the data at the [client repository](https://github.com/F1Jobs/client).

## Summary

`getjobs.py` - This is the main script, which is responsible for making web requests, fetching, validating and formatting data, and writing it at the client repository.

`getcookies.js` - This is a helper script which is required only to query the Ferrari careers page, which is run as an argument to [PhantomJS](http://phantomjs.org/). This is because Ferrari decided to use [XHR](https://en.wikipedia.org/wiki/XMLHttpRequest) to fetch their job listings instead of embedding them into the markup, and to those XHRs send a valid response only when valid cookies (which are set by the Ferrari careers page) are included in the request header.
