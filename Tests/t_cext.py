from __future__ import unicode_literals


import unittest, slapd
import _pyldap
import logging

reusable_server = None
def get_reusable_server():
    global reusable_server
    if reusable_server is None:
        reusable_server = slapd.Slapd()
    return reusable_server

class TestLdapCExtension(unittest.TestCase):
    """Tests the LDAP C Extension module, _pyldap.
       These tests apply only to the _pyldap module and bypass the
       LDAPObject wrapper completely."""

    timeout = 3

    def _init_server(self, reuse_existing=True):
        global reusable_server
        """Sets self.server to a test LDAP server and self.base
           to its base"""
        if reuse_existing:
            server = get_reusable_server()
        else:
            server = slapd.Slapd() # private server
        #server.set_debug()  # enables verbose messages
        server.start()   # no effect if already started
        self.server = server
        self.base = server.get_dn_suffix()
        return server

    def _init(self, reuse_existing=True, bind=True):
        """Starts a server, and returns a LDAPObject bound to it"""
        server = self._init_server(reuse_existing)
        l = _pyldap.initialize(server.get_url())
        if bind:
            # Perform a simple bind
            l.set_option(_pyldap.OPT_PROTOCOL_VERSION, _pyldap.VERSION3)
            m = l.simple_bind(server.get_root_dn(), server.get_root_password())
            result, _pmsg, _msgid, _ctrls = l.result4(m, _pyldap.MSG_ONE, self.timeout)
            self.assertTrue(result, _pyldap.RES_BIND)
        return l

    def assertNotNone(self, expr, msg=None):
        self.assertFalse(expr is None, msg or repr(expr))
    def assertNone(self, expr, msg=None):
        self.assertFalse(expr is not None, msg or repr(expr))

    # Test for the existence of a whole bunch of constants
    # that the C module is supposed to export
    def test_constants(self):
        self.assertEqual(_pyldap.PORT, 389)
        self.assertEqual(_pyldap.VERSION1, 1)
        self.assertEqual(_pyldap.VERSION2, 2)
        self.assertEqual(_pyldap.VERSION3, 3)

        # constants for result4()
        self.assertEqual(_pyldap.RES_BIND, 0x61)
        self.assertEqual(_pyldap.RES_SEARCH_ENTRY, 0x64)
        self.assertEqual(_pyldap.RES_SEARCH_RESULT, 0x65)
        self.assertEqual(_pyldap.RES_MODIFY, 0x67)
        self.assertEqual(_pyldap.RES_ADD, 0x69)
        self.assertEqual(_pyldap.RES_DELETE, 0x6b)
        self.assertEqual(_pyldap.RES_MODRDN, 0x6d)
        self.assertEqual(_pyldap.RES_COMPARE, 0x6f)
        self.assertEqual(_pyldap.RES_SEARCH_REFERENCE, 0x73) # v3
        self.assertEqual(_pyldap.RES_EXTENDED, 0x78)         # v3
        #self.assertEqual(_pyldap.RES_INTERMEDIATE, 0x79)     # v3
        self.assertNotNone(_pyldap.RES_ANY)
        self.assertNotNone(_pyldap.RES_UNSOLICITED)

        self.assertNotNone(_pyldap.AUTH_NONE)
        self.assertNotNone(_pyldap.AUTH_SIMPLE)

        self.assertNotNone(_pyldap.SCOPE_BASE)
        self.assertNotNone(_pyldap.SCOPE_ONELEVEL)
        self.assertNotNone(_pyldap.SCOPE_SUBTREE)

        self.assertNotNone(_pyldap.MOD_ADD)
        self.assertNotNone(_pyldap.MOD_DELETE)
        self.assertNotNone(_pyldap.MOD_REPLACE)
        self.assertNotNone(_pyldap.MOD_INCREMENT)
        self.assertNotNone(_pyldap.MOD_BVALUES)

        # for result4()
        self.assertNotNone(_pyldap.MSG_ONE)
        self.assertNotNone(_pyldap.MSG_ALL)
        self.assertNotNone(_pyldap.MSG_RECEIVED)

        # for OPT_DEFEF
        self.assertNotNone(_pyldap.DEREF_NEVER)
        self.assertNotNone(_pyldap.DEREF_SEARCHING)
        self.assertNotNone(_pyldap.DEREF_FINDING)
        self.assertNotNone(_pyldap.DEREF_ALWAYS)

        # for OPT_SIZELIMIT, OPT_TIMELIMIT
        self.assertNotNone(_pyldap.NO_LIMIT)

        # standard options
        self.assertNotNone(_pyldap.OPT_API_INFO)
        self.assertNotNone(_pyldap.OPT_DEREF)
        self.assertNotNone(_pyldap.OPT_SIZELIMIT)
        self.assertNotNone(_pyldap.OPT_TIMELIMIT)
        self.assertNotNone(_pyldap.OPT_REFERRALS)
        self.assertNotNone(_pyldap.OPT_RESTART)
        self.assertNotNone(_pyldap.OPT_PROTOCOL_VERSION)
        self.assertNotNone(_pyldap.OPT_SERVER_CONTROLS)
        self.assertNotNone(_pyldap.OPT_CLIENT_CONTROLS)
        self.assertNotNone(_pyldap.OPT_API_FEATURE_INFO)
        self.assertNotNone(_pyldap.OPT_HOST_NAME)
        self.assertNotNone(_pyldap.OPT_ERROR_NUMBER)   # = OPT_RESULT_CODE
        self.assertNotNone(_pyldap.OPT_ERROR_STRING)   # = OPT_DIAGNOSITIC_MESSAGE
        self.assertNotNone(_pyldap.OPT_MATCHED_DN)

        # OpenLDAP specific
        self.assertNotNone(_pyldap.OPT_DEBUG_LEVEL)
        self.assertNotNone(_pyldap.OPT_TIMEOUT)
        self.assertNotNone(_pyldap.OPT_REFHOPLIMIT)
        self.assertNotNone(_pyldap.OPT_NETWORK_TIMEOUT)
        self.assertNotNone(_pyldap.OPT_URI)
        #self.assertNotNone(_pyldap.OPT_REFERRAL_URLS)
        #self.assertNotNone(_pyldap.OPT_SOCKBUF)
        #self.assertNotNone(_pyldap.OPT_DEFBASE)
        #self.assertNotNone(_pyldap.OPT_CONNECT_ASYNC)

        # str2dn()
        self.assertNotNone(_pyldap.DN_FORMAT_LDAP)
        self.assertNotNone(_pyldap.DN_FORMAT_LDAPV3)
        self.assertNotNone(_pyldap.DN_FORMAT_LDAPV2)
        self.assertNotNone(_pyldap.DN_FORMAT_DCE)
        self.assertNotNone(_pyldap.DN_FORMAT_UFN)
        self.assertNotNone(_pyldap.DN_FORMAT_AD_CANONICAL)
        self.assertNotNone(_pyldap.DN_FORMAT_MASK)
        self.assertNotNone(_pyldap.DN_PRETTY)
        self.assertNotNone(_pyldap.DN_SKIP)
        self.assertNotNone(_pyldap.DN_P_NOLEADTRAILSPACES)
        self.assertNotNone(_pyldap.DN_P_NOSPACEAFTERRDN)
        self.assertNotNone(_pyldap.DN_PEDANTIC)
        self.assertNotNone(_pyldap.AVA_NULL)
        self.assertNotNone(_pyldap.AVA_STRING)
        self.assertNotNone(_pyldap.AVA_BINARY)
        self.assertNotNone(_pyldap.AVA_NONPRINTABLE)

        # these constants useless after ldap_url_parse() was dropped XXX
        self.assertNotNone(_pyldap.URL_ERR_BADSCOPE)
        self.assertNotNone(_pyldap.URL_ERR_MEM)

    def test_simple_bind(self):
        l = self._init()

    def test_simple_anonymous_bind(self):
        l = self._init(bind=False)
        m = l.simple_bind("", "")
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertTrue(result, _pyldap.RES_BIND)
        self.assertEqual(msgid, m)
        self.assertEqual(pmsg, [])
        self.assertEqual(ctrls, [])

        # see if we can get the rootdse while we're here
        m = l.search_ext("", _pyldap.SCOPE_BASE, '(objectClass=*)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(pmsg[0][0], "") # rootDSE has no dn
        self.assertEqual(msgid, m)
        self.assertIn('objectClass', pmsg[0][1])

    def test_unbind(self):
        l = self._init()
        m = l.unbind_ext()
        self.assertNone(m)

        # Second attempt to unbind should yield an exception
        try: l.unbind_ext()
        except _pyldap.error: pass

    def test_search_ext_individual(self):
        l = self._init()

        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, 
                '(objectClass=dcObject)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ONE, self.timeout)

        # Expect to get just one object
        self.assertEqual(result, _pyldap.RES_SEARCH_ENTRY)
        self.assertEqual(len(pmsg), 1)
        self.assertEqual(len(pmsg[0]), 2)
        self.assertEqual(pmsg[0][0], self.base)
        self.assertEqual(pmsg[0][0], self.base)
        self.assertTrue(b'dcObject' in pmsg[0][1]['objectClass'])
        self.assertTrue(b'organization' in pmsg[0][1]['objectClass'])
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ONE, self.timeout)
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(pmsg, [])
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

    def test_abandon(self):
        l = self._init()

        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(objectClass=*)')

        ret = l.abandon_ext(m)
        self.assertNone(ret)

        got_timeout = False
        try:
            r = l.result4(m, _pyldap.MSG_ALL, 0.3)  # (timeout /could/ be longer)
        except _pyldap.TIMEOUT as e:
            got_timeout = True
        self.assertTrue(got_timeout)

    def test_search_ext_all(self):
        l = self._init()

        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(objectClass=*)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)

        # Expect to get some objects
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertTrue(len(pmsg) >= 2)
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

    def test_add(self):
        l = self._init()

        m = l.add_ext("cn=Foo," + self.base, [
               ('objectClass', b'organizationalRole'),
               ('cn', b'Foo'),
               ('description', b'testing'),
            ])

        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)
        self.assertEqual(pmsg, [])
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

        # search for it back
        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(cn=Foo)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)

        # Expect to get the objects
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(len(pmsg), 1)
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

        self.assertEqual(pmsg[0], ('cn=Foo,'+self.base,
                { 'objectClass': [b'organizationalRole'],
                  'cn': [b'Foo'],
                  'description': [b'testing'] }))

    def test_compare(self):
        l = self._init()

        # first, add an object with a field we can compare on
        dn = "cn=CompareTest," + self.base
        m = l.add_ext(dn, [
               ('objectClass', b'person'),
               ('sn', b'CompareTest'),
               ('cn', b'CompareTest'),
               ('userPassword', b'the_password'),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)

        # try a false compare
        m = l.compare_ext(dn, "userPassword", "bad_string")
        compared_false = False
        try:
            r = l.result4(m, _pyldap.MSG_ALL, self.timeout)
            self.fail(repr(r))
        except _pyldap.COMPARE_FALSE:
            compared_false = True
        self.assertTrue(compared_false)

        # try a true compare
        m = l.compare_ext(dn, "userPassword", "the_password")
        compared_true = False
        try:
            r = l.result4(m, _pyldap.MSG_ALL, self.timeout)
            self.fail(repr(r))
        except _pyldap.COMPARE_TRUE:
            compared_true = True
        self.assertTrue(compared_true)

        m = l.compare_ext(dn, "badAttribute", "ignoreme")
        raised_error = False
        try:
            r = l.result4(m, _pyldap.MSG_ALL, self.timeout)
            self.fail(repr(r))
        except _pyldap.error:
            raised_error = True
        self.assertTrue(raised_error)

    def test_delete_no_such_object(self):
        l = self._init()

        # try deleting an object that doesn't exist
        not_found = False
        m = l.delete_ext("cn=DoesNotExist,"+self.base)
        try:
            r = l.result4(m, _pyldap.MSG_ALL, self.timeout)
            self.fail(r)
        except _pyldap.NO_SUCH_OBJECT:
            not_found = True
        self.assertTrue(not_found)

    def test_delete(self):
        l = self._init()
        # first, add an object we will delete
        dn = "cn=Deleteme,"+self.base
        m = l.add_ext(dn, [
               ('objectClass', b'organizationalRole'),
               ('cn', b'Deleteme'),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)

        m = l.delete_ext(dn)
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_DELETE)
        self.assertEqual(msgid, m)
        self.assertEqual(pmsg, [])
        self.assertEqual(ctrls, [])

    def test_modify_no_such_object(self):
        l = self._init()

        # try deleting an object that doesn't exist
        not_found = False
        m = l.modify_ext("cn=DoesNotExist,"+self.base, [
                (_pyldap.MOD_ADD, 'description', [b'blah']),
            ])
        try:
            r = l.result4(m, _pyldap.MSG_ALL, self.timeout)
            self.fail(r)
        except _pyldap.NO_SUCH_OBJECT:
            not_found = True
        self.assertTrue(not_found)

    def DISABLED_test_modify_no_such_object_empty_attrs(self):
        # XXX ldif-backend for slapd appears broken???

        l = self._init()

        # try deleting an object that doesn't exist
        m = l.modify_ext("cn=DoesNotExist,"+self.base, [
                (_pyldap.MOD_ADD, 'description', []),
            ])
        self.assertTrue(isinstance(m, int))
        r = l.result4(m, _pyldap.MSG_ALL, self.timeout) # what should happen??
        self.fail(r)

    def test_modify(self):
        l = self._init()
        # first, add an object we will delete
        dn = "cn=AddToMe,"+self.base
        m = l.add_ext(dn, [
               ('objectClass', b'person'),
               ('cn', b'AddToMe'),
               ('sn', b'Modify'),
               ('description', b'a description'),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)

        m = l.modify_ext(dn, [
                (_pyldap.MOD_ADD, 'description', [b'b desc', b'c desc']),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_MODIFY)
        self.assertEqual(pmsg, [])
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

        # search for it back
        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(cn=AddToMe)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)

        # Expect to get the objects
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(len(pmsg), 1)
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

        self.assertEqual(pmsg[0][0], dn)
        d = list(pmsg[0][1]['description'])
        d.sort()
        self.assertEqual(d, [b'a description', b'b desc', b'c desc'])

    def test_rename(self):
        l = self._init()
        dn = "cn=RenameMe,"+self.base
        m = l.add_ext(dn, [
               ('objectClass', b'organizationalRole'),
               ('cn', b'RenameMe'),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)

        # do the rename with same parent
        m = l.rename(dn, "cn=IAmRenamed")
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_MODRDN)
        self.assertEqual(msgid, m)
        self.assertEqual(pmsg, [])
        self.assertEqual(ctrls, [])

        # make sure the old one is gone
        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(cn=RenameMe)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(len(pmsg), 0) # expect no results
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

        # check that the new one looks right
        dn2 = "cn=IAmRenamed,"+self.base
        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(cn=IAmRenamed)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])
        self.assertEqual(len(pmsg), 1)
        self.assertEqual(pmsg[0][0], dn2)
        self.assertEqual(pmsg[0][1]['cn'], [b'IAmRenamed'])

        # create the container
        containerDn = "ou=RenameContainer,"+self.base
        m = l.add_ext(containerDn, [
               ('objectClass', b'organizationalUnit'),
               ('ou', b'RenameContainer'),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)

        # WORKAROUND bug in slapd. (Without an existing child, 
        # renames into a container object do not work for the ldif backend,
        # the renamed object appears to be deleted, not moved.)
        # see http://www.openldap.org/its/index.cgi/Software%20Bugs?id=5408
        m = l.add_ext("cn=Bogus," + containerDn, [
               ('objectClass', b'organizationalRole'),
               ('cn', b'Bogus'),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)

        # now rename from dn2 to the conater
        dn3 = "cn=IAmRenamedAgain," + containerDn

        # Now try renaming dn2 across container (simultaneous name change)
        m = l.rename(dn2, "cn=IAmRenamedAgain", containerDn)
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_MODRDN)
        self.assertEqual(msgid, m)
        self.assertEqual(pmsg, [])
        self.assertEqual(ctrls, [])

        # make sure dn2 is gone
        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(cn=IAmRenamed)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(len(pmsg), 0) # expect no results
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])

        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(objectClass=*)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)

        # make sure dn3 is there
        m = l.search_ext(self.base, _pyldap.SCOPE_SUBTREE, '(cn=IAmRenamedAgain)')
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_SEARCH_RESULT)
        self.assertEqual(msgid, m)
        self.assertEqual(ctrls, [])
        self.assertEqual(len(pmsg), 1)
        self.assertEqual(pmsg[0][0], dn3)
        self.assertEqual(pmsg[0][1]['cn'], [b'IAmRenamedAgain'])


    def test_whoami(self):
        l = self._init()
        r = l.whoami_s()
        self.assertEqual("dn:" + self.server.get_root_dn(), r)

    def test_whoami_unbound(self):
        l = self._init(bind=False)
        l.set_option(_pyldap.OPT_PROTOCOL_VERSION, _pyldap.VERSION3)
        r = l.whoami_s()
        self.assertEqual("", r)

    def test_whoami_anonymous(self):
        l = self._init(bind=False)
        l.set_option(_pyldap.OPT_PROTOCOL_VERSION, _pyldap.VERSION3)

        # Anonymous bind
        m = l.simple_bind("", "")
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertTrue(result, _pyldap.RES_BIND)

        r = l.whoami_s()
        self.assertEqual("", r)

    def test_passwd(self):
        l = self._init()

        # first, create a user to change password on
        dn = "cn=PasswordTest," + self.base
        m = l.add_ext(dn, [
               ('objectClass', b'person'),
               ('sn', b'PasswordTest'),
               ('cn', b'PasswordTest'),
               ('userPassword', b'initial'),
            ])
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(result, _pyldap.RES_ADD)

        # try changing password with a wrong old-pw
        m = l.passwd(dn, "bogus", "ignored")
        try:
            r = l.result4(m, _pyldap.MSG_ALL, self.timeout)
            self.fail("expected UNWILLING_TO_PERFORM")
        except _pyldap.UNWILLING_TO_PERFORM:
            pass

        # try changing password with a correct old-pw
        m = l.passwd(dn, "initial", "changed")
        result,pmsg,msgid,ctrls = l.result4(m, _pyldap.MSG_ALL, self.timeout)
        self.assertEqual(msgid, m)
        self.assertEqual(pmsg, [])
        self.assertEqual(result, _pyldap.RES_EXTENDED)
        self.assertEqual(ctrls, [])

    def test_options(self):
        oldval = _pyldap.get_option(_pyldap.OPT_PROTOCOL_VERSION)
        try:

            try:
                _pyldap.set_option(_pyldap.OPT_PROTOCOL_VERSION, "3")
                self.fail("expected string value to raise a type error")
            except TypeError: pass

            _pyldap.set_option(_pyldap.OPT_PROTOCOL_VERSION, _pyldap.VERSION2)
            v = _pyldap.get_option(_pyldap.OPT_PROTOCOL_VERSION)
            self.assertEqual(v, _pyldap.VERSION2)
            _pyldap.set_option(_pyldap.OPT_PROTOCOL_VERSION, _pyldap.VERSION3)
            v = _pyldap.get_option(_pyldap.OPT_PROTOCOL_VERSION)
            self.assertEqual(v, _pyldap.VERSION3)
        finally:
            _pyldap.set_option(_pyldap.OPT_PROTOCOL_VERSION, oldval)

        l = self._init()

        # Try changing some basic options and checking that they took effect

        l.set_option(_pyldap.OPT_PROTOCOL_VERSION, _pyldap.VERSION2)
        v = l.get_option(_pyldap.OPT_PROTOCOL_VERSION)
        self.assertEqual(v, _pyldap.VERSION2)

        l.set_option(_pyldap.OPT_PROTOCOL_VERSION, _pyldap.VERSION3)
        v = l.get_option(_pyldap.OPT_PROTOCOL_VERSION)
        self.assertEqual(v, _pyldap.VERSION3)

        # Try setting options that will yield a known error.
        try:
            _pyldap.get_option(_pyldap.OPT_MATCHED_DN)
            self.fail("expected ValueError")
        except ValueError:
            pass

    def _require_attr(self, obj, attrname):
        """Returns true if the attribute exists on the object.
           This is to allow some tests to be optional, because
           _pyldap is compiled with different properties depending
           on the underlying C library.
           This could me made to thrown an exception if you want the
           tests to be strict."""
        if hasattr(obj, attrname):
            return True
        #self.fail("required attribute '%s' missing" % attrname)
        return False

    def test_sasl(self):
        l = self._init()
        if not self._require_attr(l, 'sasl_interactive_bind_s'): # HAVE_SASL
            return
        # TODO

    def test_tls(self):
        l = self._init()
        if not self._require_attr(l, 'start_tls_s'):    # HAVE_TLS
            return
        # TODO

    def test_cancel(self):
        l = self._init()
        if not self._require_attr(l, 'cancel'):         # FEATURE_CANCEL
            return

    def test_str2dn(self):
        pass

if __name__ == '__main__':
    unittest.main()
