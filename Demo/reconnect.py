import sys,time,pyldap,pyldap.ldapobject,ldapurl

from pyldap.ldapobject import *

ldap_url = ldapurl.LDAPUrl(sys.argv[1])
ldap_url.applyDefaults({
  'who':'',
  'cred':'',
  'filterstr':'(objectClass=*)',
  'scope':pyldap.SCOPE_BASE
})

pyldap.trace_level=1

l = pyldap.ldapobject.ReconnectLDAPObject(
  ldap_url.initializeUrl(),trace_level=pyldap.trace_level
)
l.protocol_version = pyldap.VERSION3

l.simple_bind_s(ldap_url.who,ldap_url.cred)

while 1:
  l.search_s(ldap_url.dn,ldap_url.scope,ldap_url.filterstr,ldap_url.attrs)
  sys.stdin.readline()
