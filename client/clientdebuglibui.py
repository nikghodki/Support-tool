import re
import json
import time
import zipfile
import os
import urllib.request
import subprocess
import tarfile
import getpass 
import os.path
from os import path
import pandas,csv
import ssl


#Global Variables
data1=0
data2=0
data3=0
data4=0
data5=0


def follow(thefile):
    '''generator function that yields new lines in a file
    '''
    # seek the end of the file
    thefile.seek(0, os.SEEK_END)
    while True:
        line = thefile.readline()
        yield line

def taillogs(inputdomain):
  domain=inputdomain
  logfile = open("/Library/Logs/Netskope/nsdebuglog.log","r")
  loglines = follow(logfile)
  for line in loglines:
    if domain in line:
      return line

def get_sql(query):
    #email=input("Enter the email ID : ")
    
    file = open('./getsql.sh','w')
    file.write("#!/bin/bash\necho \"#!/usr/bin/expect -f\nspawn ssh ngwebui02 \\\"mysql -h mysql02 -u webui -ptheD@t@isM1n312 -e\\\\\\\"USE tenant"+str(tid)+"db; "+str(query)+"\\\\\\\" >> /tmp/"+str(filename)+".txt\\\"\nexpect \\\"Password:\\\"\nsend \\\""+str(p)+"\\r\\\"\ninteract\n\nspawn scp "+str(username)+"@ngwebui02:/tmp/"+str(filename)+".txt /tmp/"+str(filename)+".txt\nexpect \\\"Password:\\\"\nsend \\\""+str(p)+"\\r\\\"\ninteract\n\nspawn ssh ngwebui02 \\\"rm -rf /tmp/"+str(filename)+".txt\\\"\nexpect \\\"Password:\\\"\nsend \\\""+str(p)+"\\r\\\"\ninteract\" > getuser.sh\n\nscp -P 30022 ./getuser.sh 192.168.0.139:~\nssh 192.168.0.139 -p 30022 \"chmod 777 getuser.sh\"\nssh 192.168.0.139 -p 30022 \"./getuser.sh\"\nscp -P 30022  192.168.0.139:/tmp/"+str(filename)+".txt ./"+str(filename)+".txt\nssh 192.168.0.139 -p 30022 \"rm -rf getuser.sh\"\nssh 192.168.0.139 -p 30022 \"rm -rf /tmp/"+str(filename)+".txt\"")
    file.close()
    subprocess.call(['chmod','777','getsql.sh'])
    subprocess.call(['./getsql.sh'])
    out=''
    with open('./'+str(filename)+'.txt') as fileread:
        out=fileread.read()
    print (out)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    folderpath2=str(dir_path) +"/" 
    subprocess.call(['rm','-rf',str(folderpath2)+str(filename)+'.txt'])
    subprocess.call(['rm','-rf','./getsql.sh'])
    subprocess.call(['rm','-rf','./getuser.sh'])
    return

# Def for API Request

def get_account_info(api_url):
     #api_url='https://addon-apria.goskope.com/steering/domains?orgkey=c6egF9ai70f56Sf39p38&userkey=Kv3OLqtLUWAc96btmho6&os=win'
     #response = requests.get(api_url)
     context = ssl._create_unverified_context()
     response = urllib.request.urlopen(api_url,context=context)
     #if response.status_code == 200:
     if response.getcode() == 200:
         data = response.read()
         outddata=json.loads(data.decode('utf-8'))
         return json.dumps(outddata, indent=4)
       #return json.loads(response.content.decode('utf-8'))
     else:
         return None
# Ask to run module of code

def client_specifics(destfolder):
  filepath=str(destfolder) +'/nssteering.json'
  if path.exists(filepath):
    with open(filepath, 'r') as nsdomain:
      try:
        data1 = json.load(nsdomain)
        p1=data1["steering_config_name"]
        p2=data1["traffic_mode"]
      except:
        p1='The nssteering.json file does not exists.'
        p2='The nssteering.json file does not exists.'
  else:
    p1='The nssteering.json file does not exists.'
    p2='The nssteering.json file does not exists.'

  filepath2=str(destfolder) + '/nsbranding.json'
  if path.exists(filepath2):
    with open(filepath2, 'r') as nsbranding:
      try:
        data2 = json.load(nsbranding)
        p3=data2["AddonManagerHost"]
        p4=data2["OrgKey"]
        p5=data2["UserEmail"]
        p6=data2["UserKey"]
      except:
        p3='The nsbranding.json file does not exists.'
        p4='The nsbranding.json file does not exists.'
        p5='The nsbranding.json file does not exists.'
        p6='The nsbranding.json file does not exists.'

  else:
    p3='The nsbranding.json file does not exists.'
    p4='The nsbranding.json file does not exists.'
    p5='The nsbranding.json file does not exists.'
    p6='The nsbranding.json file does not exists.'
