import requests
import unittest
import sys
import os
import string 
from API.NewSourceofTurthAPI import objects
import random
import hashlib

class BaseClass(unittest.TestCase):

 
    def API_objects(self):
        return objects()


    def random_str(self,n=8):
        return "".join(random.sample(string.ascii_letters,n))

    def _hash_md5(self,data1,data2):
        md5_hash1 = hashlib.md5(bytes(data1,encoding='utf-8'))
        md5_hash2 = hashlib.md5(bytes(data2,encoding='utf-8'))
        if md5_hash1.hexdigest() == md5_hash2.hexdigest():
            return True
        else:
            return False

    def common_assert(self, result):
        self.assertIsInstance(result, dict, msg=result)
        self.assertEqual(result['statusCode'], 0, msg=result)
        print('xxxxxx')



