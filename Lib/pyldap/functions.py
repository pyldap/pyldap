"""
functions.py - wraps functions of module _pyldap

See http://www.python-ldap.org/ for details.

\$Id: functions.py,v 1.31 2015/06/06 09:21:37 stroeder Exp $

Compability:
- Tested with Python 2.0+ but should work with Python 1.5.x
- functions should behave exactly the same like in _pyldap

Usage:
Directly imported by pyldap/__init__.py. The symbols of _pyldap are
overridden.

Thread-lock:
Basically calls into the LDAP lib are serialized by the module-wide
lock _ldapmodule_lock.
"""

from pyldap import __version__

__all__ = [
  'open','initialize','init',
  'explode_dn','explode_rdn',
  'get_option','set_option',
  'escape_str',
]

import sys,pprint,_pyldap,pyldap

from pyldap import LDAPError

from pyldap.dn import explode_dn,explode_rdn

from pyldap.ldapobject import LDAPObject

if __debug__:
  # Tracing is only supported in debugging mode
  import traceback


def _ldap_function_call(lock,func,*args,**kwargs):
  """
  Wrapper function which locks and logs calls to function

  lock
      Instance of threading.Lock or compatible
  func
      Function to call with arguments passed in via *args and **kwargs
  """
  if lock:
    lock.acquire()
  if __debug__:
    if pyldap._trace_level>=1:
      pyldap._trace_file.write('*** %s.%s %s\n' % (
        '_pyldap',func.__name__,
        pprint.pformat((args,kwargs))
      ))
      if pyldap._trace_level>=9:
        traceback.print_stack(limit=pyldap._trace_stack_limit,file=pyldap._trace_file)
  try:
    try:
      result = func(*args,**kwargs)
    finally:
      if lock:
        lock.release()
  except LDAPError as e:
    if __debug__ and pyldap._trace_level>=2:
      pyldap._trace_file.write('=> LDAPError: %s\n' % (str(e)))
    raise
  if __debug__ and pyldap._trace_level>=2:
    pyldap._trace_file.write('=> result:\n%s\n' % (pprint.pformat(result)))
  return result


def initialize(uri,trace_level=0,trace_file=sys.stdout,trace_stack_limit=None):
  """
  Return LDAPObject instance by opening LDAP connection to
  LDAP host specified by LDAP URL

  Parameters:
  uri
        LDAP URL containing at least connection scheme and hostport,
        e.g. ldap://localhost:389
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  return LDAPObject(uri,trace_level,trace_file,trace_stack_limit)


def open(host,port=389,trace_level=0,trace_file=sys.stdout,trace_stack_limit=None):
  """
  Return LDAPObject instance by opening LDAP connection to
  specified LDAP host

  Parameters:
  host
        LDAP host and port, e.g. localhost
  port
        integer specifying the port number to use, e.g. 389
  trace_level
        If non-zero a trace output of LDAP calls is generated.
  trace_file
        File object where to write the trace output to.
        Default is to use stdout.
  """
  import warnings
  warnings.warn('pyldap.open() is deprecated! Use pyldap.initialize() instead.', DeprecationWarning,2)
  return initialize('ldap://%s:%d' % (host,port),trace_level,trace_file,trace_stack_limit)

init = open


def get_option(option):
  """
  get_option(name) -> value

  Get the value of an LDAP global option.
  """
  return _ldap_function_call(None,_pyldap.get_option,option)


def set_option(option,invalue):
  """
  set_option(name, value)

  Set the value of an LDAP global option.
  """
  return _ldap_function_call(None,_pyldap.set_option,option,invalue)


def escape_str(escape_func,s,*args):
  """
  Applies escape_func() to all items of `args' and returns a string based
  on format string `s'.
  """
  escape_args = map(escape_func,args)
  return s % tuple(escape_args)
