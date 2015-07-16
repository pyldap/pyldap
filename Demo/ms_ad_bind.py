# How to bind to MS AD with python-ldap and various methods

import pyldap,pyldap.sasl

ldap_uri = "ldap://dc1.example.com"
dn = "CN=Anna Blume,CN=Users,DC=addomain,DC=example,DC=com"
sAMAccountName = "ABlume"
userPrincipalName = "ablume@addomain.example.com"
password = 'testsecret'

trace_level = 2

l = pyldap.initialize(ldap_uri,trace_level=trace_level)

# Normal LDAPv3 compliant simple bind
l.simple_bind_s(dn,password)

# This is AD-specific and not LDAPv3 compliant
l.simple_bind_s(userPrincipalName,password)

# This is AD-specific and not LDAPv3 compliant
l.simple_bind_s(userPrincipalName,password)

# SASL bind with mech DIGEST-MD5 with sAMAccountName as SASL user name
sasl_auth = pyldap.sasl.sasl(
  {
    pyldap.sasl.CB_AUTHNAME:sAMAccountName,
    pyldap.sasl.CB_PASS    :password,
  },
  'DIGEST-MD5'
)
l.sasl_interactive_bind_s("", sasl_auth)

# SASL bind with mech GSSAPI
# with the help of Kerberos V TGT obtained before with command
# kinit ablume@ADDOMAIN.EXAMPLE.COM
sasl_auth = pyldap.sasl.sasl({},'GSSAPI')
l.sasl_interactive_bind_s("", sasl_auth)