#Parsing nsdeviceID.json file
  filepath3=str(destfolder) + '/nsdeviceid.json'
  if path.exists(filepath3):
    with open(filepath3, 'r') as nsdeviceid:
      try:
        data3 = json.load(nsdeviceid)
        p7=str(data3["device_classification_rules"])
      except:
        p7='The nsdeviceid.json file does not exists.'
  else:
    p7='The nsdeviceid.json file does not exists.'
#Parsing nsconfig.json file
  filepath4=str(destfolder) + '/nsconfig.json'
  if path.exists(filepath4):
    with open(filepath4, 'r') as nsconfig:
      try:
        data4 = json.load(nsconfig)
        p8=str(data4["clientConfig"]["configurationName"])
        p9=str(data4["clientConfig"]["allowClientDisabling"])
        p10=str(data4["nsgw"]["host"])
        p11=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(data4["cache"]["configUpdateTimestamp"])))
        if data4["clientConfig"]["hideClientIcon"] == 'false':
          p15='Yes'
        else:
          p15='No'
      except:
        p8='The nsconfig.json file does not exists.'
        p9='The nsconfig.json file does not exists.'
        p10='The nsconfig.json file does not exists.'
        p11='The nsconfig.json file does not exists.'
        p15='The nsconfig.json file does not exists.'
  else:
    p8='The nsconfig.json file does not exists.'
    p9='The nsconfig.json file does not exists.'
    p10='The nsconfig.json file does not exists.'
    p11='The nsconfig.json file does not exists.'
    p15='The nsconfig.json file does not exists.'
  filepath6=str(destfolder) +'/nsuserconfig.json'
  if path.exists(filepath6):
    with open(filepath6, 'r') as nsdomain:
      try:
        data6 = json.load(nsdomain)
        p13=data6["nsUserConfig"]["enablePerUserConfig"]
        p14=data6["nsUserConfig"]["autoupdate"]
      except:
        p13='The nsuser.conf file does not exists.'
        p14='The nsuser.conf file does not exists.'
  else:
    p13='The nsuser.conf file does not exists.'
    p14='The nsuser.conf file does not exists.'
#Parsing nsuser.config file
  filepath5=str(destfolder) +'/nsuser.conf'
  if path.exists(filepath5):
    with open(filepath5, 'r') as nsdomain:
      try:
        data5 = json.load(nsdomain)
        p12=data5["userConfig"]["clientStatus"]
      except:
        p12='The nsuser.conf file does not exists.'
  else:
    p12='The nsuser.conf file does not exists.'
  outr='******************Client Specifics*********************\n\nSteering Config                      : '+str(p1)+'\nTraffic Mode                           : '+str(p2)+'\nAddon Host                            : '+str(p3)+'\nOrg Key                                   : '+str(p4)+'\nUser Email                              : '+str(p5)+'\nUserKey                                  : '+str(p6)+'\nClient Configuration Name    : '+str(p8)+'\nClient can be Disabled           : '+str(p9)+'\nNSGateway Host                    : '+str(p10)+'\nLast Config Update time        : '+str(p11)+'\nClient Status                           : '+str(p12)+'\nClient is in multi-user Mode  : '+str(p13)+'\nAutoUpdate is enabled          : '+str(p14)+'\nClient is Visible                       : '+p15+'\n\n*******************************************************************'
  return outr
