#!/usr/bin/env python

from urllib import urlopen
import json
from traceback import print_tb
import re
from time import sleep
from random import random

def access_page(url):
    content = None
    try:
        page = urlopen(url)
        content = page.read().decode('utf-8')
    except:
        print('Unable to open or decode content: %s' % url)
        print_tb()
    return content


def index_subjects(year='DEFAULT', term='DEFAULT'):
    """
    TO BE IMPLEMENTED LATER
    """
    return
    
    """
    Args:
        year (int): eg. `2017`
        semester (str): `summer`, `fall`, `winter`, or `spring`
    """
    main_index_url = 'https://courses.illinois.edu/schedule/{year}/{term}' \
                        .format(year=year, term=term)
    main_index_content = access_page(main_index_url)
    if main_index_content is None:
        print('Main index not accessible. Exiting.')
        exit()
    start_idx = main_index_content.find('<tbody>')
    end_idx = main_index_content.find('</tbody>')
    table_content = main_index_content[start_idx:end_idx].split('<tr>')
    for row in table_content:
        # get abbrs
        subject_abbr = re.findall(r'<td>[\s\S]*</td>[\s\S]*<td>', row)
        if len(subject_abbr) == 0:
            continue
        subject_abbr = subject_abbr[0]
        edge = '<td>'
        subject_abbr = subject_abbr[len(edge):].strip()
        subject_abbr = subject_abbr.split()[0]

        # get subject names
        subject = re.findall(r'</td>[\s\S]*<td>[\s\S]*</td>', row)
        if len(subject) == 0:
            continue
        subject = subject[0]
        edge1, edge2 = '</td>', '<td>'
        subject = subject[len(edge1):].strip()[len(edge1):]
        subject = subject.split()


        print '==='
        print subject_abbr
        print subject

def index_courses(year, term, subj_code):
    pass


def parse_page(subject, code, year='DEFAULT', term='DEFAULT'):
    url_format = 'https://courses.illinois.edu/schedule/' + \
                 '{year}/{term}/{subject}/{code}'
    url = url_format.format(year=year, term=term, subject=subject, code=code)
    content = access_page(url)
    print('Looking at {subject} {code}'.format(subject=subject, code=code))
    if content is None:
        print('  - Page not found.')
        return

    # Title
    title = re.findall(r'<span class="app-label app-text-engage">.*</span>', content)
    try:
        prefix, suffix = '<span class="app-label app-text-engage">', '</span>'
        title = title[0][len(prefix):-len(suffix)].strip()
        print('  - Title: %s' % title)
    except:
        print('  - Title not found')

    # Credit
    credit = re.findall(r'<p><b>Credit:</b>.*</p>', content)
    try:
        prefix, suffix = '<p><b>Credit:</b>', '</p>'
        credit = credit[0][len(prefix):-len(suffix)].strip()[:-1]
        print('  - Credit: %s' % credit)
    except:
        print('  - Credit not found')

    # Description
    try:
        desc = re.findall(r'<p><b>Credit:</b>[\s\S]*<a href="#toggleinfo"',
                          content)[0]
        prefix = '</p>'
        prefix_len = desc.find('</p>')
        suffix_len = desc.find('</div>')
        desc = desc[prefix_len + len(prefix):suffix_len].strip()
        desc = re.sub(r'[\s][\s]*[\s]', r'\n', desc)
        # print(desc)
        print('  - Description: %s...' % desc[:30])
    except:
        print('  - Description not found')
        print_tb()

    # GenEd
    gened_str = 'This course satisfies the General Education Criteria'
    gened = re.findall(gened_str, desc)
    if len(gened) == 0:
        geneds = None
        print('  - Not a GenEd course.')
    else:
        try:
            gened = gened[0]
            desc_split = desc.split('<p>')
            if gened_str in desc_split[-1]:
                gened = desc_split.pop(-1)
            else:
                for i in range(len(desc_split)):
                    if gened_desc in desc_split[i]:
                        gened = desc_split.pop(i)
            desc = '<p>'.join(desc_split)
            geneds = []
            geneds_raw = re.findall(r'UIUC.*course', gened)
            for ge in geneds_raw:
                prefix, suffix = 'UIUC', '&#160;course'
                ge = ge[len(prefix):-len(suffix)]
                if ge[0] == ':':
                    ge = ge[1:]
                ge = ge.strip()
                geneds.append(ge)
            print('  - GenEds: %s' % geneds)
        except:
            print('  - GenEds parsing failed.')

    # Out
    return {
        'subject': subject,
        'code': code,
        'title': title,
        'credit': credit,
        'desc': desc,
        'geneds': geneds,
        'url': url
    }

def random_sleep(mean=0.3, tolerance=0.15):
    sleep_time = mean - tolerance + 2 * tolerance * random()
    sleep(sleep_time)

if __name__ == '__main__':
#    print(parse_page('CS', '225'))
#    print(parse_page('CS', '241'))
#    print(parse_page('ANTH', '101'))
    pool = [('CHEM', '102'),('CHEM', '103'),('CHEM', '104'),('CS', '101'),('CS', '125'),('CS', '126'),('CS', '173'),('CS', '225'),('CS', '233'),('CS', '241'),('CS', '357'),('CS', '374'),('CS', '412'),('CS', '418'),('CS', '421'),('CS', '498'),('ECON', '103'),('GE', '101'),('MATH', '220'),('MATH', '231'),('MATH', '241'),('MATH', '415'),('MATH', '448'),('MATH', '461'),('PHYS', '211'),('PHYS', '212'),('PHYS', '213'),('STAT', '400'),('TAM', '211'),('TAM', '212'),('TAM', '251')]

    for subj, code in pool:
        random_sleep()
        try:
            res = parse_page(subj, code)
        except:
            print('Error pulling %s %s' % (subj, code))
            continue
        fh = open('out/%s_%s.json' % (subj, code), 'w')
        fh.write(json.dumps(res))
        fh.close()
    print('Done.')
