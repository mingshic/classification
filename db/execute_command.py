#-*- coding: utf-8 -*-
#!/usr/bin/env python


from .model import MysqlDB
#from .data_processing import data_type 

#data_deal = data_analysis()

class command_ready(MysqlDB):
    def __init__(self):
        super(command_ready,self).__init__()
        self.conn = self.connection
    
    def create_table(self, table):
        sql = '''create table if not exists %s(id int not null primary key auto_increment, custom_code VARCHAR(1000) character set utf8 collate utf8_bin, rule_id varchar(1000) character set utf8 collate utf8_bin, rule_name varchar(1000) character set utf8 collate utf8_bin, rule_matched varchar(1000) character set utf8 collate utf8_bin, suggest_operate_case varchar(1000) character set utf8 collate utf8_bin, alarm_content MEDIUMTEXT, SN varchar(50) character set utf8 collate utf8_bin, top_response int, create_by varchar(1000) character set utf8 collate utf8_bin, create_on timestamp, modified_by varchar(1000) character set utf8 collate utf8_bin, modified_on timestamp DEFAULT CURRENT_TIMESTAMP) engine=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin''' % (table)        
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()

    def insert_alarm(self, data, policySet):
        policy_matched = str(policySet['rule_matched'])
#        content_id, data_content = data_deal.data_type(data)
#        data_content = str(data[1]['alarm_title'])+' '+str(data[1]['alarm_level'])+' '+str(data[1]['alarm_content'])+' '+str(data[1]['processer'])+' '+str(data[1]['instance'])+' '+str(data[1]['service_name'])
        data_content = str(data[1]['alarm_title'])+str(data[1]['alarm_level'])+str(data[1]['processer'])+str(data[1]['instance'])+str(data[1]['service_name'])+str(data[1]['alarm_content'])
        try:
            if "'" in data_content:
                data_content = data_content.replace("'","")
            elif '"' in data_content:
                data_content = data_content.replace('"',"")
        except:
            pass
        try:
            if "'" in policy_matched:
                policy_matched = policy_matched.replace("'","")
            elif '"' in policy_matched:
                policy_matched = policy_matched.replace('"',"")
        except:
            pass
#        print (data[0],policySet['建议'],data[1])
        sql = '''insert into rule_recotb (rule_id,rule_matched,suggest_operate_case,alarm_content,SN,top_response) values ('%s','%s','%s','%s','%s','%s')''' % (data[1]['rule_id'],policy_matched,policySet['建议'],data_content,data[1]['SN'],data[2]['top_response'])     

#        sql = '''insert into test (a) values ('%s')''' % (data['alarm_content'])
        conn = self.conn
        conn.execute(sql)
        conn.connection.commit()
        conn.connection.close()
        
