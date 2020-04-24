'''
This Python script (re)generate topics
from Google Spreadsheets to MongoDB JSON collection
'''

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
        except:
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

    def load_topics(self):
        for data_reference_item in self.data_reference:
            if self.verbose:
                print("[EXPORT] Processing {}".format(data_reference_item['name']))
            wks = self.google_credentials.open(data_reference_item['filename']).sheet1
            topic = data_reference_item.copy()
            del topic['filename']
            topic['_id'] = Utils.generate_id(topic['name'])
            topic['tags'] = []
            for record in wks.get_all_records(value_render='UNFORMATTED_VALUE'):
                tag = {
                        'regex': record['regex'],
                        'tag': record['tag'],
                        'subtopic': record['subtopic'],
                        'shuffle': bool(record['shuffle']),
                        }
                self.__validate(tag)
                topic['tags'].append(tag)
            self.topics.append(topic)

    def export_topics(self):
        file_out = open('topics.json', 'w')
        file_out.write(json.dumps(self.topics, indent=True, ensure_ascii=True))
        file_out.close()

    def run(self):
        self.load_data_reference()
        self.load_google_credentials()
        self.load_topics()
        self.export_topics()




if __name__ == '__main__':
    extractor = TopicsExtractor(verbose=True)
    extractor.run()
