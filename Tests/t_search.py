from __future__ import unicode_literals

import sys

if sys.version_info[0] <= 2:
    PY2 = True
    text_type = unicode
else:
    PY2 = False
    text_type = str

import os
import unittest
from slapdtest import SlapdTestCase

# Switch off processing .ldaprc or ldap.conf before importing _ldap
os.environ['LDAPNOINIT'] = '1'

import ldap
from ldap.ldapobject import LDAPObject

LDIF_TEMPLATE = """dn: cn=Foo1,%(suffix)s
objectClass: organizationalRole
cn: Foo1

dn: cn=Foo2,%(suffix)s
objectClass: organizationalRole
cn: Foo2

dn: cn=Foo3,%(suffix)s
objectClass: organizationalRole
cn: Foo3

dn: ou=Container,%(suffix)s
objectClass: organizationalUnit
ou: Container

dn: cn=Foo4,ou=Container,%(suffix)s
objectClass: organizationalRole
cn: Foo4

"""


class TestSearch(SlapdTestCase):

    ldap_object_class = LDAPObject

    @classmethod
    def setUpClass(cls):
        SlapdTestCase.setUpClass()
        # insert some Foo* objects via ldapadd
        cls.server.ldapadd(LDIF_TEMPLATE % {'suffix':cls.server.suffix})

    def setUp(self):
        try:
            self._ldap_conn
        except AttributeError:
            # open local LDAP connection
            self._ldap_conn = self._open_ldap_conn(bytes_mode=False)

    def test_reject_bytes_base(self):
        base = self.server.suffix
        l = self._ldap_conn

        with self.assertRaises(TypeError):
            l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, '(cn=Foo*)', ['*'])
        with self.assertRaises(TypeError):
            l.search_s(base, ldap.SCOPE_SUBTREE, b'(cn=Foo*)', ['*'])
        with self.assertRaises(TypeError):
            l.search_s(base, ldap.SCOPE_SUBTREE, '(cn=Foo*)', [b'*'])

    def test_search_keys_are_text(self):
        base = self.server.suffix
        l = self._ldap_conn
        result = l.search_s(base, ldap.SCOPE_SUBTREE, '(cn=Foo*)', ['*'])
        result.sort()
        dn, fields = result[0]
        self.assertEqual(dn, 'cn=Foo1,%s' % base)
        self.assertEqual(type(dn), text_type)
        for key, values in fields.items():
            self.assertEqual(type(key), text_type)
            for value in values:
                self.assertEqual(type(value), bytes)

    def _get_bytes_ldapobject(self, explicit=True):
        if explicit:
            kwargs = {'bytes_mode': True}
        else:
            kwargs = {}
        return self._open_ldap_conn(
            who=self.server.root_dn.encode('utf-8'),
            cred=self.server.root_pw.encode('utf-8'),
            **kwargs
        )

    @unittest.skipUnless(PY2, "no bytes_mode under Py3")
    def test_bytesmode_search_requires_bytes(self):
        l = self._get_bytes_ldapobject()
        base = self.server.suffix

        with self.assertRaises(TypeError):
            l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, '(cn=Foo*)', [b'*'])
        with self.assertRaises(TypeError):
            l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, b'(cn=Foo*)', ['*'])
        with self.assertRaises(TypeError):
            l.search_s(base, ldap.SCOPE_SUBTREE, b'(cn=Foo*)', [b'*'])

    @unittest.skipUnless(PY2, "no bytes_mode under Py3")
    def test_bytesmode_search_results_have_bytes(self):
        l = self._get_bytes_ldapobject()
        base = self.server.suffix
        result = l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, b'(cn=Foo*)', [b'*'])
        result.sort()
        dn, fields = result[0]
        self.assertEqual(dn, b'cn=Foo1,%s' % base)
        self.assertEqual(type(dn), bytes)
        for key, values in fields.items():
            self.assertEqual(type(key), bytes)
            for value in values:
                self.assertEqual(type(value), bytes)

    @unittest.skipUnless(PY2, "no bytes_mode under Py3")
    def test_unset_bytesmode_search_warns_bytes(self):
        l = self._get_bytes_ldapobject(explicit=False)
        base = self.server.suffix

        l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, '(cn=Foo*)', [b'*'])
        l.search_s(base.encode('utf-8'), ldap.SCOPE_SUBTREE, b'(cn=Foo*)', ['*'])
        l.search_s(base, ldap.SCOPE_SUBTREE, b'(cn=Foo*)', [b'*'])

    def test_search_accepts_unicode_dn(self):
        base = self.server.suffix
        l = self._ldap_conn

        with self.assertRaises(ldap.NO_SUCH_OBJECT):
            result = l.search_s("CN=abc\U0001f498def", ldap.SCOPE_SUBTREE)

    def test_filterstr_accepts_unicode(self):
        l = self._ldap_conn
        base = self.server.suffix
        result = l.search_s(base, ldap.SCOPE_SUBTREE, '(cn=abc\U0001f498def)', ['*'])
        self.assertEqual(result, [])

    def test_attrlist_accepts_unicode(self):
        base = self.server.suffix
        result = self._ldap_conn.search_s(
            base, ldap.SCOPE_SUBTREE,
            '(cn=Foo*)', ['abc', 'abc\U0001f498def'])
        result.sort()

        for dn, attrs in result:
            self.assertIsInstance(dn, text_type)
            self.assertEqual(attrs, {})

    def test_search_subtree(self):
        l = self._ldap_conn
        result = l.search_s(self.server.suffix, ldap.SCOPE_SUBTREE, '(cn=Foo*)', ['*'])
        result.sort()
        self.assertEqual(result,
            [('cn=Foo1,'+self.server.suffix,
               {'cn': [b'Foo1'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo2,'+self.server.suffix,
               {'cn': [b'Foo2'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo3,'+self.server.suffix,
               {'cn': [b'Foo3'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo4,ou=Container,'+self.server.suffix,
               {'cn': [b'Foo4'], 'objectClass': [b'organizationalRole']}),
            ]
        )

    def test_search_onelevel(self):
        l = self._ldap_conn
        result = l.search_s(self.server.suffix, ldap.SCOPE_ONELEVEL, '(cn=Foo*)', ['*'])
        result.sort()
        self.assertEqual(result,
            [('cn=Foo1,'+self.server.suffix,
               {'cn': [b'Foo1'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo2,'+self.server.suffix,
               {'cn': [b'Foo2'], 'objectClass': [b'organizationalRole']}),
             ('cn=Foo3,'+self.server.suffix,
               {'cn': [b'Foo3'], 'objectClass': [b'organizationalRole']}),
            ]
        )

    def test_search_oneattr(self):
        l = self._ldap_conn
        result = l.search_s(self.server.suffix, ldap.SCOPE_SUBTREE, '(cn=Foo4)', ['cn'])
        result.sort()
        self.assertEqual(result,
            [('cn=Foo4,ou=Container,'+self.server.suffix, {'cn': [b'Foo4']})]
        )

    def test_search_subschema(self):
        l = self._ldap_conn
        dn = l.search_subschemasubentry_s()
        self.assertIsInstance(dn, text_type)
        self.assertEqual(dn, "cn=Subschema")

    @unittest.skipUnless(PY2, "no bytes_mode under Py3")
    def test_search_subschema_have_bytes(self):
        l = self._get_bytes_ldapobject(explicit=False)
        dn = l.search_subschemasubentry_s()
        self.assertIsInstance(dn, bytes)
        self.assertEqual(dn, b"cn=Subschema")

if __name__ == '__main__':
    unittest.main()
