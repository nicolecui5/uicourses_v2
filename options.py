#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#
# UICourses Project
#
# Authored by:   WSB & Suyie
# Drafted:       June 28, 2017
# Last modifed:  June 29, 2017
# Description:   This script contains hardcoded parameters for the database
#
###############################################################################


###############################################################################
# DATABASE OPTIONS
###############################################################################

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

MARKDOWN_FIELDS = (
    'Description',
    'Resource',
    'Tool',
    'Curve',
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
    'Honor',
    'Advice',
    'AdviceForUs',
    'Review',
    'Research',
)
