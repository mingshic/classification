# coding=utf-8
import os  
import paramiko  

def download(host,port,username,password,remote,local):
    sf = paramiko.Transport((host,port))
    sf.connect(username = username,password = password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        if os.path.isdir(local):
            for f in sftp.listdir(remote):
                sftp.get(os.path.join(remote+f),os.path.join(local+f))
        else:
            sftp.get(remote,local)
    except Exception as e:
          print('download exception:',e)
    sf.close()
