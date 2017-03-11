# Sentiment-Analysis-from-Quora
This code is encompassed of 2 programs written in Python. 
<br/>1. scraper.py - Scrapes data off of Quora and stores it into a Cassandra Database. This is done using the Beautiful Soup library recursively run for all related questions as well. 
<br/>2. analysis.py - The Analysis is done using an algorithm called VADER which portrays the net positivity, negativity and neutrality that one could expect in any Quora answer.


VADER Ref-http://comp.social.gatech.edu/papers/icwsm14.vader.hutto.pdf
