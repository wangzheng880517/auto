import requests
import ssl
import urllib
import base64
import json
import time
import pprint
import string
import os
import configparser
import requests.packages.urllib3 as urllib3
import random
from ConfigSetting import Config

urllib3.disable_warnings()
headers = {"Content-Type": "application/json",
           "Accept": "application/json", 'Accept-Encoding': 'gzip'}
Host_url = Config.HOST_URL
user = Config.USER
pwd = Config.PASSWORD
TENANT = Config.TENANT
DOMAIN = Config.DOMAIN
POST = 'post'
GET = 'get'
DELETE = 'delete'
# Need to install requests package for python
# pip install requests


class SourceofTurthAPI(object):
    def __init__(self, user, password, url, tenant, domain, headers=None):

        self.user = user
        self.password = password
        self.url = url
        self.tenant = tenant
        self.domain = domain
        self.headers = self. _headers()

    def _getToken(self):
        login_url = 'API/login'
        full_url = self.url + login_url
        # basic_data = self.user + ":" + self.password
        # # basic_data = basic_data.encode("ascii")
        # auth_data = base64.b64encode(basic_data.encode('utf-8'))
        # headers2 = {"Authorization": "Basic " + auth_data.decode(),
        #             "Content-Type": "application/json", "Accept": "application/json"}
        tokens = requests.post(full_url, headers=headers, auth =(user,pwd),verify=False)
        print(tokens.json())
        if "token" in tokens.json():
            return tokens.json()["token"]
        else:
            return "Token ERROR:" + " " + str(tokens.json())
    def _random_str(self):
        return "".join(random.sample(string.ascii_letters,6))
    def _headers(self):
        headers = {"Content-Type": "application/json",
                   "Accept": "application/json",
                #    'Content-Encoding':'gzip'
                }
        token = self._getToken()
        headers['Token'] = token
        return headers
    

    def _requestInstant(self, method, api_url, body=None, headers=None):
        # __headers = self._headers()
        main_url = self.url + api_url
        if str(method).lower() == "get":
            if body and isinstance(body, dict):
                result = requests.get(
                    main_url, params=body, headers=self.headers, verify=False)
            else:
                result = requests.get(
                    main_url, headers=self.headers, verify=False)
            if result.status_code == 200:
                return result.json()
            else:
                return "request error:\r\n%s" % (str(result.status_code) + "->" + main_url)
        elif str(method).lower() == "post" and isinstance(body, dict):
            result = requests.post(main_url, data=json.dumps(
                body), headers=self.headers, verify=False)
            if result.status_code == 200:
                return result.json()
            else:

                return "request error:\r\n%s" % (str(result.status_code) + "->" + main_url)

        elif str(method).lower() == "delete" and isinstance(body, dict):
            result = requests.delete(main_url, data=json.dumps(
                body), headers=self.headers, verify=False)
            if result.status_code == 200:
                return result.json()
            else:
                return "request error:\r\n%s" % (str(result.status_code) + "->" + main_url)

        else:
            return "Token is None"
    def Logout(self,token):
        logout_url = "API/logout"
        data ={
            'token':token
        }
        return self._requestInstant("POST",logout_url,data)

    def setCrruentDomain(self,tenant=None,domain=None):
        set_crruent_domain_url = 'API/setCurrentDomain'
        if tenant==None and domain==None:
            data = {
                "tenantName": self.tenant,
                "domainName": self.domain
            }
        else:
            data = {
                "tenantName":tenant,
                "domainName":domain
            }
        return self._requestInstant(POST, set_crruent_domain_url, data)

    def addRole(self, **kwarg):
        '''
        ["domainManagement",
        "sharePolicyManagement",
        "deviceManagement",
        "sharedDeviceLinkGroupManagement",
        "siteManagement",
        "discoverTuneNetworkDevice",
        "scheduleBenchmark",
        "globalDataFolderSnapshotManagement",
        "manageNetworkSettings"
        "manageDeviceSettings"
        "accessToLiveNetwork"
        "changeManagement"
        ]

        '''
        add_role_url = r'API/CMDB/role/addRole'
        data = {
            'roleName': None,
            'description': 'This is a API test...',
            'privileges': []
        }
        for k, v in kwarg.items():
            data[k] = v
        return self._requestInstant(POST, add_role_url, data)

    def EditRole(self, **kwarg):
        edit_role_url = r'API/CMDB/role/editRole'
        data = {
            'newRoleName': None,
            'roleName': None,
            'description': "edit role api test",
            'provileges': []

        }

        for k, v in kwarg.items():
            data[k] = v

        return self._requestInstant(POST, edit_role_url, data)

    def deleteRole(self, roleName):
        delete_role_url = r'API/CMDB/role/deleteRole'
        data = {
            'roleName': roleName
        }
        return self._requestInstant(DELETE, delete_role_url, data)

    def addtenant(self, **kwarg):
        '''
         add tenant api function..
        '''
        add_tenant_url = 'API/CMDB/tenant/addTenant'
        data = {
            'tenantName': None,
            'description': None,
            'maximumNodes': None,
            'advancedOptions':
            {
                'tenantConnSetting': {
                    'replicaSet': None,
                    'servers': None,
                    'user': None,
                    'password': None
                }
            },
            'liveDataConnSetting': {
                'replicaSet': None,
                'servers': None,
                'user': None,
                'password': None
            }
        }
        for k, v in kwarg.items():
            data[k] = v
        return self._requestInstant(POST, add_tenant_url, data)

    def edittenant(self, **kwarg):
        """
         edit tenant API fucntion..
        """
        edit_tenant_url = 'API/CMDB/tenant/editTenant'
        data = {
            'newTenantName': None,
            'tenantName': None,
            'description': None,
            'maximumNodes': None,
        }
        for k, v in kwarg.items():
            data[k] = v
        return self._requestInstant(POST, edit_tenant_url, data)

    def deletetenant(self, tenant_name):
        '''
            delete tenant API function
        '''
        delete_tenant_url = 'API/CMDB/tenant/deleteTenant'
        data = {
            'tenantName': tenant_name
        }
        return self._requestInstant(DELETE, delete_tenant_url, data)

    def assignUserForTenant(self, **kwarg):
        # self.setCrruentDomain()
        '''
         assignUserForTenant api function...
        '''
        asg_user_tenant_url = r'API/CMDB/tenant/assignUsersForTenant'
        data = {
            'tenantName': None,
            'users': [
                {
                    # userName:xx,
                    # isTenantAdmin:xx
                }
            ]
        }
        for k, value in kwarg.items():
            data[k] = value
        return self._requestInstant(POST, asg_user_tenant_url, data)

    def createDomain(self, **kwarg):
        '''
        create domain API function....
        '''
        create_domain_url = 'API/CMDB/domain/createDomain'
        data = {
            'tenantName': self.tenant,
            'domainName': None,
            'maximumNodes': None,
            'description': 'This is a test for creating domain'

        }
        for k, value in kwarg.items():
            data[k] = value
        return self._requestInstant(POST, create_domain_url, data)

    def editDomain(self, **kwarg):
        edit_domain_url = 'API/CMDB/domain/editDomain'
        data = {
            'tenantName': self.tenant,
            'newDomainName': None,
            'domainName': None,
            'maximumNodes': None,
            'description': None
        }
        for k, value in kwarg.items():
            data[k] = value
        return self._requestInstant(POST, edit_domain_url, data)

    def deleteDomain(self, **kwarg):
        delete_domain_url = 'API/CMDB/domain/deleteDomain'
        data = {
            'tenantName': self.tenant,
            'domainName': None
        }
        for k, value in kwarg.items():
            data[k] = value
        return self._requestInstant(DELETE, delete_domain_url, data)

    def AssignUserForDomain(self, **kwarg):
        # self.setCrruentDomain()
        assign_user_for_domain_url = 'API/CMDB/domain/assignUsersForDomain'
        data = {
            'tenantName': self.tenant,
            'domainName': None,
            'users': [
                #{userName:xxx,roles:[xx,xx]}
            ]

        }
        for k, value in kwarg.items():
            data[k] = value
        return self._requestInstant(POST, assign_user_for_domain_url, data)

    def removeUsersForDomain(self, **kwarg):
        # self.setCrruentDomain()
        remove_user_for_domain_url = r'API/CMDB/domain/removeUsersFromDomain'
        data = {
            'tenantName': self.tenant,
            'domainName': None,
            'users': []
        }
        for k, value in kwarg.items():
            data[k] = value
        return self._requestInstant(DELETE, remove_user_for_domain_url, data)
    def DiscoveryIPNow(self,**kwarg):
        discovery_ip_now_url = 'API/CMDB/discovery/discoverIPNow'
        data={
            "mgmtIPs":None,# ip type is list;e.g mgmtIPs=['15.0.0.1',15.0.0.2]
            'cliType':None,#Telnet or SSH
            'username':None,
            'password':None,
            'privilegeUsername':None,
            'privilegePassword':None,
            'snmpCommunity':None,
            'proxyServerAlias':None
        }

        for key,value in kwarg.items():
            data[key] = value 
        result = self._requestInstant(POST,discovery_ip_now_url,data)
        if isinstance(result,dict) and "taskId" in result.keys():
            return result.get("taskId")
        else:
            return None 


    def GetDiscoveryIPResult(self,**kwarg):
        '''
        This API should use 'GET' method for http to get data, 
        but it use 'POST' method for http now.
        Scrum Team  will fix the bug after Chinese New Year 
        '''
        task_id = self.DiscoveryIPNow(**kwarg)
        if task_id:
            discovery_ip_result_url =r"API/CMDB/discovery/CheckDiscoveryStatus/"
            full_url = discovery_ip_result_url + task_id
            result = self._requestInstant(GET, full_url)
            if isinstance(result,dict) and 'completed' in result.keys():
                completed = False
                while completed==False:
                    time.sleep(5)
                    result = self._requestInstant(GET, full_url)
                    if isinstance(result,dict):
                        completed = result["completed"]
                    else:
                        print("result return error:%s"%result)
                    print("Executing,please wait...")
                print('Execute discovery finish.....')
                return result
            else:
                return "result error...."
    def addNetworkSetting(self, data,tenant=None,domain=None):
        self.setCrruentDomain(tenant,domain)
        add_network_set_url = r'API/CMDB/networkSettings/addNetworkSetting'
        '''
           proxyServer = {
          'networkServer': {
            'alias':'xxxx',
            'ipOrHostName':'192.168.1.23',
            'nsPort':9099,
            'timeOut': 2,
            'encryptionKey': 'netbrain12345'
            },    

        'privateKey':
        {
            'alias':'xxx',
            'keyName':'xxa.pa',
            'keyContent':"No speaking to fuck ",
            'md5KeyContent':'xxxxxx',
            'passphrase':'xxxxx'
        },
        'jumpBox':{
            'alias': 'None1',  # //必填项
            'ipAddr':'192.168.1.1',  # //必填项
            'mode':None,  # 必填项 2->SSH Public 1-> ssh 0->telnet
            'port':22,    # 必填项
            'userName': 'netbrain',  # 非必填项
            'privateKey': 'nopass',  # 如果mode是SSH Publice Key则此项必填
            'password': 'netbrain',  # 非必填项
            'loginPrompt': 'Login:',  # 非必填项
            'passwordPrompt': 'Password:',  # 非必填项
            'yesNoPrompt': '(yes/no)?',  # 非必填项
            'commandPrompt': 'cli command',  # 非必填项
    },
        'telnetInfo':{
            'alias':'xxaww',
            'userName':'telnetbrain@#$%^&*()',
            'password':"QWERTTTWWWACVVGGADSS",
            'cliMode':2,
            'sshKeyID':'nopass'
        },
        'privilegeInfo':{
            'alias':'xxxx',
            'userName':"previleges",
            'password':"netbrain@233"
        },
        'snmpInfo':{
            'alias':"sn11",
            'snmpVersion':3,
            'roString':"netbrain",
            'v3':{
                'userName':"snmpV3",
                'contextName':"xxxx",
                'authMode':11,
                'authPro':2,
                'encryptPro':3,
                'authPassword':'netbrain',
                'encryptPassword':'admin'


            }
          }
    }
        '''
        return self._requestInstant(POST,add_network_set_url,data)

    def deleteNetworkSetting(self,data):
        self.setCrruentDomain()
        del_network_set_url = r'API/CMDB/networkSettings/deleteNetworkSetting'
        return self._requestInstant(DELETE,del_network_set_url,data)

    def getDeviceData(self,**kwarg):
        # header1 = {"Content-Type": "application/json",
        #            "Accept": "application/json",
        #         #    'Accept-Encoding':'gzip, deflate'
        #         }
        self.setCrruentDomain()
        get_device_data_url = r'API/CMDB/device/getDeviceData'
        data = {
            'hostname':None,
            'dataType':None,#require, support the following types: “ConfigurationFile”,“RouteTable”, “MACTable”,”ARPTable”, “NDPTable”,”STPTable”,”BGPAdvertised-routeTable”,”NCTTable”. should ignore letter case.
            'vrf': None,# //optional, only valid for route, arp, or bgp table type, when not specified, return the global vrf content.
            'nctName': None,# // required by nct table, ignored by other type
            'subName':None# //optional, only valid for nct table
        }
        for k , value  in kwarg.items():
            data[k] = value
        return self._requestInstant(GET,get_device_data_url,data)
        
        # return self._requestInstant(GET,get_device_data_url,data,headers=header1)
    def addBenchmarkTask(self,tenant=None,domain=None,**kwarg):
        self.setCrruentDomain(tenant,domain)
        data ={
            'taskName':None,
            'description':"xxxxx",
            'startDate':'2017/7/10',
            'endDate': None,
            'schedule':{
                'frequency':'weekly',
                'startTime':['2017/7/11 16:20:20'],
                'interval':1,
                'weekday':[1,3,5],
                # 'dayOfMonth':None,
                # 'months':[1,2,3,4,5]

            },
            'deviceScope':{
                'scopeType':'all',
                'scopes':None,
               
            },
            'retrieveData':["BGP Neighbors",
            #                 "BGP VPNv4 Neighbors",
            #                 "EIGRP Neighbors",
            #                 "MPLS TE",
            #                 "IPsec VPN Table",
            #                 "IPsec VPN Table[Real-time]",
            #                 "IPv6 Route Table",
            #                 "IS-IS Neighbors",
            #                 "Interface Information Brief",
            #                 "Fabricpath Route Table",
            #                 "LDP Neighbors",
            #                 "MPLS LFIB",
            #                 "MPLS VPNv4 Label",
            #                 "OSPF Neighbors",
            #                 "MPLS VRF",
            #                 "Multicast Route Table",
            #                 "NAT Table",
            #                 "NAT Table[Real-time]",
            #                 "NetFlow",
            #                 "PIM Neighbors",
            #                 "Virtual Server Table",
            #                 "Zone Table",
            #                 "Cisco Nexus VDC",
                            'config',
                            'routingtable',
                            'arptable',
                            'mactable',
                            'cdptable',
                            'stptable',
                            'bgpnbr',
                            'inventoryinfo'

                            ],
            'limitRunMins':20,
            'cliCommands':['show interface','show ip interface','show version','show ip ospf interface'],
            'isBuildIPv4L3Topo': True, #optional
            'isBuildIPv6L3Topo': True, #optional
            'isBuildL2Topo': True, #optional
            'IsBuildVPNTopo':True,
            'isRecalculateDynamicDeviceGroups': True, #optional
            'isRecalculateSite': True, #optional
            'isRecalculateMPLSVirtualRouteTables': True, #optional
            'isbuildDefaultDeviceDataView': True, #optional
            'isEnable': True #optional, the default value is true

        }
        add_benchmark_task_url = r'API/CMDB/benchmark/addBenchmarkTask'
        for k, value in kwarg.items():
            data[k] =  value
        return self._requestInstant(POST,add_benchmark_task_url,data)
    def editBenchmarkTask(self,**kwarg):
        self.setCrruentDomain()
        edit_beachmark_task_url ='API/CMDB/benchmark/editBenchmarkTask'
        return self._requestInstant(POST,edit_beachmark_task_url,kwarg)
    def deleteBenchmarkTask(self,taskName):
        self.setCrruentDomain()
        delete_bmt_url = 'API/CMDB/benchmark/deleteBenchmarkTask'
        data = {
            'taskName':taskName,
            'isDeletedDataFolders':None
        } 
        return self._requestInstant(DELETE,delete_bmt_url,data)

    def runBenchmarkTaskNow(self,taskName,tenant=None,domain=None):
        self.setCrruentDomain(tenant,domain)
        run_bmt_url = 'API/CMDB/benchmark/runBenchmarkTaskNow'
        data = {
            'taskName':taskName
        }
        return self._requestInstant(POST,run_bmt_url,data)

    def GetDeviceNbrs(self,**kwarg):
        self.setCrruentDomain()
        get_dev_nbr_url = r'API/CMDB/neighbor/getDeviceNbrs'
        data = {
            'hostname':None,
            'topoType':None,
        }
        for k,value in kwarg.items():
            data[k] = value 
        return self._requestInstant(GET,get_dev_nbr_url,data)

    def getConenctedSwitchPort(self,ip):
        self.setCrruentDomain()
        get_conn_switch_port_url = r'API/CMDB/site/getConnectedSwitchPort'
        data ={
            'ip':ip
        }
        return self._requestInstant(GET,get_conn_switch_port_url,data)

    def deleteMap(self,url):
        self.setCrruentDomain()
        delete_map_url = r'API/CMDB/map/deleteMap'
        data = {
            'url':url
        }
        return self._requestInstant(DELETE,delete_map_url,data)
    def ExportMap(self,**kwarg):
        self.setCrruentDomain()
        export_map_url = r'API/CMDB/map/exportMap'
        data = {
            'url':None,
            'format':None,#xmap,visio
            'pages':[],
            #/optional, only for visio format, not valid for qmap format,
            # qmap must be full map, the export file can be import later. 
            # this will not be supported in this version unless the requirement changed.
        }
        for k,value in kwarg.items():
            data[k] = value
        return self._requestInstant(POST,export_map_url,data)

    def ImportSiteTree(self,path,devices,iscontainer=False):
        self.setCrruentDomain()
        import_Site_Tree = r'API/CMDB/site/importSiteTree'
        if isinstance(devices,list):
            data = {
                'sites':
                [
                    {
                        'fullPath':path,
                        'isContainer':iscontainer,
                        'devices':devices,
                        #'this will not be supported in this version unless the requirement changed.'
                    }
                ]
            }
            return self._requestInstant(POST,import_Site_Tree,data)
        else:
            return 'device paramter must be a list type....'



