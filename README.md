SROM
====

## Background ##
Sucks-Rules-O-Meter redone in Python and Bing

This is my reimplementation of the following web site:

http://srom.zgp.org

The original used Altavista and a perl script. Unfortunately, Altavista is no
longer :(

My version uses Bing and Python becauset Bing gives me 5000 queries a month for
free and I wanted an excuse to play around with matplotlib.

This is an initial working version. It could use alot more polish.

Working version can be found at http://bdombrowski.us/srom

## Files ##

### Database ###
This directory contains the database schema dumped from PostgreSQL.

### Collector ###

#### collector.py ####
This script will collect the search results and put them in the database.
I run this as as cron job on a daily basis.

#### Search.py ####
This contains the search object classes used by the collector script. There are
classes defined for each search engine. Each sub class is configured from the
database.

### WebApp ###
