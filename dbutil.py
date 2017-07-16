#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# UICourses Project
#
# Authored by:   WSB & Suyie
# Drafted:       June 27, 2017
# Last modifed:  June 29, 2017
# Description:   This script provides functions that fetch data from the MySQL
#                database and parse them into python dictionary. This is
#                needed as a part of the db2json api. For security reason this
#                script should run on the server. Otherwise remote database
#                access must be granted for it to work.
#
###############################################################################


import MySQLdb as dblib
from traceback import print_tb
from markdown import markdown
from util import *
from options import *
from credentials import *
from graph_generator import *
from calc_diff import *
import re

###############################################################################
# CONNECTION UTIL
###############################################################################

def connect():
    try:
        log('I', 'db', 'Establishing connection...')
        db = dblib.connect(host='localhost',
                           user=DB['username'],
                           passwd=DB['password'],
                           db=DB['database'],
                           use_unicode=1,
                           charset='utf8')
        return db
    except:
        log('E', 'db', 'Could not establish connection')
        print_tb()


def disconnect(db):
    db.close()
    log('I', 'db', 'Closed database connection.')


###############################################################################
# LOOK-UP
###############################################################################

def lookup_course_review(db, review_id):
    # perform SQL query
    cur = db.cursor()
    qry = 'SELECT * FROM CourseReview WHERE Id = %s'
    cur.execute(qry, [review_id])

    # process results
    row = cur.fetchone()
    if row is None:
        log('W', 'record', 'CourseReview %d not found. Skipping.' % review_id)
        return None
    res = {}
    for idx, elem in enumerate(row):
        # encode strings (unicode strings due to utf-8)
        # if type(elem) == type(u''):
        #     elem = elem.replace('"', '\\"').replace('\n', '\\n')
        #     elem = elem.encode(encoding='utf-8')
        if TABLE_STRUCT['CourseReview'][idx] in MARKDOWN_FIELDS:
            elem = markdown(elem)
        res[TABLE_STRUCT['CourseReview'][idx]] = elem

    return res


def lookup_prof_review(db, review_id):
    # perform SQL query
    cur = db.cursor()
    qry = 'SELECT * FROM ProfReview WHERE Id = %s'
    cur.execute(qry, [review_id])

    # process results
    row = cur.fetchone()
    if row is None:
        log('W', 'record', 'ProfReview %d not found. Skipping' % review_id)
        return None
    res = {}
    for idx, elem in enumerate(row):
        # encode unicode strings
        # if type(elem) == type(u''):
        #     elem = elem.encode(encoding='utf-8')
        #     elem = elem.replace('"', '\\"').replace('\n', '<br>')
        if TABLE_STRUCT['ProfReview'][idx] in MARKDOWN_FIELDS:
            elem = markdown(elem)
        res[TABLE_STRUCT['ProfReview'][idx]] = elem
    
    return res


def lookup_prof(db, first_name, last_name):
    # perform SQL query
    cur = db.cursor()
    qry = 'SELECT * FROM Professor WHERE UPPER(FirstName) = %s ' + \
              'AND UPPER(LastName) = %s'
    cur.execute(qry, (first_name.upper(), last_name.upper()))

    # process results
    row = cur.fetchone()
    if row is None:
        log('W', 'record',
            'Professor `%s %s` not found. Skipping' % (first_name, last_name))
        return None
    res = {}
    for idx, elem in enumerate(row):
        # encode unicode strings
        # if type(elem) == type(u''):
        #     elem = elem.encode(encoding='utf-8')
        #     elem = elem.replace('"', '\\"').replace('\n', '<br>')
        if TABLE_STRUCT['Professor'][idx] in MARKDOWN_FIELDS:
            elem = markdown(elem)
        res[TABLE_STRUCT['Professor'][idx]] = elem

    # fetch prof reviews
    # prof_reviews = []
    # ignore cases
    # this only handles the case of one space - reviewers feel free to improve
    rids = expand_csl(res['Reviews'])
    res['List_Review'] = ''
    res['List_Research'] =  ''
    for rid in rids:
        try:
            rid = int(rid)
        except:
            log('W', 'record',
                'Could not parse ProfReview id `%s`. Skipping' % rid)
            continue
        review = lookup_prof_review(db, rid)
        if review is None:
            continue
        # validate that review and prof match
        full_name = '%s %s' % (res['FirstName'], res['LastName'])
        if review['Target'].upper() != full_name.upper():
            log('W', 'record',
                'ProfReview %s does not match Professor %s. Skipping.'
                    % (review['Target'], res['Id']))
            continue
        if review['Review']:
            res['List_Review'] += ('- ' + review['Review'] + '\n')
        if review['Research']:
            res['List_Research'] += ('- ' + review['Research'] + '\n')
        # prof_reviews.append(review)
    # res['Reviews'] = prof_reviews
    res['List_Review'] = markdown(res['List_Review']).replace('\n', '')
    res['List_Research'] = markdown(res['List_Research']).replace('\n', '')
    return res


