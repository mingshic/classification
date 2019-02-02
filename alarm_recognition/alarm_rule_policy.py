#!/usr/bin/env python
#-*- coding: utf-8 -*-


def Q_learning_rule(ruleSet):
    if len(ruleSet['rule_matched']) == 0 or ruleSet['rule_matched'][0] == '' and ruleSet['rule_matched'][-1] == '':
        ruleSet.update({"建议": "选择人工判断是否开case"})
    elif ruleSet['rule_matched'][0] != '' and ruleSet['rule_matched'][-1] != '':
        ruleSet.update({"建议": "开case"})
    return ruleSet