def testGetDevicedata():
    Test_API = SourceofTurthAPI(
        'admin', 'admin', 'https://10.10.4.214/ServicesAPI/', 'ZLH-Tenant', 'ZLH-Domain')

    dataTypes=[ 'ConfigurationFile','RouteTable', 'MACTable','ARPTable', 'NDPTable','STPTable','BGPAdvertised-routeTable','NCTTable']
    with open('D://2.txt','w') as ff:
        for data in dataTypes:
            if data == 'NCTTable':
                ff.write('NCTTable'+"data============================================\n")
                result = Test_API.getDeviceData(hostname='MPLS_PE1',dataType=data,nctName='BGP Neighbors')
                print(result)
                # ff.write(result['content'].replace('\r\n','\n'))
                ff.write('NCTTable'+"data============================================\n")
            else:
                ff.write(str(data)+"data============================================\n")
                result = Test_API.getDeviceData(hostname='MPLS_PE1',dataType=data)
                print(result)
                ff.write(str(data)+"data============================================\n")
                if isinstance(result,dict) and result.get('content'):
                    ff.write(str(data)+"data============================================")
                    ff.write(result['content'].replace('\r\n','\n'))
                    ff.write('=============================\r\n')
                else:
                    ff.write(str(data)+'other error......\n')


                    ff.write(str(result))

