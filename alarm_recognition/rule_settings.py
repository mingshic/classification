#!/usr/bin/env python
#-*- coding: utf-8 -*-


#DEF_SEVIRITY_KEYS = [u'紧急', u'主要', u'次要', u'警告',u'正常']

#DEF_SEVIRITY_RULE = {'name': 'SEVIRITY','model': 'KEYWORD', 'field': 'Sevirity', 'slog': '级别'}

DEF_SEVIRITY_KEYWORDS = [
    'PROCESS WARNING;批处理运行失败;Status: No answer;Status: Bad;本日调度失败;>不可用;分区利用率超过90%;故障中 级别: Disaster;故障中 级别: High;级别：紧急;- 故障 -;级 别：紧急;>=95%;告警级别：5;- 严重 -;>=96%;>=90%;严重:;故障中 级别: Average;故障中 级别: Warning;故障中 级别: information;故障中 级别: Not classified;告警级别：4;- 错误 - ;UAT;SIT;>=85%;>=80%;警告:;告警级别：3;告警级别：2;>=75%;>=70%;- 警告 - ;10.1.188.9;up;恢复;告警级别：1;信息;状态: 故障已恢复;设备告警结束;Nagios;'
]
