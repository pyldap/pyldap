from __future__ import print_function

import pyldap

host="localhost:1390"

print("API info:",pyldap.get_option(pyldap.OPT_API_INFO))
print("debug level:",pyldap.get_option(pyldap.OPT_DEBUG_LEVEL))
#print("Setting debug level to 255...")
#pyldap.set_option(pyldap.OPT_DEBUG_LEVEL,255)
#print("debug level:",pyldap.get_option(pyldap.OPT_DEBUG_LEVEL))
print("default size limit:",pyldap.get_option(pyldap.OPT_SIZELIMIT))
print("Setting default size limit to 10...")
pyldap.set_option(pyldap.OPT_SIZELIMIT,10)
print("default size limit:",pyldap.get_option(pyldap.OPT_SIZELIMIT))
print("Creating connection to",host,"...")
l=pyldap.init(host)
print("size limit:",l.get_option(pyldap.OPT_SIZELIMIT))
print("Setting connection size limit to 20...")
l.set_option(pyldap.OPT_SIZELIMIT,20)
print("size limit:",l.get_option(pyldap.OPT_SIZELIMIT))
#print("Setting time limit to 60 secs...")
l.set_option(pyldap.OPT_TIMELIMIT,60)
#print("time limit:",l.get_option(pyldap.OPT_TIMELIMIT))
print("Binding...")
l.simple_bind_s("","")




