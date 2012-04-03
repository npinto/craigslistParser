## CraigslistParser

A utility that occasionally polls a given craigslist URL and generates emails when new posts surface. I've forked this from "craigsuck" (and renamed it) to reintroduce email functionality. I've expanded it to take a list of keywords where at least one of the keywords needs to be present in a post title for an email to be generated.

# Usage

Modify conf.py to suit your particular query. Then, just run

    ./craigslistParser



From the original repo:


Periodically checks a Craigslist RSS feed for listings and pipes them to output.  See the legacy `craigslist-mailer` tags (`1.0.x`) for e-mail functionality.

# Installation

* `craigsuck` depends on `BeautifulSoup`. See [this page](http://stackoverflow.com/questions/452283/how-can-i-install-the-beautiful-soup-module-on-the-mac) for Mac instructions.
