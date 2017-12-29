print(__file__)
import sys
import os

from pymongo import MongoClient
# sys.path.insert()

from ConfigSetting import Config

MONGODB_IP = Config.MONGODB_IP
MONGODB_PORT = Config.MONGODB_PORT
MONGODB_USER = Config.MONGODB_USER
MONGODB_PWD = Config.MONGODB_PWD
MONGODB_DB = Config.MONGODB_DB
MONGODB_SYS_DB = Config.MONGODB_SYS_DB
MONGODB_TENANT_DB = Config.MONGODB_TENANT_DB
MONGODB_SSL = True
from bson.objectid import ObjectId
from urllib import parse
import gridfs

class Mongodb_Connect():
    
    def __init__(self,ip,port,db=None,collect=None,username=None,password=None,ssl=False):
        self.ip=ip
        self.port=port
        self.db=db
        self.collect=collect
        self.username = parse.quote_plus(username)
        self.password = parse.quote_plus(password)
        self.ssl = ssl
    def _conn_db(self):
        if self.username !=None and self.password != None and self.ssl==False:
            client=MongoClient('mongodb://%s:'%self.username + self.password +"@%s"%self.ip+":"+str(self.port))
            return  client[self.db]
        elif self.username !=None and self.password != None and self.ssl == True:
            client=MongoClient('mongodb://%s:'%self.username + self.password +"@%s"%self.ip+":"+str(self.port)+"/"+'?ssl=true&ssl_cert_reqs=CERT_NONE')
            return  client[self.db]
        else:
            client = MongoClient(self.ip, self.port)
            return client[self.db]
    def conn_collect(self,collect=None):

        dbs=self._conn_db()
        if collect:
            collects=dbs[collect]
        else:
            collects=dbs[self.collect]
        return  collects
class Connect_object(object):
    @staticmethod
    def connect(database=MONGODB_DB):
        connect_db = Mongodb_Connect(MONGODB_IP,int(MONGODB_PORT),db=database,username=MONGODB_USER,password=MONGODB_PWD,ssl=MONGODB_SSL)
        return connect_db

def device_id(device_name):
    connect_db = Connect_object.connect().conn_collect('Device')
    device_id = connect_db.find({'name':device_name},{'name':1})
    return ''.join([_id['_id'] for _id in device_id])

def retrieveDevice():
    print(id(Connect_object.connect()))
    connect_db=Connect_object.connect().conn_collect('Device')
    devices = connect_db.find({'subType':{'$in':[2,2001]}},{"name":1,'subType':1},limit=1000)
    return [[device.get('name'),device['subType']] for device in devices]

def getRole(rolename):
    connect_db=Connect_object.connect(database=MONGODB_SYS_DB).conn_collect('Role')
    roles = connect_db.find({'name':rolename},{'name':1,"permissions":1})
    return [(data['name'],data['permissions']) for data in roles]

def getConfiguration(device_name,type=None,subname=None):
    connect_db =Connect_object.connect().conn_collect('DeviceDataCurr')
    devId = device_id(device_name)
    configurations = connect_db.find({'devId':devId,'type':type,'subName':subname},{'content':1})
    return ''.join([config['content'] for config in configurations])
    # device_id= connect_db.finde({'name':})

def getbenchmarkTaskName(task_name):
    connect_db = Connect_object.connect().conn_collect('BenchmarkDefinition')
    task_item = connect_db.find({'name':task_name},{'name':1})
    task = [data for data in task_item]
    if len(task) >=1:
        return True
    else:
        return False

def getbenchmarkTaskStatus(task_name,status='Running'):
    connect_db =  Connect_object.connect().conn_collect('DeviceDataSource') 
    data_source = connect_db.find({'name':task_name},{'name':1,"status":1},limit = -1)
    if data_source.count() > 0:
        if data_source.next()['status'] == status:
            return True
        else:
            return False
        
def getTenantInfo(Tenant_Name):
    connect_db = Connect_object.connect(database=MONGODB_SYS_DB).conn_collect('Tenant')
    tenant_data = connect_db.find({'name':Tenant_Name},{'name':1,'description':1})
    if tenant_data:
        return [data for data in tenant_data]
    
def getDoaminInfo(Tenant_name,domain_name):
    connect_db = Connect_object.connect(database=MONGODB_SYS_DB).conn_collect('Tenant')
    domain_data = connect_db.find({'name':Tenant_name},{'name':1,'domains.name':1,'domains.guid':1})
    domains = [data for data in domain_data]
    if len(domains) > 0:
        for domain in domains[0]['domains']:
            if domain['name'] == domain_name:
                return True
    return False


def getNetworkServer(alias):
    connect_db = Connect_object.connect().conn_collect('NetworkServer')
    NS_data = connect_db.find({'alias':alias},{'ipOrHostname':1,'alias':1,'nsport':1})
    if NS_data.count() > 0:
        if NS_data.next()['alias'] == alias:
            return True
        else:
            return False
    else:
        return False
def getSSHPrivateKey(alias):
    connect_db = Connect_object.connect().conn_collect('SSHPrivateKey')
    key_data = connect_db.find({'alias':alias},{'alias':1})
    if key_data.count() > 0:
        if key_data.next()['alias'] == alias:
            return True
        else:
            return False
    else:
        return False


