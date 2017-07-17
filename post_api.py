#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# UICourses Project
#
# Authored by:   WSB & Suyie
# Drafted:       June 18, 2017
# Last modified: June 29, 2017
# Description:   This is a simple server that acts as an db-to-json API.
#                It calls function from dbutil.py. It takes in GET request and
#                returns the query results as a json string.
#
###############################################################################


import json
import SocketServer
import SimpleHTTPServer
import cgi
import argparse
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import parse_qs
from sys import argv
from util import *
from options import *
from dbutil import *
from credentials import USERS
from search_prof_info import *

try:
    PORT = int(argv[1])
except:
    usage()
REQUEST_HEAD = '/dbapi'
DEBUG = True


def usage():
    print('USAGE:    ./server.py <port>')


def validate_key(key):
    return key in KEYS

def validate_id(username, password):
    if username not in list(USERS.keys()):
        return False
    return USERS[username] == password

def courses_handler(postvars):
    cmd = '''
    INSERT INTO `Courses` 
    (`Id`, `Reviews`,
    `InitUid`, `Subject`, `Code`, `Suffix`, `Title`, `Professor`, 
    `Description`, `Knowledge`, `Resource`, `Tool`, 
    `Letter_Ap`, `Letter_A`, `Letter_Am`, 
    `Letter_Bp`, `Letter_B`, `Letter_Bm`, 
    `Curve`,
    `Pct_Lecture`, `Pct_Discussion`, `Pct_Homework`, `Pct_Lab`, `Pct_Quiz`, 
    `Pct_Midterm`, `Pct_Project`, `Pct_Final`, `Pct_ExtraCredit`, `Pct_Other`, 
    `Desc_Lecture`, `Desc_Discussion`, `Desc_Homework`, `Desc_Lab`, 
    `Desc_Quiz`, `Desc_Midterm`, `Desc_Project`, `Desc_Final`, 
    `Desc_ExtraCredit`, `Desc_Other`, 
    `Diff_Lecture`, `Diff_Discussion`, `Diff_Homework`, `Diff_Lab`, 
    `Diff_Quiz`, `Diff_Midterm`, `Diff_Project`, `Diff_Final`, 
    `Honor`) 
    VALUES (NULL, '',
            %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s, 
            %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s)
    '''
    fields = [postvars['InitUid'][0],
              postvars['Subject'][0],
              postvars['Code'][0],
              postvars['Suffix'][0],
              postvars['Title'][0],
              postvars['Professor'][0],
              postvars['Description'][0],
              postvars['Knowledge'][0],
              postvars['Resource'][0],
              postvars['Tool'][0],
              postvars['Letter_Ap'][0],
              postvars['Letter_A'][0],
              postvars['Letter_Am'][0],
              postvars['Letter_Bp'][0],
              postvars['Letter_B'][0],
              postvars['Letter_Bm'][0],
              postvars['Curve'][0],
              postvars['Pct_Lecture'][0],
              postvars['Pct_Discussion'][0],
              postvars['Pct_Homework'][0],
              postvars['Pct_Lab'][0],
              postvars['Pct_Quiz'][0],
              postvars['Pct_Midterm'][0],
              postvars['Pct_Project'][0],
              postvars['Pct_Final'][0],
              postvars['Pct_ExtraCredit'][0],
              postvars['Pct_Other'][0],
              postvars['Desc_Lecture'][0],
              postvars['Desc_Discussion'][0],
              postvars['Desc_Homework'][0],
              postvars['Desc_Lab'][0],
              postvars['Desc_Quiz'][0],
              postvars['Desc_Midterm'][0],
              postvars['Desc_Project'][0],
              postvars['Desc_Final'][0],
              postvars['Desc_ExtraCredit'][0],
              postvars['Desc_Other'][0],
              postvars['Diff_Lecture'][0],
              postvars['Diff_Discussion'][0],
              postvars['Diff_Homework'][0],
              postvars['Diff_Lab'][0],
              postvars['Diff_Quiz'][0],
              postvars['Diff_Midterm'][0],
              postvars['Diff_Project'][0],
              postvars['Diff_Final'][0],
              postvars['Honor'][0]]
    # print(cmd)
    cur = db.cursor()
    cur.execute(cmd, fields)
    log('C', 'hand.', 'Course %s %s written.' \
                       % (postvars['Subject'][0], postvars['Code'][0]))

