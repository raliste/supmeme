# supmeme

The codebase of supmeme.com

## What is Supmeme?

Supmeme aggregates news from major Chilean entrepreneurial blogs into just one and easy to read webpage.

## Why Supmeme?

I was getting tired of that "I didn't know that!" feeling everytime someone told me of an interesting local story. 

## How it works

Supmeme has a simple feed crawler that downloads and parses RSS feeds from local sources every hour. The feed entries are then stored in a database that is used by Supmeme's frontend to score and display them.
The simple scoring algorithm is based on the [Hacker News algorithm](http://news.ycombinator.com/item?id=1781013).

## How can you contribute

Clone the repo, commit changes to a branch, push it and ask for a pull request.