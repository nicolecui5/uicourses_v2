#############################################################################
#                                                                           #
#  Author:           Sibo Wang, Fangxing Liu                                #
#  Created:          February 17, 2017                                      #
#  Last modified:    February 17, 2017                                      #
#  Derived from:     csv_to_json.py                                         #
#  Python version:   2.7.0                                                  #
#                                                                           #
#############################################################################


import enum
from urllib2 import urlopen
import json


BASE_URL = 'http://www.ratemyprofessors.com/'
SEARCH_URL = 'http://www.ratemyprofessors.com/search.jsp?queryoption=HEADER&queryBy=teacherName&schoolName=university+of+illinois&schoolID=&query=%s'
DECODING = 'utf-8'


class Status(enum.Enum):
    FRESH = -1
    SUCCESS = 0
    NOT_FOUND = 1
    GUESSED_FIRST = 2
    OPEN_ERROR = 3
    PARSE_ERROR = 4


class ProfParser:

    url = ''
    first_name = ''
    last_name = ''
    overall_quality = -1
    level_of_difficulty = -1
    keywords = None
    tags = []
    status = Status.FRESH

    def __init__(self, first_name, last_name, keywords=None):
        self.first_name = first_name
        self.last_name = last_name
        self.keywords = keywords

    def gen_search_url(self):
        name_str = '%s+%s' % (self.first_name, self.last_name)
        return SEARCH_URL % name_str

    def get_prof_page_url(self):
        # Open search page
        search_url = self.gen_search_url()
        search_res = self.read_from_url(search_url)
        if search_res is None:
            self.status = Status.OPEN_ERROR
            return

        # Filter result listing
        search_res = self.trim_middle(search_res, '<ul class="listings">', '</ul>')
        if search_res is None:
            self.status = Status.NOT_FOUND
            return
        # Split listing entries
        listings = search_res.split('<li ')
        # no result found
        if len(listings) == 1:
            self.status = Status.NOT_FOUND
        # results found
        else:
            if self.keywords is None: subjects = ['']
            else: subjects = self.keywords
            found = False
            first = True
            for entry_content in listings:
                if first:
                    first = False
                    continue
                subject_match = False
                for subj in subjects:
                    if subj.lower() in entry_content.lower():
                        subject_match = True
                if not subject_match:
                    continue
                if not found:
                    url_res = self.filter_url_from_listing(entry_content)
                    if url_res is None:
                        self.status = Status.PARSE_ERROR
                    else:
                        self.url = url_res
                        self.status = Status.SUCCESS
                        return
                else:
                    self.status = Status.GUESSED_FIRST
            self.status = Status.NOT_FOUND

    def parse_data(self):
        # Open page
        prof_page = self.read_from_url(self.url)
        if prof_page is None:
            self.status = Status.OPEN_ERROR
            return
        else:
            # Overall quality and difficulty
            left_breakdown = self.trim_middle(prof_page,
                                              '<div class="left-breakdown">',
                                              '<div class="right-breakdown">')
            quality_field = self.trim_middle(left_breakdown,
                                             'Overall Quality',
                                             '/div>')
            difficulty_field = self.trim_middle(left_breakdown,
                                                'Level of Difficulty',
                                                '/div>')
            quality_field = self.trim_middle(quality_field, '>', '<')
            difficulty_field = self.trim_middle(difficulty_field, '>', '<')
            try:
                self.overall_quality = float(quality_field.strip())
            except:
                self.status = Status.PARSE_ERROR
            try:
                self.level_of_difficulty = float(difficulty_field.strip())
            except:
                self.status = Status.PARSE_ERROR

            # Tags
            right_breakdown = self.trim_middle(prof_page,
                                               '<div class="left-breakdown">',
                                               '<a href="#"')
            tag_listings = right_breakdown.split('<span class="tag-box-choosetags">')[1:]
            for t in tag_listings:
                label = self.trim_middle(t, ' ', '<b>')
                if label is not None:
                    self.tags.append(label.strip())

    def filter_url_from_listing(self, entry):
        # Filter url suffix
        trimmed = self.trim_middle(entry, 'href="', '"')
        if trimmed is None:
            return None

        # Get full url
        return BASE_URL[:-1] + trimmed

    def make_json(self):
        d = {'first_name': self.first_name,
             'last_name': self.last_name,
             'url': self.url,
             'quality': self.overall_quality,
             'difficulty': self.level_of_difficulty,
             'tags': self.tags}
        return json.dumps(d)

    @staticmethod
    def read_from_url(url):
        # noinspection PyBroadException
        try:
            page = urlopen(url)
            content = page.read().decode(DECODING)
            page.close()
            return content
        except:
            return None

    @staticmethod
    def trim_middle(string, start_pattern, end_pattern):
        start_index = string.find(start_pattern)
        if start_index < 0:
            return None
        string = string[start_index + len(start_pattern):]
        end_index = string.find(end_pattern)
        if end_index < 0:
            return None
        return string[:end_index]

if __name__ == '__main__':
    parser = ProfParser('neal', 'dalal', keywords=['astronomy'])
    parser.get_prof_page_url()
    parser.parse_data()
    print(parser.make_json())

