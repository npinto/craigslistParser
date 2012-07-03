#
# SMTP information.
#
SENDER ='craigslistupdate@gmail.com'

#
# Colon separated recipients
#
RECIPIENTS = '4012585329@txt.att.net;nicolas.pinto+craigslist@gmail.com'

#
# The URL you want to parse
#
CRAIGS_URL = 'http://sfbay.craigslist.org/search/hhh?query=palo+alto+-east&srchType=A&minAsk=1600&maxAsk=3000&bedrooms=2'
#CRAIGS_URL = 'http://sfbay.craigslist.org/search/apa?query=palo+alto&catAbb=hhh&srchType=A&minAsk=1600&maxAsk=3000&bedrooms=2'
 

#
# Keywords. At least one needs to be present in the post title for an
# email to be generated.
#
KEYWORDS = ['palo alto', '2br']
