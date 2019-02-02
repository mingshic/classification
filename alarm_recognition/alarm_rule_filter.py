#!/usr/bin/env python
#-*- coding: utf-8 -*-

from .rule_settings import DEF_SEVIRITY_KEYWORDS


def rule_filter(content):
    ruleSet = {}
    rules = []
    ruleSplitSet = DEF_SEVIRITY_KEYWORDS[0].split(";")
    for rule in ruleSplitSet:
        if rule in str(content) and rule != '' and rule != ' ':
            rules.append(rule)
#    if len(rules) != 0:
    ruleSet.update({"rule_matched": rules})
    return ruleSet
