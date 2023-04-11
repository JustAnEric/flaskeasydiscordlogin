import json, os, re, random, sys
class NewDatabase:
  def __init__(self, dbName):
    try:
      uf = json.load(open('./databases.json'))
      if (uf.get(dbName)):
        self.dbName = dbName
        self.db = json.load(open('./databases.json'))
        return print(f"Database name `{dbName}` already exists!")
      else:
        with open('./databases.json', 'w') as f:
          uf[dbName] = {}
          json.dump(uf, f)
        print("Written database.")
        self.dbName = dbName
        self.db = json.load(open('./databases.json'))
    except: 
      with open('./databases.json','w') as f: f.write('{"%s": {}}' % (dbName));
      self.dbName = dbName
      self.db = json.load(open('./databases.json'))

  def getKey(self, keyName):
    return self.db[self.dbName].get(keyName)
  def setKey(self, keyName, keyValue):
    with open('./databases.json','w') as f:
      self.db[self.dbName][keyName] = keyValue
      json.dump(self.db, f)
    return self.db[self.dbName][keyName]
  def removeKey(self, keyName):
    with open('./databases.json', 'w') as f:
      del self.db[self.dbName][keyName]
      json.dump(self.db, f)
  def editKey(self, keyName, newValue):
    with open('./databases.json', 'w') as f:
      self.db[self.dbName][keyName] = newValue
      json.dump(self.db, f)
  def clearKeys(self):
    with open('./databases.json', 'w') as f:
      self.db[self.dbName] = {}
      json.dump(self.db, f)
