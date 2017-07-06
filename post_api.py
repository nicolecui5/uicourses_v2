#!/usr/bin/env python

import cgi
import argparse
import SocketServer
import BaseHTTPServer
import logging
import sys
from dbutil import *


def usage():
    print('USAGE:    ./insertion_api.py <port>')
    exit(1)


def course_handler():
    pass


def course_review_handler():
    pass


def prof_handler():
    pass


def prof_review_handler():
    pass



def dispatch_insertion(postvars):
    if 'toTable' not in list(postvars.keys()):
        return 'toTable not found'
    handlers = {
        'Courses': courses_handler,
        'CourseReview': course_review_handler,
        'Professor': professor_handler,
        'ProfReview': prof_review_handler
    }
    handlers[postvars['toTable']](postvars)


class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/txt')
        self.end_headers()


    def do_POST(self):
        # Parse POST parameters
        # http://stackoverflow.com/questions/4233218/python-basehttprequesthandler-post-variables
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        print(postvars)
        dispatch_insertion(postvars)


if __name__ == '__main__':
    try:
        PORT = int(sys.argv[1])
    except:
        usage()

    db = connect()

    httpd = SocketServer.TCPServer(('', PORT), RequestHandler)
    httpd.serve_forever()

    db.disconnect()
