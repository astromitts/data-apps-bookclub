import os
import requests
import re

from octavo.ingestion import Ingestion


class GoodReads(object):

    @classmethod
    def __init__(self, api_key = None, htdocs = None):
        self.api_key = api_key
        self.htdocs = htdocs
        self.host = "https://www.goodreads.com"
        self.api_urls = {
            'reviews': "/review/list/",
        }

    @classmethod
    def construct_url(self, url_base, request_args):
        url = self.host + url_base
        parts = []
        for k, v in request_args.iteritems():
            parts.append('%s=%s' % (k, v))
        url = url + '&'.join(parts)
        return url

    @classmethod
    def fetch_request_to_disk(self, response, outfile):
        with open(outfile, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return outfile

    @classmethod
    def fetch_reviews(self, userid=None):

        def get_page(page_number):
            standard_url_args = {
                'format': 'xml',
                'v': '2',
                'key': self.api_key,
                'per_page': '200',
            }
            request_args = standard_url_args

            request_args['page'] = page
            url = self.construct_url("%s/%s?" % (
                self.api_urls['reviews'], userid), request_args)
            response = requests.get(url)
            outfile = os.path.join("%s/%s-reviews-%s.xml" % (
                self.htdocs, userid, page))
            self.fetch_request_to_disk(response, outfile)

            search = re.compile(r'<reviews start="(\d+)" end="(\d+)" total="(\d+)">')
            match  = re.search(search, response.text)
            if not match:
                raise Exception("Could not find total for batch request")

            start = int(match.groups()[0])
            end = int(match.groups()[1])
            total = int(match.groups()[2])
            return (start, end, total)

        page = 1
        (start, end, total) = get_page(page)
        while end < total:
            page += 1  
            (start, end, total) = get_page(page)
        return page

