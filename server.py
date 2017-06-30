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
# TODOs:         1. Change log format
#                2. Change log color
#
###############################################################################


import json
import SocketServer
import SimpleHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler
from urlparse import parse_qs
from sys import argv
from util import *
from options import *
from dbutil import *

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
        # print(json_str.encode('utf-8').decode('unicode-escape'))
        self.wfile.write(json_str.decode('unicode-escape').encode('utf-8'))
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

