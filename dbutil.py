#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# UICourses Project
#
# Authored by:   WSB & Suyie
# Drafted:       June 27, 2017
# Last modifed:  June 28, 2017
# Debugged:      June 28, 2017
# Description:   This script provides functions that fetch data from the MySQL
#                database and parse them into python dictionary. This is
#                needed as a part of the db2json api. For security reason this
#                script should run on the server. Otherwise remote database
#                access must be granted for it to work.
# TODOs:         1. Markdown support
#                2. Refactor util and options into a separate file
#
###############################################################################


import MySQLdb as dblib
from traceback import print_tb

###############################################################################
# GLOBAL OPTIONS
###############################################################################

DB = {
    'username': 'uicourses',
    'password': 'Haochideyumi!',
    'database': 'uicourse_uicourses_v2'
}

# Could have queried from .Columns tables. Reviewers feel free to improve
TABLE_STRUCT = {
    'Courses': (
        'Id',
        'Reviews',
        'InitUid',
        'Subject',
        'Code',
        'Suffix',
        'Title',
        'Professor',
        'Description',
        'Knowledge',
        'Resource',
        'Tool',
        'Letter_Ap',
        'Letter_A',
        'Letter_Am',
        'Letter_Bp',
        'Letter_B',
        'Letter_Bm',
        'Curve',
        'Pct_Lecture',
        'Pct_Discussion',
        'Pct_Homework',
        'Pct_Lab',
        'Pct_Quiz',
        'Pct_Midterm',
        'Pct_Project',
        'Pct_Final',
        'Pct_ExtraCredit',
        'Pct_Other',
        'Desc_Lecture',
        'Desc_Discussion',
        'Desc_Homework',
        'Desc_Lab',
        'Desc_Quiz',
        'Desc_Midterm',
        'Desc_Project',
        'Desc_Final',
        'Desc_ExtraCredit',
        'Desc_Other',
        'Diff_Lecture',
        'Diff_Discussion',
        'Diff_Homework',
        'Diff_Lab',
        'Diff_Quiz',
        'Diff_Midterm',
        'Diff_Project',
        'Diff_Final',
        'Honor',
    ),
    'CourseReview': (
        'Id',
        'Target',
        'Desc_Lecture',
        'Desc_Discussion',
        'Desc_Homework',
        'Desc_Lab',
        'Desc_Quiz',
        'Desc_Midterm',
        'Desc_Project',
        'Desc_Final',
        'Desc_ExtraCredit',
        'Desc_Other',
        'Diff_Lecture',
        'Diff_Discussion',
        'Diff_Homework',
        'Diff_Lab',
        'Diff_Quiz',
        'Diff_Midterm',
        'Diff_Project',
        'Diff_Final',
        'Advice',
        'AdviceForUs',
    ),
    'Professor': (
        'Id',
        'Reviews',
        'FirstName',
        'LastName',
        'Course',
        'Review',
    ),
    'ProfReview': (
        'Id',
        'Target',
        'Review',
        'Research',
    ),
}



###############################################################################
# INFRA UTIL
###############################################################################

def log(type='I', tag='', comment=''):
    tag = tag[:8]
    type = type[0]
    print('{type}    {tag}{tagpad}    {comment}'\
               .format(type=type,
                       tag=tag, tagpad=' ' * (8 - len(tag)),
                       comment=comment))

def expand_csl(string):
    if string == '':
        return []
    if string[-1] == ',':
        string = string[:-1]
    return string.replace(', ', ',').split(',')


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
        #     elem = elem.encode(encoding='utf-8')
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
        res[TABLE_STRUCT['Professor'][idx]] = elem

    # fetch prof reviews
    prof_reviews = []
    # ignore cases
    # this only handles the case of one space - reviewers feel free to improve
    rids = expand_csl(res['Reviews'])
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
        if review['Target'] != res['Id']:
            log('W', 'record',
                'ProfReview %d does not match Professor %d. Skipping.'
                    % (review['Target'], res['Id']))
            continue
        prof_reviews.append(review)
    res['Reviews'] = prof_reviews
    return res


def lookup_course(db, subject, code):
    # perform SQL query
    cur = db.cursor()
    # TODO add suffix check
    qry = 'SELECT * FROM Courses WHERE UPPER(Subject) = %s AND UPPER(Code) = %s'
    cur.execute(qry, (subject.upper(), code.upper()))

    # process results
    row = cur.fetchone()
    if row is None:
        log('E', 'record', '%s %s not found.' % subject, code)
        return None
    res = {}
    for idx, elem in enumerate(row):
        # encode strings. due to utf-8 encoding all strings are unicode strings
        # if type(elem) == type(u''):
        #     elem = elem.encode(encoding='utf-8')
            # print '> ' + elem          # just to make sure encoding works
        res[TABLE_STRUCT['Courses'][idx]] = elem
    if cur.fetchone() is not None:
        log('W', 'record',
            'Multiple %s %s found. Using the first one.' % (subject, code))

    # fetch reviews
    course_reviews = []
    # should ignore space. this cheats a bit becasue it can't handle multiple
    # spaces or tabs. reviewers: feel free to fix (only if time permits)
    course_review_ids = expand_csl(res['Reviews'])
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
        if review['Target'] != res['Id']:
            log('W', 'record',
                'Review %d does not match Course %d. Skipping.'
                    % (review['Target'], res['Id']))
            continue
        course_reviews.append(review)
    res['Reviews'] = course_reviews

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
