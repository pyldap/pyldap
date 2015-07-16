from __future__ import print_function

import pyldap,pyldap.async

class DeleteLeafs(pyldap.async.AsyncSearchHandler):
  """
  Class for deleting entries which are results of a search.
  
  DNs of Non-leaf entries are collected in DeleteLeafs.nonLeafEntries.
  """
  _entryResultTypes = pyldap.async._entryResultTypes

  def __init__(self,l):
    pyldap.async.AsyncSearchHandler.__init__(self,l)
    self.nonLeafEntries = []
    self.deletedEntries = 0

  def startSearch(self,searchRoot,searchScope):
    if not searchScope in [pyldap.SCOPE_ONELEVEL,pyldap.SCOPE_SUBTREE]:
      raise ValueError("Parameter searchScope must be either pyldap.SCOPE_ONELEVEL or pyldap.SCOPE_SUBTREE.")
    self.nonLeafEntries = []
    self.deletedEntries = 0
    pyldap.async.AsyncSearchHandler.startSearch(
      self,
      searchRoot,
      searchScope,
      filterStr='(objectClass=*)',
      attrList=['hasSubordinates','numSubordinates'],
      attrsOnly=0,
    )

  def _processSingleResult(self,resultType,resultItem):
    if resultType in self._entryResultTypes:
      # Don't process search references
      dn,entry = resultItem
      hasSubordinates = entry.get(
        'hasSubordinates',
        entry.get('hassubordinates',['FALSE']
        )
      )[0]
      numSubordinates = entry.get(
        'numSubordinates',
        entry.get('numsubordinates',['0'])
      )[0]
      if hasSubordinates=='TRUE' or int(numSubordinates):
        self.nonLeafEntries.append(dn)
      else:
        try:
          self._l.delete_s(dn)
        except pyldap.NOT_ALLOWED_ON_NONLEAF as e:
          self.nonLeafEntries.append(dn)
        else:
          self.deletedEntries = self.deletedEntries+1


def DelTree(l,dn,scope=pyldap.SCOPE_ONELEVEL):
  """
  Recursively delete entries below or including entry with name dn.
  """
  leafs_deleter = DeleteLeafs(l)
  leafs_deleter.startSearch(dn,scope)
  leafs_deleter.processResults()
  deleted_entries = leafs_deleter.deletedEntries
  non_leaf_entries = leafs_deleter.nonLeafEntries[:]
  while non_leaf_entries:
    dn = non_leaf_entries.pop()
    print(deleted_entries,len(non_leaf_entries),dn)
    leafs_deleter.startSearch(dn,pyldap.SCOPE_SUBTREE)
    leafs_deleter.processResults()
    deleted_entries = deleted_entries+leafs_deleter.deletedEntries
    non_leaf_entries.extend(leafs_deleter.nonLeafEntries)
  return # DelTree()


# Create LDAPObject instance
l = pyldap.initialize('ldap://localhost:1390')

# Try a bind to provoke failure if protocol version is not supported
l.simple_bind_s('cn=Directory Manager,dc=IMC,dc=org','controller')

# Delete all entries *below* the entry dc=Delete,dc=IMC,dc=org
DelTree(l,'dc=Delete,dc=IMC,dc=org',pyldap.SCOPE_ONELEVEL)
