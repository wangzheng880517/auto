import os
import importlib
dirs = os.path.dirname(__file__)
__all__ = []
for file_data in os.listdir(dirs):
    if 'test' in str(file_data).lower():
        modules = file_data.split(".")[0]
        name = 'TestCase.{0}'.format(modules)
        __all__.append(importlib.import_module(name))




# from NewSourceofTurthAPI import objects
