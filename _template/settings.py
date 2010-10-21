#Put your application settings that can be opensourced here

try:
    from local_settings import *
except ImportError:
    raise Exception("Please create a local_settings.py with your real settings in")
