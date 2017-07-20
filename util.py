#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# UICourses Project
#
# Authored by:   WSB & Suyie
# Drafted:       June 28, 2017
# Last modifed:  June 29, 2017
# Description:   This script contains some general utilities
#
###############################################################################


from termcolor import colored

###############################################################################
# INFRA UTIL
###############################################################################

def log(type='I', tag='', comment=''):
    tag = tag[:8]
    type = type[0]
    fstr = '{type}    {tag}{tagpad}    {comment}'\
               .format(type=type,
                       tag=tag, tagpad=' ' * (8 - len(tag)),
                       comment=comment)
    
    color = None
    if type.upper() == 'I':
        color = 'cyan'
    if type.upper() == 'C':
        color = 'green'
    if type.upper() == 'W':
        color = 'magenta'
    if type.upper() == 'E':
        color = 'red'
    if type.upper() == 'D':
        color = 'yellow'
    if color is not None:
        fstr = colored(fstr, color)

    print(fstr)


###############################################################################
# DATA FORMAT
###############################################################################

def expand_csl(string):
    if string == '':
        return []
    if string[-1] == ',':
        string = string[:-1]
    return string.replace(', ', ',').split(',')

def append_csl(csl, new_str):
    if csl == '':
        return new_str
    return csl + ',' + new_str