def apicheck(destfolder):
  filepath=str(destfolder) +'/nsbranding.json'
  if path.exists(filepath):
    with open(filepath, 'r') as nsbranding:
      data2 = json.load(nsbranding)
      account_info=['a','b','c','d','e','f','g','h','i','j','k','l']
      #https://addon-nikhil.goskope.com/config/org/version?orgkey=s2Ks4M1s58F7lRbMp4H&userkey=8Ny2Kn2NQtgmThL9glma\
      configversion_url='https://' + str(data2["AddonManagerHost"]) + "/config/org/version?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"])
      account_info[0] = get_account_info(configversion_url)
      #https://addon-nikhil.goskope.com/v2/config/org/clientconfig?orgkey=s2Ks4M1s58F7lRbMp4H&hashkey=8Ny2Kn2NQtgmThL9glma&tenantconfig=1\
      tenantadmin_url='https://' + str(data2["AddonManagerHost"]) + "/v2/config/org/clientconfig?orgkey=" + str(data2["OrgKey"]) + "&hashkey=" + str(data2["UserKey"]) +'&tenantconfig=1'
      account_info[1] = get_account_info(tenantadmin_url)
      #https://addon-nikhil.goskope.com/steering/domains?orgkey=s2Ks4M1s58F7lRbMp4H&userkey=8Ny2Kn2NQtgmThL9glma&os=mac\
      domainlist_url='https://' + str(data2["AddonManagerHost"]) + "/steering/domains?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"]) + '&os=mac'
      account_info[2] = get_account_info(domainlist_url)
      #https://addon-nikhil.goskope.com/steering/exceptions?orgkey=s2Ks4M1s58F7lRbMp4H&userkey=8Ny2Kn2NQtgmThL9glma\
      exceptionlist_url='https://' + str(data2["AddonManagerHost"]) + "/steering/exceptions?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"])
      account_info[3] = get_account_info(exceptionlist_url)
      #https://addon-nikhil.goskope.com/steering/pinnedapps?orgkey=s2Ks4M1s58F7lRbMp4H&userkey=8Ny2Kn2NQtgmThL9glma&os=mac\
      certpinned_url='https://' + str(data2["AddonManagerHost"]) + "/steering/pinnedapps?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"])+ '&os=mac'
      account_info[4] = get_account_info(certpinned_url)
      #https://addon-nikhil.goskope.com/v2/config/org/getmanagedchecks?orgkey=s2Ks4M1s58F7lRbMp4H&os=mac\
      deviceidurl='https://' + str(data2["AddonManagerHost"]) + "/v2/config/org/getmanagedchecks?orgkey=" + str(data2["OrgKey"]) + '&os=mac'
      account_info[5] = get_account_info(deviceidurl)
      #https://addon-nikhil.goskope.com/steering/categories?orgkey=s2Ks4M1s58F7lRbMp4H&userkey=8Ny2Kn2NQtgmThL9glma\
      catbypass_url='https://' + str(data2["AddonManagerHost"]) + "/steering/categories?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"]) 
      account_info[6] = get_account_info(catbypass_url)
      #https://addon-nikhil.goskope.com/config/getoverlappingdomainlist?orgkey=s2Ks4M1s58F7lRbMp4H\
      overlapping_url='https://' + str(data2["AddonManagerHost"]) + "/config/getoverlappingdomainlist?orgkey=" + str(data2["OrgKey"])
      account_info[7] = get_account_info(overlapping_url)
      #https://addon-nikhil.goskope.com/config/org/gettunnelpolicy?orgkey=s2Ks4M1s58F7lRbMp4H&os=mac\
      nstunnel_url='https://' + str(data2["AddonManagerHost"]) + "/config/org/gettunnelpolicy?orgkey=" + str(data2["OrgKey"])  + '&os=mac'
      account_info[8] = get_account_info(nstunnel_url)
      #https://addon-nikhil.goskope.com/v2/checkupdate?orgkey=s2Ks4M1s58F7lRbMp4H&os=mac&userkey=8Ny2Kn2NQtgmThL9glma\
      stagentupdate_url='https://' + str(data2["AddonManagerHost"]) + "/v2/checkupdate?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"]) + '&os=mac'
      account_info[9] = get_account_info(stagentupdate_url)
      #https://addon-takeda.goskope.com/v1/config/user/getbrandingbyupn?orgkey=USUL7U1eToSHBKA3784n&upn=jn3542@onetakeda.com
      branding_url='https://' + str(data2["AddonManagerHost"]) + "/v1/config/user/getbrandingbyupn?orgkey=" + str(data2["OrgKey"]) + "&upn=" + str(data2["UserEmail"])
      account_info[10] = get_account_info(branding_url)
      #https://addon-nikhil.goskope.com/v3/support/client/get?hashkey=8Ny2Kn2NQtgmThL9glma&orgkey=s2Ks4M1s58F7lRbMp4H\
      supportability_url='https://' + str(data2["AddonManagerHost"]) + "/v3/support/client/get?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"])
      account_info[11] = get_account_info(supportability_url)
      API_name={'config version API': account_info[0],'tenant admin API': account_info[1],'Domain list API': account_info[2],'exception list API': account_info[3],'certpinned API': account_info[4],'deviceid API': account_info[5],'catbypass API': account_info[6],'overlapping API': account_info[7],'nstunnel API': account_info[8],'stagentupdate API': account_info[9],'Branding File': account_info[10],'supportability API': account_info[11]}
      return API_name
  else:
    return "nsbranding file is not present"