def getdomainId(Tenant_name,Domain_name=None):
    print(id(Connect_object.connect(database=MONGODB_SYS_DB)))
    connect_db = Connect_object.connect(database=MONGODB_SYS_DB).conn_collect('Tenant')
    print(connect_db)
    domain_data = connect_db.find({'name':Tenant_name},{'name':1,'domains.name':1,'domains.guid':1})
    print(domain_data)
    if domain_data.count():
        domains=domain_data.next()
        tenant_id = domains['_id']
        for domain in domains['domains']:
            if domain['name'] == Domain_name:
                return tenant_id,domain['guid']
            else:
                return 'funck'
    else:
        print('error.......')
def getUserId(user):
    print(id(Connect_object.connect(database=MONGODB_SYS_DB)))
    connect_db = Connect_object.connect(database=MONGODB_SYS_DB).conn_collect('User')
    users_data = connect_db.find({'name':user},{'name':1})
    if users_data.count() > 0:
        return users_data.next()['_id']
        
    else:
        return    

def getPolicy(user):
    tenant_id,domain_id = getdomainId(Config.TENANT,Config.DOMAIN)
    user_id = getUserId(user)
    connect_db = Connect_object.connect(database=MONGODB_SYS_DB).conn_collect('SecurityPolicy')
    policy_data = connect_db.find({'userId':user_id},{'tenantPolicies':1})
    if policy_data.count() >0:
        return policy_data.next()
    else:
        return 


def getUserforDomain(user):
    policy_data = getPolicy(user)
    tenant_id,domain_id = getdomainId(Config.TENANT,Config.DOMAIN)
    if policy_data:
        tenantPolicies = policy_data['tenantPolicies']
        for domains in  tenantPolicies:
            if domains['tenantId'] == tenant_id:
                for domain in domains['domainPolicies']:
                    if domain['domainId'] == domain_id:
                        return True
            else:
                return False
    else:
        return False    
def getUserforTenant(Tenant_name,user):
    policy_data = getPolicy(user)
    tenant_id,domain_id = getdomainId(Config.TENANT,Config.DOMAIN)
    if policy_data:
        tenantPolicies = policy_data['tenantPolicies']
        for domains in  tenantPolicies:
            if domains['tenantId'] == tenant_id:
                return True
            else:
                return False
    else:
        return False
def getproperty():
    pass
def getSiteTree(site_name):
    connect_db = Connect_object.connect().conn_collect('Site')
    site_data = connect_db.find({'name':site_name},{'name':1})
    if site_data.count() == 1:
        _id=site_data.next()['_id']
        site_number = Connect_object.connect().conn_collect('SiteMember').find({'siteId':_id},{"deviceName":1})
        if site_number.count() >=1:
            site_device = [device['deviceName'] for device in site_number]
            return site_device

    else:
        return "site does not find or site name duplicate.."
def getsnmpinfo(alias):
    connect_db = Connect_object.connect().conn_collect('SnmpRoInfo')
    snmp_info = connect_db.find({"alias":alias},{'alias':1})
    if snmp_info.count():
        return True
    else:
        return False   

def getallQapp():
    connect_db = Connect_object.connect(MONGODB_TENANT_DB).conn_collect('QappInfo')
    data =connect_db.find({},{'name':1})
    if data.count() > 0:
     
        return [qapp_name['name'] for qapp_name in data]
    else:
        return  

def getallParserCLI():
    connect_db = Connect_object.connect(MONGODB_TENANT_DB).conn_collect('Parsers')
    data = connect_db.find({},{'name':1,'command':1,'devTypes':1})
    if data.count() > 0:
        return [parser_cli for parser_cli in data] 
def deviceType(devType):
    connect_db = Connect_object.connect(MONGODB_TENANT_DB).conn_collect('DeviceType')
    data = connect_db.find({"_id":devType},{'typeName':1})
    if data.count() > 0:
        return  "".join([type_name['typeName'] for type_name in data])
if __name__ =="__main__":
    import csv
    parser_data = getallParserCLI()
    with open('D:\parser.csv',"w+",newline="",encoding='utf-8') as cvs_file:
        header=["Parser_name","Cli_Command","device_type","parser_type"]
        writer= csv.DictWriter(cvs_file,fieldnames=header,)
        writer.writeheader() 
        for parser in parser_data:
            device_type =";".join([deviceType(type_id) for type_id in parser['devTypes']])
            if "::" in parser['command']:
                row = {'Parser_name':parser['name'],'Cli_Command':'::Current Baseline<>','device_type':device_type,'parser_type':'Configuration Parser'}
                writer.writerow(row) 
            else:
                row = {'Parser_name':parser['name'],'Cli_Command':parser['command'],'device_type':device_type,'parser_type':'CLI Parser'}
                writer.writerow(row)      
    # import pprint

    # from pymongo import database
    # db = Mongodb_Connect(MONGODB_IP,int(MONGODB_PORT),db='BJ_Rack',username=MONGODB_USER,password=MONGODB_PWD,ssl=MONGODB_SSL)._conn_db()
    # print(isinstance(db,database.Database))
    # fs = gridfs.GridFS(db,'MapPage')
    # print(fs)
    # data = fs.get(ObjectId("5a011f441076661ec4e9381c")).read()
    # print(data)
    # retrieveDevice()
    # print(getdomainId('Initial Tenant','Bj_rack'))
    # pprint.pprint(getUserId('cEeqky'))
    # pprint.pprint(getPolicy('wangzheng'))
    # pprint.pprint(getSiteTree('SITESSAWWQQ'))