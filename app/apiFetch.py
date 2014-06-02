#!/usr/bin/python
import requests
import ast
import logging
from xml.dom import minidom
from sys import exit

uri = {'characters' : 'account/characters.xml.aspx', 'skillQueue' : 'char/SkillQueue.xml.aspx'}
eveURL = 'https://api.eveonline.com/'
class APIFetch:
    

    def __init__(self, req, keyID, vCode, characterID=None):
        self.req = uri[req]
        self.payload = {'keyID' : keyID, 'vCode' : vCode, 'characterID' : characterID}
        self.result = []
        try:
            r = requests.get(eveURL+self.req, params = self.payload)
            #pass    
        except requests.exceptions.ConnectionError:
            print('ERROR: Could not connect to %s') % (eveURL)
            return None 

        response = minidom.parseString(r.text)
        #print r.text
        #response = minidom.parse('skillque2.xml')
        xmlResult = response.getElementsByTagName('result')
        self.parseResult(xmlResult)
        return

    def parseResult(self, result):
        parsedRowset = []
        parsedRow = {}
        for rowset in result[0].getElementsByTagName('rowset'):
            #print'API call: %s' % (rowset.attributes['name'].value)
            columns = []
            for key in str(rowset.attributes['columns'].value).split(','):
                columns.append(key)
            for row in rowset.getElementsByTagName('row'):
                for key in columns:
                    #print '%s: %s' % (key,row.attributes[key].value)
                    parsedRow[str(key)] = str(row.attributes[key].value)
                parsedRowset.append(parsedRow)
                parsedRow = {}
            self.result.append(parsedRowset)
        return 'OK'


