#!/usr/bin/env python
#-*- coding: utf-8 -*-

from alarm_recognition.alarm_rule_filter import rule_filter
from alarm_recognition.alarm_rule_policy import Q_learning_rule

def rule_match(filename):
    with open(filename, 'r') as rp:
        content = rp.read()
    ruleSet = rule_filter(content)
    rule_policy = Q_learning_rule(ruleSet)
    return rule_policy

def rule_match_from_send(content):
    ruleSet = rule_filter(content)
    rule_policy = Q_learning_rule(ruleSet)
    return rule_policy
