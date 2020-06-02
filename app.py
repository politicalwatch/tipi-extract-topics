'''
This Python script (re)generate topics
from Google Spreadsheets to MongoDB JSON collection
'''

import sys
import json
import hashlib
import itertools

import pygsheets
import pcre

from settings import settings


class Utils:
    @staticmethod
    def generate_id(*args):
        try:
            return hashlib.sha1(
                    u''.join(args).encode('utf-8')
                    ).hexdigest()
        except Exception:
            return 'ID_ERROR'


class TopicsExtractor:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.topics = list()
        self.data_reference = list()
        self.google_credentials = None

    def __regex_validation(self, tagname, regex):
        try:
            pcre.compile('(?i)'+regex)
        except Exception as e:
            print(tagname, e)

    def __validate(self, tag):
        if tag['shuffle']:
            delimiter = '.*?' if '.*?' in tag['regex'] else '.*'
            perms = itertools.permutations(tag['regex'].split(delimiter))
            for perm in perms:
                self.__regex_validation(tag['tag'], delimiter.join(perm))
        else:
            self.__regex_validation(tag['tag'], tag['regex'])

    def load_data_reference(self):
        with open(settings.DATA_REFERENCE_FILE, 'r') as data_reference_file:
            self.data_reference = json.load(data_reference_file)

    def load_google_credentials(self):
        self.google_credentials = pygsheets.authorize(
                service_account_file=settings.GOOGLE_DRIVE_CREDENTIALS_FILE
                )

    def load_topics(self, method=''):
        for data_reference_item in self.data_reference:
            if self.verbose:
                print("[EXTRACT] {}".format(data_reference_item['name']))
            wks = self.google_credentials.open(data_reference_item['filename']).sheet1
            topic = data_reference_item.copy()
            del topic['filename']
            if method == 'old':
                del topic['shortname']
            topic['_id'] = Utils.generate_id(topic['name'])
            topic['tags'] = []
            data = wks.get_values(grange=pygsheets.GridRange(worksheet=wks, start=None, end=None))
            for row in data[1:]:
                tag = {
                        'regex': row[3],
                        'tag': row[2],
                        'subtopic': row[1],
                        'shuffle': bool(int(row[0]))
                        }
                self.__validate(tag)
                topic['tags'].append(tag)
            self.topics.append(topic)

    def export_topics(self):
        file_out = open('topics.json', 'w')
        file_out.write(json.dumps(self.topics, indent=True, ensure_ascii=False))
        file_out.close()
        print("[EXPORT] Created topics.json file")

    def run(self, args):
        method = args[1] if len(args) > 1 else ''
        self.load_data_reference()
        self.load_google_credentials()
        self.load_topics(method)
        self.export_topics()


if __name__ == '__main__':
    extractor = TopicsExtractor(verbose=True)
    extractor.run(sys.argv)