def apinsbrandingout(destfolder):
  filepath=str(destfolder) +'/nsbranding.json'
  if path.exists(filepath):
    with open(filepath, 'r') as nsbranding:
      data2 = json.load(nsbranding)
      branding_url='https://' + str(data2["AddonManagerHost"]) + "/v1/config/user/getbrandingbyupn?orgkey=" + str(data2["OrgKey"]) + "&upn=" + str(data2["UserEmail"])
      return get_account_info(branding_url)
  else:
    return "nsbranding file is not present"

def apiexceptionout(destfolder):
  filepath=str(destfolder) +'/nsbranding.json'
  if path.exists(filepath):
    with open(filepath, 'r') as nsbranding:
      data2 = json.load(nsbranding)
      exceptionlist_url='https://' + str(data2["AddonManagerHost"]) + "/steering/exceptions?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"])
      return get_account_info(exceptionlist_url)
  else:
    return "nsexception file is not present"
def apinsuserout(destfolder):
  filepath=str(destfolder) +'/nsbranding.json'
  if path.exists(filepath):
    with open(filepath, 'r') as nsbranding:
      data2 = json.load(nsbranding)
      tenantadmin_url='https://' + str(data2["AddonManagerHost"]) + "/v2/config/org/clientconfig?orgkey=" + str(data2["OrgKey"]) + "&hashkey=" + str(data2["UserKey"]) +'&tenantconfig=1'
      return get_account_info(tenantadmin_url)
  else:
    return "nsuser file is not present"
def apibypassout(destfolder):
  filepath=str(destfolder) +'/nsbranding.json'
  if path.exists(filepath):
    with open(filepath, 'r') as nsbranding:
      data2 = json.load(nsbranding)
      certpinned_url='https://' + str(data2["AddonManagerHost"]) + "/steering/pinnedapps?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"])+ '&os=mac'
      return get_account_info(certpinned_url)
  else:
    return "Bypass file is not present"
def apisteeringout(destfolder):
  filepath=str(destfolder) +'/nsbranding.json'
  if path.exists(filepath):
    with open(filepath, 'r') as nsbranding:
      data2 = json.load(nsbranding)
      domainlist_url='https://' + str(data2["AddonManagerHost"]) + "/steering/domains?orgkey=" + str(data2["OrgKey"]) + "&userkey=" + str(data2["UserKey"]) + '&os=mac'
      return get_account_info(domainlist_url)
  else:
    return "nssteering file is not present"


def unzipfolder(foldername):
  folder=foldername[:-4]
  zip_ref = zipfile.ZipFile(foldername, 'r')
  zip_ref.extractall(folder)
  return folder

def checkerrorlogs(foldername):
  filepath=str(foldername) +'/nsdebuglog.log'
  if path.exists(filepath):
    df=pandas.read_csv('logcheck.csv')
    outremedy=[]
    dicto={}
    out={}
    file=open(filepath,'r')
    for line in file:
      for phrase in df['Log line']:
        if phrase in line:
          outerror=(df.loc[df['Log line'] == phrase, 'issue'].iloc[0])
          outremedy=(df.loc[df['Log line'] == phrase, 'remediation'].iloc[0])
          dicto[outerror]=outremedy
          out[line]=dicto
          dicto={}
    file.close()
    return out
  else:
    return "nsdebuglog.log is not available"

     
