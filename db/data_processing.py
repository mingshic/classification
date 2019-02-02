#!/usr/bin/env python

def _type_dict(data):
    content = []
    data_content = ""
    content_id = data.pop('id')
    content.append(content_id)
#    for value in data.values():
#        data_content += str(value) + " "
    content.append(data)
    return content



def data_type(data):
    if type(data) is dict:
        data_ = _type_dict(data)
    return data_

                                                               