def look_up_course_explore(db, subject, code):
    # perform SQL query
    cur = db.cursor()
    qry = 'SELECT * FROM CourseExplorer ' + \
          'WHERE UPPER(Subject) = %s ' + \
          'AND UPPER(Code) = %s'
    cur.execute(qry, (subject, code))
    
    # process results
    row = cur.fetchone()
    if row is None:
        log('E', 'record', 'Course explorer record: %s %s not found.' % (subject, code))
        return None
    res = {}
    for idx, elem in enumerate(row):
        res[TABLE_STRUCT['CourseExplorer'][idx]] = elem
    if cur.fetchone() is not None:
        log('W', 'record',
            'Coruse explorer record: multiple %s %s found. Using the first one.' % (subject, code))

    # GenEd
    if res['GenEd'] == '':
        res['GenEd'] = 'This course does not meet a General Education requirement.'

    # Link redirection
    # res['Description'] = res['Description'].replace(
    #     '<a href="/schedule/', '<a target="_blank" href=https://courses.illinois.edu/schedule/')
    res['Description'] = res['Description'].replace(
        unicode('&quot;'), '"')
    
    desc = res['Description']
    desc = desc.replace('">', '>')
    desc = desc.replace('<a href="/schedule/', '<a target="_blank" href=https://courses.illinois.edu/schedule/')
    res['Description'] = desc

    return res


