# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from ldap.compat import quote

import ldapurl
from ldapurl import LDAPUrl


class MyLDAPUrl(LDAPUrl):
    attr2extype = {
        'who':'bindname',
        'cred':'X-BINDPW',
        'start_tls':'startTLS',
        'trace_level':'trace',
    }


class TestLDAPUrl(unittest.TestCase):

    def assertNone(self, expr, msg=None):
        self.assertFalse(expr is not None, msg or ("%r" % expr))

    def test_combo(self):
        u = MyLDAPUrl(
            "ldap://127.0.0.1:1234/dc=example,dc=com"
            + "?attr1,attr2,attr3"
            + "?sub"
            + "?" + quote("(objectClass=*)")
            + "?bindname=" + quote("cn=d,c=au")
            + ",X-BINDPW=" + quote("???")
            + ",trace=8"
        )
        self.assertEqual(u.urlscheme, "ldap")
        self.assertEqual(u.hostport, "127.0.0.1:1234")
        self.assertEqual(u.dn, "dc=example,dc=com")
        self.assertEqual(u.attrs, ["attr1","attr2","attr3"])
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_SUBTREE)
        self.assertEqual(u.filterstr, "(objectClass=*)")
        self.assertEqual(len(u.extensions), 3)
        self.assertEqual(u.who, "cn=d,c=au")
        self.assertEqual(u.cred, "???")
        self.assertEqual(u.trace_level, "8")

    def test_parse_default_hostport(self):
        u = LDAPUrl("ldap://")
        self.assertEqual(u.urlscheme, "ldap")
        self.assertEqual(u.hostport, "")

    def test_parse_empty_dn(self):
        u = LDAPUrl("ldap://")
        self.assertEqual(u.dn, "")
        u = LDAPUrl("ldap:///")
        self.assertEqual(u.dn, "")
        u = LDAPUrl("ldap:///?")
        self.assertEqual(u.dn, "")

    def test_parse_default_attrs(self):
        u = LDAPUrl("ldap://")
        self.assertNone(u.attrs)

    def test_parse_default_scope(self):
        u = LDAPUrl("ldap://")
        self.assertNone(u.scope)     # RFC4516 s3

    def test_parse_default_filter(self):
        u = LDAPUrl("ldap://")
        self.assertNone(u.filterstr) # RFC4516 s3

    def test_parse_default_extensions(self):
        u = LDAPUrl("ldap://")
        self.assertEqual(len(u.extensions), 0)

    def test_parse_schemes(self):
        u = LDAPUrl("ldap://")
        self.assertEqual(u.urlscheme, "ldap")
        u = LDAPUrl("ldapi://")
        self.assertEqual(u.urlscheme, "ldapi")
        u = LDAPUrl("ldaps://")
        self.assertEqual(u.urlscheme, "ldaps")

    def test_parse_hostport(self):
        u = LDAPUrl("ldap://a")
        self.assertEqual(u.hostport, "a")
        u = LDAPUrl("ldap://a.b")
        self.assertEqual(u.hostport, "a.b")
        u = LDAPUrl("ldap://a.")
        self.assertEqual(u.hostport, "a.")
        u = LDAPUrl("ldap://%61%62:%32/")
        self.assertEqual(u.hostport, "ab:2")
        u = LDAPUrl("ldap://[::1]/")
        self.assertEqual(u.hostport, "[::1]")
        u = LDAPUrl("ldap://[::1]")
        self.assertEqual(u.hostport, "[::1]")
        u = LDAPUrl("ldap://[::1]:123/")
        self.assertEqual(u.hostport, "[::1]:123")
        u = LDAPUrl("ldap://[::1]:123")
        self.assertEqual(u.hostport, "[::1]:123")

    def test_parse_dn(self):
        u = LDAPUrl("ldap:///")
        self.assertEqual(u.dn, "")
        u = LDAPUrl("ldap:///dn=foo")
        self.assertEqual(u.dn, "dn=foo")
        u = LDAPUrl("ldap:///dn=foo%2cdc=bar")
        self.assertEqual(u.dn, "dn=foo,dc=bar")
        u = LDAPUrl("ldap:///dn=foo%20bar")
        self.assertEqual(u.dn, "dn=foo bar")
        u = LDAPUrl("ldap:///dn=foo%2fbar")
        self.assertEqual(u.dn, "dn=foo/bar")
        u = LDAPUrl("ldap:///dn=foo%2fbar?")
        self.assertEqual(u.dn, "dn=foo/bar")
        u = LDAPUrl("ldap:///dn=foo%3f?")
        self.assertEqual(u.dn, "dn=foo?")
        u = LDAPUrl("ldap:///dn=foo%3f")
        self.assertEqual(u.dn, "dn=foo?")
        u = LDAPUrl("ldap:///dn=str%c3%b6der.com")
        self.assertEqual(u.dn, "dn=str\xf6der.com")

    def test_parse_attrs(self):
        u = LDAPUrl("ldap:///?")
        self.assertEqual(u.attrs, None)
        u = LDAPUrl("ldap:///??")
        self.assertEqual(u.attrs, None)
        u = LDAPUrl("ldap:///?*?")
        self.assertEqual(u.attrs, ['*'])
        u = LDAPUrl("ldap:///?*,*?")
        self.assertEqual(u.attrs, ['*','*'])
        u = LDAPUrl("ldap:///?a")
        self.assertEqual(u.attrs, ['a'])
        u = LDAPUrl("ldap:///?%61")
        self.assertEqual(u.attrs, ['a'])
        u = LDAPUrl("ldap:///?a,b")
        self.assertEqual(u.attrs, ['a','b'])
        u = LDAPUrl("ldap:///?a%3fb")
        self.assertEqual(u.attrs, ['a?b'])

    def test_parse_scope_default(self):
        u = LDAPUrl("ldap:///??")
        self.assertNone(u.scope) # on opposite to RFC4516 s3 for referral chasing
        u = LDAPUrl("ldap:///???")
        self.assertNone(u.scope) # on opposite to RFC4516 s3 for referral chasing

    def test_parse_scope(self):
        u = LDAPUrl("ldap:///??sub")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_SUBTREE)
        u = LDAPUrl("ldap:///??sub?")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_SUBTREE)
        u = LDAPUrl("ldap:///??base")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_BASE)
        u = LDAPUrl("ldap:///??base?")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_BASE)
        u = LDAPUrl("ldap:///??one")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_ONELEVEL)
        u = LDAPUrl("ldap:///??one?")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_ONELEVEL)
        u = LDAPUrl("ldap:///??subordinates")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_SUBORDINATES)
        u = LDAPUrl("ldap:///??subordinates?")
        self.assertEqual(u.scope, ldapurl.LDAP_SCOPE_SUBORDINATES)

    def test_parse_filter(self):
        u = LDAPUrl("ldap:///???(cn=Bob)")
        self.assertEqual(u.filterstr, "(cn=Bob)")
        u = LDAPUrl("ldap:///???(cn=Bob)?")
        self.assertEqual(u.filterstr, "(cn=Bob)")
        u = LDAPUrl("ldap:///???(cn=Bob%20Smith)?")
        self.assertEqual(u.filterstr, "(cn=Bob Smith)")
        u = LDAPUrl("ldap:///???(cn=Bob/Smith)?")
        self.assertEqual(u.filterstr, "(cn=Bob/Smith)")
        u = LDAPUrl("ldap:///???(cn=Bob:Smith)?")
        self.assertEqual(u.filterstr, "(cn=Bob:Smith)")
        u = LDAPUrl("ldap:///???&(cn=Bob)(objectClass=user)?")
        self.assertEqual(u.filterstr, "&(cn=Bob)(objectClass=user)")
        u = LDAPUrl("ldap:///???|(cn=Bob)(objectClass=user)?")
        self.assertEqual(u.filterstr, "|(cn=Bob)(objectClass=user)")
        u = LDAPUrl("ldap:///???(cn=Q%3f)?")
        self.assertEqual(u.filterstr, "(cn=Q?)")
        u = LDAPUrl("ldap:///???(cn=Q%3f)")
        self.assertEqual(u.filterstr, "(cn=Q?)")
        u = LDAPUrl("ldap:///???(sn=Str%c3%b6der)") # (possibly bad?)
        self.assertEqual(u.filterstr, "(sn=Str\xf6der)")
        u = LDAPUrl("ldap:///???(sn=Str\\c3\\b6der)")
        self.assertEqual(u.filterstr, "(sn=Str\\c3\\b6der)") # (recommended)
        u = LDAPUrl("ldap:///???(cn=*\\2a*)")
        self.assertEqual(u.filterstr, "(cn=*\\2a*)")
        u = LDAPUrl("ldap:///???(cn=*%5c2a*)")
        self.assertEqual(u.filterstr, "(cn=*\\2a*)")

    def test_parse_extensions(self):
        u = LDAPUrl("ldap:///????")
        self.assertNone(u.extensions)
        self.assertNone(u.who)
        u = LDAPUrl("ldap:///????bindname=cn=root")
        self.assertEqual(len(u.extensions), 1)
        self.assertEqual(u.who, "cn=root")
        u = LDAPUrl("ldap:///????!bindname=cn=root")
        self.assertEqual(len(u.extensions), 1)
        self.assertEqual(u.who, "cn=root")
        u = LDAPUrl("ldap:///????bindname=%3f,X-BINDPW=%2c")
        self.assertEqual(len(u.extensions), 2)
        self.assertEqual(u.who, "?")
        self.assertEqual(u.cred, ",")

    def test_parse_extensions_nulls(self):
        u = LDAPUrl("ldap:///????bindname=%00name")
        self.assertEqual(u.who, "\0name")

    def test_parse_extensions_5questions(self):
        u = LDAPUrl("ldap:///????bindname=?")
        self.assertEqual(len(u.extensions), 1)
        self.assertEqual(u.who, "?")

    def test_parse_extensions_novalue(self):
        u = LDAPUrl("ldap:///????bindname")
        self.assertEqual(len(u.extensions), 1)
        self.assertNone(u.who)

    @unittest.expectedFailure
    def test_bad_urls(self):
        for bad in ("", "ldap:", "ldap:/", ":///", "://", "///", "//", "/",
                "ldap:///?????",       # extension can't start with '?'
                "LDAP://", "invalid://", "ldap:///??invalid",
                #XXX-- the following should raise exceptions!
                "ldap://:389/",         # [host [COLON port]]
                "ldap://a:/",           # [host [COLON port]]
                r"ldap://%%%/",          # invalid URL encoding
                "ldap:///?,",           # attrdesc *(COMMA attrdesc)
                "ldap:///?a,",          # attrdesc *(COMMA attrdesc)
                "ldap:///?,a",          # attrdesc *(COMMA attrdesc)
                "ldap:///?a,,b",        # attrdesc *(COMMA attrdesc)
                r"ldap://%00/",         # RFC4516 2.1
                r"ldap:///%00",         # RFC4516 2.1
                r"ldap:///?%00",        # RFC4516 2.1
                r"ldap:///??%00",       # RFC4516 2.1
                "ldap:///????0=0",      # extype must start with Alpha
                "ldap:///????a_b=0",    # extype contains only [-a-zA-Z0-9]
                "ldap:///????!!a=0",    # only one exclamation allowed
        ):
            try:
                LDAPUrl(bad)
            except ValueError:
                pass
            else:
                self.fail("should have raised ValueError: %r" % bad)

if __name__ == '__main__':
    unittest.main()
