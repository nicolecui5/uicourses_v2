#!/usr/bin/env python

from options import *


def calc_diff(init_diff, addit_diff):
    weighted_diff = {}
    for diff_entry in DIFF_ITEMS:
        total_val = 0
        denominator = 0
        # initial value
        if init_diff[diff_entry] is not None:
            if init_diff[diff_entry] != 0:
                total_val += float(init_diff[diff_entry]) * INIT_INFO_WEIGHT
                denominator += INIT_INFO_WEIGHT
        # additional values
        for add_val in addit_diff[diff_entry]:
            if add_val is not None:
                if add_val != 0:
                    total_val += float(add_val)
                    denominator += 1
        if denominator == 0:
            denominator = 1
        weighted_diff[diff_entry] = total_val / float(denominator)
    return weighted_diff
