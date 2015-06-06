#!/usr/bin/env python
import yaml
from optparse import OptionParser

import octavo
from octavo.goodreads import GoodReads



CONFIGS = yaml.load(open("conf/octavo.yaml"))

parser = OptionParser()
parser.add_option("-u", "--user", dest="userid",
                  help="id of user to fetch", default=CONFIGS['my_id'])

(options, args) = parser.parse_args()

gr = GoodReads(api_key=CONFIGS['api_key'], htdocs=CONFIGS['htdocs'])
gr.fetch_reviews(options.userid)