def course_review_handler(postvars):
    cmd = '''
    INSERT INTO `CourseReview` 
    (`Id`, 
    `Target`, 
    `Desc_Lecture`, `Desc_Discussion`, `Desc_Homework`, `Desc_Lab`, 
    `Desc_Quiz`, `Desc_Midterm`, `Desc_Project`, `Desc_Final`, 
    `Desc_ExtraCredit`, `Desc_Other`, 
    `Diff_Lecture`, `Diff_Discussion`, `Diff_Homework`, `Diff_Lab`, 
    `Diff_Quiz`, `Diff_Midterm`, `Diff_Project`, `Diff_Final`, 
    `Advice`, `AdviceForUs`) 
    VALUES (NULL, 
    %s, 
    %s, %s, %s, %s, 
    %s, %s, %s, %s,
    %s, %s, 
    %s, %s, %s, %s, 
    %s, %s, %s, %s, 
    %s, %s)
    '''
    # print(cmd)
    target = '%s %s %s' \
                % (postvars['targetCourse::subject'][0],
                   postvars['targetCourse::code'][0],
                   postvars['targetCourse::suffix'][0])
    field = [
        target,
        postvars['Desc_Lecture'][0],
        postvars['Desc_Discussion'][0],
        postvars['Desc_Homework'][0],
        postvars['Desc_Lab'][0],
        postvars['Desc_Quiz'][0],
        postvars['Desc_Midterm'][0],
        postvars['Desc_Project'][0],
        postvars['Desc_Final'][0],
        postvars['Desc_ExtraCredit'][0],
        postvars['Desc_Other'][0],
        postvars['Diff_Lecture'][0],
        postvars['Diff_Discussion'][0],
        postvars['Diff_Homework'][0],
        postvars['Diff_Lab'][0],
        postvars['Diff_Quiz'][0],
        postvars['Diff_Midterm'][0],
        postvars['Diff_Project'][0],
        postvars['Diff_Final'][0],
        postvars['Advice'][0],
        postvars['AdviceForUs'][0] 
    ]
    cur = db.cursor()
    cur.execute(cmd, field)
    log('C', 'hand.', 'CourseReview for `%s` written.' % target)
    
    # Update review list in target
    # get last id
    cur.execute('SELECT LAST_INSERT_ID();')
    row = cur.fetchone()
    review_id = row[0]

    # get current list
    cmd = '''
    SELECT `Id`, `Reviews` FROM `Courses`
    WHERE UPPER(`Subject`) = %s 
    AND UPPER(`Code`) = %s 
    AND UPPER(`Suffix`) = %s;
    '''
    fields = [postvars['targetCourse::subject'][0].upper(), 
              postvars['targetCourse::code'][0].upper(),
              postvars['targetCourse::suffix'][0].upper()]
    cur.execute(cmd, fields)
    row = cur.fetchone()
    course_id, curr_csl = row[0], row[1]
    new_csl = append_csl(curr_csl, str(review_id))
    if cur.fetchone() is not None:
        log('W', 'record', 'Duplicate exists for %s' % str(fields))
    
    # update list
    cmd = '''
    UPDATE `Courses`
    SET `Reviews` = %s
    WHERE `Id` = %s;
    '''
    cur.execute(cmd, [new_csl, course_id])
    log('C', 'hand.', 'Review appended to target course in Courses table.')

def professor_handler(postvars):
    cmd = '''
    INSERT INTO `Professor` (`Id`, `Reviews`, `RMP_index`, `FirstName`, `LastName`, 
    `Course`, `Review`) VALUES (NULL, '', %s, %s, '', %s);
    '''
    # print(cmd)
    cur = db.cursor()
    cur.execute(cmd,
                [postvars['FirstName'][0], postvars['LastName'][0],
                 postvars['Review'][0]])
    log('C', 'hand.', 'Professor %s written.' % postvars['LastName'][0])


    # Change start
    cmd = '''
    INSERT INTO `RateMyProfessorInfo` (`Id`, `firstName`, `lastName`, `tag`, `url`, `difficulty`, `quality`)
    VALUES (NULL,)
    '''
    # Change end

def prof_review_handler(postvars):
    full_name = '%s %s' \
                % (postvars['targetProf::firstName'][0],
                   postvars['targetProf::lastName'][0])
    cmd = '''
    INSERT INTO `ProfReview` (`Id`, `Target`, `Review`, `Research`)
    VALUES (NULL, %s, %s, %s);
    '''
    # print(cmd)
    cur = db.cursor()
    cur.execute(cmd,
                [full_name, postvars['Review'][0], postvars['Research'][0]])
    log('C', 'hand.', 'ProfReview to %s written.'
                      % postvars['targetProf::lastName'][0])

    # Update review list in target
    # get last id
    cur.execute('SELECT LAST_INSERT_ID();')
    row = cur.fetchone()
    review_id = row[0]

    # get current list
    cmd = '''
    SELECT `Id`, `Reviews` FROM `Professor`
    WHERE UPPER(`FirstName`) = %s 
    AND UPPER(`LastName`) = %s;
    '''
    fields = [postvars['targetProf::firstName'][0].upper(), 
              postvars['targetProf::lastName'][0].upper()]
    cur.execute(cmd, fields)
    row = cur.fetchone()
    course_id, curr_csl = row[0], row[1]
    new_csl = append_csl(curr_csl, str(review_id))
    if cur.fetchone() is not None:
        log('W', 'record', 'Duplicate exists for %s' % str(fields))
    
    # update list
    cmd = '''
    UPDATE `Professor`
    SET `Reviews` = %s
    WHERE `Id` = %s;
    '''
    cur.execute(cmd, [new_csl, course_id])
    log('C', 'hand.', 'Review appended to target prof in Professor table.')


