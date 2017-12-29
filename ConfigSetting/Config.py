import configparser
import os
import sys
import pprint
BASIC_SECTION ='Basic_Config'
current_path = os.path.dirname(__file__)

if 'config.ini' in os.listdir(current_path):
    config_path = os.path.join(current_path,'config.ini')
    cf = configparser.ConfigParser()
    cf.read(config_path)
    MONGODB_IP = cf.get(BASIC_SECTION,'mongodb_ip')
    MONGODB_PORT = cf.get(BASIC_SECTION,'mongodb_port')
    MONGODB_USER = cf.get(BASIC_SECTION,'mongodb_user')
    MONGODB_PWD = cf.get(BASIC_SECTION,'mongodb_pwd')
    MONGODB_DB = cf.get(BASIC_SECTION,'mongodb_db')
    MONGODB_SYS_DB = cf.get(BASIC_SECTION,'mongodb_system_db')
    MONGODB_TENANT_DB = cf.get(BASIC_SECTION,'modgodb_tenant_db')
    USER=cf.get(BASIC_SECTION,'user')
    PASSWORD=cf.get(BASIC_SECTION,'pwd')
    DOMAIN = cf.get(BASIC_SECTION,'domain')
    TENANT = cf.get(BASIC_SECTION,'tenant')
    HOST_URL = cf.get(BASIC_SECTION,'host_url')
    MONGODB_SSL = cf.get(BASIC_SECTION,"mongodb_ssl")

else:
    print('Current path does not config.ini file')
    sys.exit()

def log(result):
    if isinstance(result,dict) and result.get('statusCode') == 0:
        pprint.pprint(result)
    elif isinstance(result,str):
        pprint.pprint("======="+ result+"==========")
    elif isinstance(result,dict):
        pprint.pprint(result)
    else:
        pprint.pprint('execute API Failed:%s'%result)