API_init = SourceofTurthAPI(user,pwd,Host_url,TENANT,DOMAIN)                 
          
def objects():
    # global API_init
    
    return API_init
if __name__ == '__main__':
    print('----------------------------------')
    import time
    start = time.time()
    # testGetDevicedata()
    # end = time.time()
    # print('execute time:%s'%(str(end-start)))end = time.time()
    # print('execute time:%s'%(str(end-start)))
    
    Test_API = SourceofTurthAPI(
        'admin', 'admin', 'https://10.10.5.187/ServicesAPI/', 'Initial Tenant', 'Bj_rack')
    # print(Test_API.runBenchmarkTaskNow("System Data view Benchmark"))
    # print(Test_API.addRole(roleName="test1",privileges=['ScheduleBenchmark']))
    # print(Test_API.addtenant(tenantName="xxxx"))
    # print(Test_API.addBenchmarkTask(taskName='ipsecVpn'))
    # print(Test_API.createDomain(domainName='xxxx',maximumNodes=1))
    # data=Test_API.GetDeviceNbrs(hostname='MPLS_PE1',topoType='L2_Topo_Type')
    # print(data)
    # data =  {
    #             'tenantConnSetting': {
    #                 'replicaSet': None,
    #                 'servers': ['10.10.4.213:27018'],
    #                 'user': 'mongodb2',
    #                 'password': 'mongodb2'
    #             },
            
    #         'liveDataConnSetting': {
    #             'replicaSet': None,
    #             'servers': ['10.10.4.213:27018'],
    #             'user': 'mongodb2',
    #             'password': 'mongodb2'
    #         }
    # }
    # print(Test_API.addtenant(tenantName='fuckk22ck2kkc',description='sssaww',maximumNodes=23,advancedOptions=data))
    # print(Test_API.GetDeviceNbrs(hostname ='Mimic-IPv6-WAN-02',topotype='Ipv4_L3_Topo_Type'))
    # print(Test_API.getConenctedSwitchPort(ip=None))
    

    map_url = 'https://10.10.5.187/map.html?t=86bf9609-f789-9f10-1655-b252dd159f80&d=16f429be-31f0-4e99-a97d-53c0b1039863&id=76962158-1561-9544-5430-3c48e2bf8f7e'

    # print(Test_API.deleteMap(map_url))
    # # map_url2 ='https://10.10.5.210/map.html?t=072a0e3e-813f-e66d-0f09-456e4280f83b&d=ef24796c-c973-4ac0-aa12-03e8f01ff8ec&id=4ae6e1b3-15a4-2edc-560b-2f389e4072f6'
    # print(Test_API.deleteMap(map_url2))
    def downloadMapforxmap():
        data = {
                'url':map_url,
                'format':'xmap',#xmap,visio
        }
        # print(Test_API.ExportMap(**data))
        map_data = Test_API.ExportMap(**data)
        print(map_data)
        with open('D:\map.xmap',"wb") as lines:
            lines.write(base64.b64decode(map_data['fileData']))
    downloadMapforxmap()
    # def downloadMapforvisio():
    #     data = {
    #             'url':map_url,
    #             'format':'visio',#xmap,visio
    #             'pages':['Page1','Page2']
    #     }
    #     # print(Test_API.ExportMap(**data))
    #     map_data = Test_API.ExportMap(**data)['fileData']
    #     print(map_data)
    #     with open('D:\map.vsdx',"wb") as lines:
    #         lines.write(base64.b64decode(map_data))

    # downloadMapforvisio()
    # # print(Test_API.deleteBenchmarkTask(taskName=None))
    # print(Test_API.addBenchmarkTask(taskName='tea22ss',startDate ='2017/7/11'))

    # benchmarkTask =['TestAPI11','TestAPI22','weekly','weel11y','ss','ns','eee','cccc' ]

    # for task in benchmarkTask:
    #     print(Test_API.runBenchmarkTaskNow(task))
    # # # data={
    #     'networkServer':{
    #         'alias':"xxxx"
    #     },
    #     'privatekey':{
    #         'alias':'xxx'
    #     },
    #     'jumpBox':{
    #         'alias':'None1'
    #     },
    #     'telnetInfo':{
    #         'alias':'xxaww'
    #     },
    #     'privilegeInfo':{
    #         'alias':"xxxx"
    #     },
    #     'snmpInfo':{
    #         'alias':'sn11'
    #     }
    # }
    # print(Test_API.deleteNetworkSetting(data))

    # priv = [
    #     "domainManagement",
    #     "sharePolicyManagement",
    #     "deviceManagement",
    #     "sharedDeviceLinkGroupManagement",
    #     "siteManagement",
    #     "discoverTuneNetworkDevice",
    #     "scheduleBenchmark",
    #     "globalDataFolderSnapshotManagement",
    #     "manageNetworkSettings",
    #     "manageDeviceSettings",
    #     "accessToLiveNetwork",
    #     "createNetworkChange",
    #     'executeNetworkChange',
    # # ]
    # proxyServer = {
    #       'networkServer': {
    #         'alias':'xxxx',
    #         'ipOrHostName':'192.168.1.23',
    #         'nsPort':9099,
    #         'timeOut': 2,
    #         'encryptionKey': 'netbrain12345'
    #         },    

    #     'privateKey':
    #     {
    #         'alias':'xxx',
    #         'keyName':'xxa.pa',
    #         'keyContent':"No speaking to fuck ",
    #         'md5KeyContent':'xxxxxx',
    #         'passphrase':'xxxxx'
    #     },
    #     'jumpBox':{
    #         'alias': 'None1',  # //必填项
    #         'ipAddr':'192.168.1.1',  # //必填项
    #         'mode':None,  # 必填项 2->SSH Public 1-> ssh 0->telnet
    #         'port':22,    # 必填项
    #         'userName':"netbrain",
    #         'keyName': '111',  # 非必填项
    #         # 'privateKey': '111',  # 如果mode是SSH Publice Key则此项必填
    #         'password': 'netbrain',  # 非必填项
    #         'loginPrompt': 'Login:',  # 非必填项
    #         'passwordPrompt': 'Password:',  # 非必填项
    #         'yesNoPrompt': '(yes/no)?',  # 非必填项
    #         'commandPrompt': 'cli command',  # 非必填项
    #     }
    # }
    # },
    #     'telnetInfo':{
    #         'alias':'xxaww',
    #         'userName':'telnetbrain@#$%^&*()',
    #         'password':"QWERTTTWWWACVVGGADSS",
    #         'cliMode':2,
    #         'sshKeyID':'nopass'
    #     },
        # 'privilegeInfo':{
        #     'alias':'xxxx',
        #     'userName':"previleges",
        #     'password':"netbrain@233"
        # },
    #     'snmpInfo':{
    #         'alias':"sn11",
    #         'snmpVersion':3,
    #         'roString':"netbrain",
    #         'v3':{
    #             'userName':"snmpV3",
    #             'contextName':"xxxx",
    #             'authMode':None,
    #             'authPro':2,
    #             'encryptPro':3,
    #             'authPassword':'netbrain',
    #             'encryptPassword':'admin'


    #         }
    #       }
    # }
    # print(Test_API.addNetworkSetting(proxyServer))

    # print(Test_API.removeUsersForDomain(domainName='Discover',users=['admin','zheng']))
    # data = [random.randint(0, len(priv)-1) for i in range(3)]
    # print(data)
    # print(Test_API.addRole(roleName=None,privileges=priv))
    # edit_role = Test_API.editRole(
    #     newRoleName='test_new111123', roleName='test_new1', privileges=[priv[i] for i in data])
    # print(edit_role)
    # print(Test_API.deleteRole('test_new2'))
    # print(add_role)
    # advanceOption = {'tenantConnsetting': {'replicaSet': 'xxxx', 'servers': [
    #     '10.10.5.190'], 'user': 'admin', 'password': 'xxxx'}}
    # addTenant = Test_API.addtenant(tenantName='te221', description='000', maximumNodes=-1)
    # print(addTenant)
    # print(Test_API.deletetenant(tenant_name = None))
    # print(Test_API.edittenant(newTenantName = 'func',tenantName ='test',description = 'edit tenant',maximumNodes = 2000))
    # print(Test_API.edittenant(newTenantName = 'func1',tenantName ='xxx',description = 'edit tenant',maximumNodes = 2000000))
    # user=[
    #     {
    #         'userName':'zheng',

    #         'isTenantAdmin':True
    #     },
    #     {
    #         'userName':'liuchao',
    #         'isTenantAdmin':False
    #     },
    #      {
    #         'userName':'admin',
    #         'isTenantAdmin':False
    #     }
    # ]
    # print(Test_API.assignUserForTenant(tenantName='xxx',users=user))
    # print(Test_API.assignUserForTenant(users=user))
    # print(Test_API.createDomain(domainName='zheng',description='this is a test auto for single source of truth api',maximumNodes = 200))
    # print(Test_API.editDomain(newDomainName='ccc',domainName="fuckss",maximumNodes=20))
    # print(Test_API.deleteDomain(tenantName=None,domainName = 'BJ_Rack'))
    # print(Test_API.AssignUserForDomain(domainName='BJ_Rack',users=[{'userName':'zhaoxu','roles':['Power User','Guest','domainAdmin','Engineer','QA','Network Change creator','ljl-tt']},{
    #     'userName':'wang','roles':['Engineer','domainAdmin']
    # }]))
    # print(Test_API.AssignUserForDomain(domainName='BJ_Rack',users=[]))
    print(Test_API.ImportSiteTree(path ="site1/SITESSAWWQQ",devices=['MPLS_PE1',"MPLS_CE1"],iscontainer=False))