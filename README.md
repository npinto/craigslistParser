## CraigslistParser

A utility that occasionally polls a given craigslist URL and generates emails when new posts surface. I've forked this from "craigsuck" (and renamed it) to reintroduce email functionality. I've expanded it to take a list of keywords where at least one of the keywords needs to be present in a post title for an email to be generated.



From the original repo:


Periodically checks a Craigslist RSS feed for listings and pipes them to output.  See the legacy `craigslist-mailer` tags (`1.0.x`) for e-mail functionality.

# Installation

* `craigsuck` depends on `BeautifulSoup`. See [this page](http://stackoverflow.com/questions/452283/how-can-i-install-the-beautiful-soup-module-on-the-mac) for Mac instructions.

# Usage

Navigate to the Craigslist page you'd like to keep an eye on and copy the URL.  Examples:

* http://newyork.craigslist.org/rnr/
* http://sfbay.craigslist.org/search/apa/sby?query=&srchType=A&minAsk=&maxAsk=&bedrooms=&addTwo=purrr

Give a list of URLS to `craigslistParser`, for instance:

    ./craigslistParser "http://newyork.craigslist.org/brk/aap/"

To change the output format, you can specify it using the `--format` option. Format is given in Python templates style, with `link`, `title`, or `date` as possible parameters.

    ./craigsuck --format "${date} - ${title}" "http://newyork.craigslist.org/brk/aap/"

See `--help` for details.