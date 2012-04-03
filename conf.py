#
# SMTP information. Yeah, the password needs to be in plaintext. Keep this close to the chest.
#
SMTP_USER ='myEmailAddy'
SMTP_PASS ='myPasswordThatIMadeSureNotToCommit'
SMTP_SERVER ='smtp.yourhost.com'
SENDER ='stranger@gmail.com'    # the e-mail sender (may not work with all SMTP providers e.g. gmail)

#
# Colon separated recipients
#
RECIPIENTS ='recipient@gmail.com'

#
# The URL you want to parse
#
CRAIGS_URL = "http://sfbay.craigslist.org/search/apa?query=&srchType=A&minAsk=2000&maxAsk=3600&bedrooms=2"


#
# Keywords. At least one needs to be present in the post title for an email to be generated.
#
KEYWORDS = ['soma', 'south of market', 'potrero', 'mission', 'south beach', 'union square', 'hayes', 'alamo', 'western addition', 'noe']