def lookup_course(db, subject, code, suffix=''):
    # perform SQL query
    cur = db.cursor()
    qry = 'SELECT * FROM Courses ' + \
          'WHERE UPPER(Subject) = %s ' + \
          'AND UPPER(Code) = %s ' + \
          'AND UPPER(Suffix) = %s'
    cur.execute(qry, (subject.upper(), code.upper(), suffix.upper()))

    # process results
    row = cur.fetchone()
    if row is None:
        log('E', 'record', '%s %s not found.' % (subject, code))
        return None
    res = {}
    for idx, elem in enumerate(row):
        # encode strings. due to utf-8 encoding all strings are unicode strings
        # if type(elem) == type(u''):
        #     elem = elem.encode(encoding='utf-8')
        #     elem = elem.replace('"', '\\"').replace('\n', '<br>')
            # print '> ' + elem          # just to make sure encoding works
        if TABLE_STRUCT['Courses'][idx] in MARKDOWN_FIELDS:
            elem = markdown(elem)
        res[TABLE_STRUCT['Courses'][idx]] = elem
    if cur.fetchone() is not None:
        log('W', 'record',
            'Multiple %s %s found. Using the first one.' % (subject, code))

    # fetch reviews
    # course_reviews = []
    # should ignore space. this cheats a bit becasue it can't handle multiple
    # spaces or tabs. reviewers: feel free to fix (only if time permits)
    course_review_ids = expand_csl(res['Reviews'])
    # a dictionary of difficulties in all categories
    diff_dict = {}
    for diff_entry in DIFF_ITEMS:
        diff_dict[diff_entry] = []
    # a list of keys / column names in CourseReview results
    key_list = []
    for rid in course_review_ids:
        try:
            rid = int(rid)
        except:
            log('W', 'record', 'Unable to parse review id `%s`. Skipped.' % rid)
            continue
        review = lookup_course_review(db, rid)
        if review is None:
            continue
        # validate that review and course match
        if int(review['Target']) != int(res['Id']):
            log('W', 'record',
                'Review %s does not match Course %s. Skipping.' \
                    % (review['Target'], res['Id']))
            continue
        # record difficulty in the diff_dict dictionary
        for diff_entry in DIFF_ITEMS:
            diff_dict[diff_entry].append(review['Diff_' + diff_entry])
        # make each of the other CourseReview attributes a list 
        # in the `res` dictionary
        for review_key in review.keys():
            if review_key[:4] in ('Desc', 'Advi'):
                this_key = "List_" + review_key
                if this_key not in key_list:
                    key_list.append(this_key)
                # if this is the first review, initalize an empty str first
                if this_key not in res:
                    res[this_key] = ''
                # append the `review_key` item from this review
                if review[review_key] != '':
                    # add it as a markdown list entry by adding '- '
                    markdown_str = '- ' + review[review_key] + '\n'
                    res[this_key] += markdown_str
    # for each attribute of CourseReview, convert markdown to html
    for this_key in key_list:
        res[this_key] = markdown(res[this_key])
        res[this_key].replace('\n', '')

    # weight difficulty scores
    init_diff = {}
    for diff_entry in DIFF_ITEMS:
        init_diff[diff_entry] = res['Diff_' + diff_entry]
    weighted_diff = calc_diff(init_diff, diff_dict)
    # Suyie: this is the dictionary you want to use for the graph
    print(weighted_diff)
    for diff_entry in DIFF_ITEMS:
        res['Wtd_Diff_' + diff_entry] = weighted_diff[diff_entry]

    # fetch prof info - same deal
    professor_info = []
    # prof names are separated by comma
    professor_names = expand_csl(res['Professor'])
    for prof_name in professor_names:
        try:
            # important: prof name must follow 'FirstName LastName' format!
            # reviewers: feel free to improve this.
            (first_name, last_name) = prof_name.split(' ')
        except:
            log('W', 'record',
                'Unable to parse professor name `%s`. Skipped' % prof_name)
            continue
        info = lookup_prof(db, first_name, last_name)
        if info is not None:
            professor_info.append(info)
    res['Professor'] = professor_info

    course_explorer = look_up_course_explore(db, subject, code)
    res['CE_Description'] = course_explorer['Description']
    res['CE_Title'] = course_explorer['Title']
    res['CE_Credit'] = course_explorer['Credit']
    res['CE_GenEd'] = course_explorer['GenEd']
    res['CE_Url'] = course_explorer['Url']

    # graph
    pct_list = (
        res['Pct_Lecture'], res['Pct_Discussion'], res['Pct_Homework'], 
        res['Pct_Lab'], res['Pct_Quiz'], res['Pct_Midterm'], 
        res['Pct_Project'], res['Pct_Final'], res['Pct_ExtraCredit'], 
        res['Pct_Other']
    )
    diff_list = (
        weighted_diff['Lecture'], weighted_diff['Discussion'], weighted_diff['Homework'], 
        weighted_diff['Lab'], weighted_diff['Quiz'], weighted_diff['Midterm'],
        weighted_diff['Project'], weighted_diff['Final']
    )
    graph_gen(subject, code, pct_list, diff_list)

    return res


###############################################################################
# UNIT TESTS
###############################################################################

if __name__ == '__main__':
    # Testing connection
    db = connect()
                
    # Testing prof review lookup
    # good
    prof_review = lookup_prof_review(db, 1)
    print(prof_review['Review'])
    # not found
    print(lookup_prof_review(db, 9999999))
                                            
    # Testing prof
    # good
    (fn, ln) = ('ChAnDrA', 'cHeKuRi')    # check that cases are ignored
    prof = lookup_prof(db, fn, ln)
    print(prof['Reviews'][2]['Review'])
    # not found
    print(lookup_prof(db, 'qile', 'WEN'))

    # Testing course review
    # good
    course_review = lookup_course_review(db, 2)
    print(course_review['Advice'])
    # not found
    print(lookup_course_review(db, 99999))

    # Testing course - integrated!
    # good
    course = lookup_course(db, 'cS', '374')
    print(course['Resource'])
    print(course['Professor'][0]['Reviews'][0]['Research'])

    # Testing disconnection
    disconnect(db)