def dispatch(postvars):
    if 'toTable' not in list(postvars.keys()):
        return 'no toTable found'
    toTable = postvars['toTable'][0]
    handlers = {
        'Courses': courses_handler,
        'CourseReview': course_review_handler,
        'Professor': professor_handler,
        'ProfReview': prof_review_handler
    }
    if toTable not in list(handlers.keys()):
        log('E', 'disp.', 'invalid toTable')
    log('I', 'disp.', 'handler: %s' % toTable)
    handlers[toTable](postvars)

class RequestHandler(BaseHTTPRequestHandler):
    def write_response(self, d):
        # send header
        self.send_response(200)
        self.send_header('Content-type', 'text/json; charset=utf-8')
        self.end_headers()
        log('I', 'conn', 'Header sent.')

        # send data
        log('I', 'conn', 'Sending data...')
        json_str = json.dumps(d)
        # print(json_str.encode('utf-8').decode('unicode-escape').replace('\n', '\\n'))
        self.wfile.write(json_str.replace('"', '\\"')
                         .decode('unicode-escape')
                         .encode('utf-8')
                         .replace('\n', '\\n'))
        log('C', 'conn', 'Data sent.')

        # clean up
        self.wfile.close()
        log('C', 'conn', 'Connection closed.')

    def exit_on_error(self, details):
        log('I', 'conn', 'Initiating exit_on_error...')
        d = {
            'status': 'Error',
            'message': details
        }
        self.write_response(d)
        log('E', 'exit', details)

    def do_POST(self):
        # http://stackoverflow.com/questions/4233218/python-basehttprequesthandler-post-variables
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        # print(postvars)
        if 'Username' not in list(postvars.keys()) \
                or 'Password' not in list(postvars.keys()):
            log('E', 'vali.', 'No credentials.')
            self.exit_on_error('No credentials.')
            return
        if not validate_id(postvars['Username'][0], postvars['Password'][0]):
            log('E', 'vali.', 'Wrong credentials.')
            self.exit_on_error('Wrong credentials.')
            return
        # print(postvars)
        try:
            dispatch(postvars)
            self.write_response({'Status': 'OK'})
        except:
            log('E', 'hand.', 'Handler throws an exception.')
            self.exit_on_error('Handler throws and exception.')
            

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

    def do_GET(self):
        # Ignore favicon requests
        if self.path == '/favicon.ico':
            return

        log('I', 'conn', 'Connection established.')
        log('I', 'api', 'request: ' + self.path)

        # Validation filters
        log('I', 'api', 'Validating parameters...')
        if self.path[:len(REQUEST_HEAD)] != REQUEST_HEAD:
            log('E', 'api', 'does not start with request head (%s)' % REQUEST_HEAD)
            self.exit_on_error('does not start with request head')
            return
        if len(self.path) <= len(REQUEST_HEAD) + 1:  # 1 covers `?`
            log('E', 'api', 'does not have GET parameters')
            self.exit_on_error('does not have GET parameters')
            return

        # Parse and check action
        request_param = parse_qs(self.path[len(REQUEST_HEAD) + 1:])
        if 'subject' not in list(request_param.keys()) or \
                'code' not in list(request_param.keys()) or \
                'key' not in list(request_param.keys()):
            self.exit_on_error('subject/code/key found')
            return
       
        # validate api key
        if not validate_key(request_param['key'][0]):
            self.exit_on_error('Invalid API key')
            return
        log('I', 'api', 'Filters validated.')

        # lookup
        subject = request_param['subject'][0]
        code = request_param['code'][0]
        suffix = ''
        if 'suffix' in list(request_param.keys()):
            suffix = request_param['suffix'][0]
        log('I', 'api', 'Looking up: %s %s %s' % (subject, code, suffix))
        res = lookup_course(db, subject, code, suffix)
        log('I', 'api', 'Lookup done.')
       
        # send response
        log('I', 'api', 'Sending response...')
        if res is None:
            self.exit_on_error('course not found')
            return
        res['Status'] = 'OK'
        self.write_response(res)


if __name__ == '__main__':
    # Db connection
    log('I', 'db', 'Connecting to database...')
    db = connect()
    log('C', 'db', 'Connected to database.')
    
    # Server setup
    log('I', 'db', 'Setting up server...')
    httpd = SocketServer.TCPServer(('', PORT), RequestHandler)
    m = SimpleHTTPServer.SimpleHTTPRequestHandler.extensions_map
    m[''] = 'text/plain'
    m.update(dict([(k, v + ';charset=UTF-8') for k, v in m.items()]))
    log('C', 'db', 'Setup done..')
    log('I', 'db', 'Serve...')
    httpd.serve_forever()
    db.disconnect()

