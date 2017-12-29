from .BaseClass import BaseClass
from DB import mongodb_engine
class TestAddRole(BaseClass):
    _token = ""
    def setUp(self):
        global _token
        _token = ''
    
    def test_add_role_all_privilege_role(self):
        role_name = self.random_str()
        params = {
            'roleName': role_name,
            'description': 'This is a API test...',
            'privileges': ['domainManagement']
        }
        #add a role
        _token = self.API_objects()._getToken() 
    
        add_role = self.API_objects().addRole(**params)
        self.common_assert(add_role)
        #database find
        db_data = mongodb_engine.getRole(role_name)
        #result assert
        self.assertEqual(1,len(db_data))
        #delete assert 
        delete_role = self.API_objects().deleteRole(role_name)
        self.common_assert(delete_role)
        #database find and result assert 
        self.assertEqual(0,len(mongodb_engine.getRole(role_name)),msg="Delete role failed from database...")


    def test_add_role_some_privilege_role(self):
        pass
    
    def test_add_role_a_some_privilege_role(self):
        pass
    
    def test_add_role_use_non_admin_user(self):
        pass
    
    def test_add_role_special_char(self):
        pass
    
    def test_add_role_repeat_name(self):
        pass
    
    def test_add_role_name_is_none(self):
        pass
    
    def tearDown(self):
        global _token
        self.API_objects().Logout(_token)
    # @classmethod
    # def tearDownClass(cls):
        # cls().API_objects().Logout() 
        
