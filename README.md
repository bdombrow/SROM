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

## Requirements ##
Python
+ Flask
+ matplotlib
+ flask-wtf
+ psycopg2
+ requests

Apache
+ mod_wsgi

PostgreSQL
