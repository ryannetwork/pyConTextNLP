#Copyright 2010 Brian E. Chapman
#
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.

"""
A module defining the itemData class. itemData objects are the basis tools for text markup.

The module instantiates several instances of this object:
    1) probableNegations
    2) definiteNegations
    3) pseudoNegations
    4) indications
    5) historicals
    6) conjugates
    7) probables
    8) definites
"""
import csv
import unicodecsv
class contextItem(object):
    __numEnteries = 4
    def __init__(self,args):
        self.__literal = args[0]
        self.__category = args[1]
        self.__re = args[2] # I need to figure out how to read this raw string in properly
        self.__rule = args[3]
    def getLiteral(self):
        return self.__literal
    def getCategory(self):
        return self.__category
    def getRE(self):
        return self.__re
    def getRule(self):
        return self.__rule
    def __unicode__(self):
        txt = u"""literal<<%s>>; category<<%s>>; re<<%s>>; rule<<%s>>"""%(
            self.__literal,self.__category,self.__re, self.__rule)
        return txt
    def __str__(self):
        return unicode(self).encode('utf-8')
    def __repr__(self):
        return unicode(self).encode('utf-8')
   
class itemData(list):
    def __init__(self,*args):
        if( args ):
            for a in args:
                if( self.__validate(a) ):
                    itm = a
                else:
                    try:
                        itm = contextItem(a)
                    except:
                        itm = None
                if( itm ):
                    super(itemData,self).append(itm)
            
    def __validate(self,data):
        return isinstance(data,contextItem)
     
    def dropByLiteral(self,value):
        """drop any contextItems with literal matching value
        """
        # must be a more functional way to write this
        j = 0
        while( True ):
            try:
                itm = self.__getitem__(j)
                if( itm.getLiteral() == value ):
                    self.__delitem__(j)
                else:
                    j += 1
            except:
                break
            
    def append(self,data):
        if(self.__validate(data)):
            itm = data
        else:
            itm = contextItem(data)
        super(itemData,self).append(itm)
    def insert(self,index,data):
        if(self.__validate(data)):
            itm = data
        else:
            itm = contextItem(data)
        super(itemData,self).insert(index,itm)
    def prepend(self,iterable):
        for i in iterable:
            if( self.__validate(i) ):
                itm = i
            else:
                itm = contextItem(i)
            super(itemData,self).insert(0,itm)
    def extend(self,iterable):
        for i in iterable:
            if( self.__validate(i) ):
                itm = i
            else:
                itm = contextItem(i)
            super(itemData,self).append(itm)
    def __unicode__(self):
        tmp = u"""itemData: %d items ["""%len(self)
        for i in self:
            tmp = tmp+"%s, "%i.getLiteral()
        tmp = tmp+"]"
        return tmp
    def __repr__(self):
        return unicode(self).encode('utf-8')
    def __str__(self):
        return unicode(self).encode('utf-8')

def instantiateFromCSV(csvFile, encoding='utf-8'):
    """takes a CSV file of itemdata rules and creates itemData instances.
    Expects first row to be header"""
    items = {} # dictionary of itemData categories to be returned to the user
    reader = unicodecsv.reader( open(csvFile, 'rU'),encoding=encoding )
    #reader = csv.reader(open(csvFile, 'rU'))
    rownum=0
    for row in reader:
        if rownum == 0:
            header = row
        else:
            case = row[0]
#        print case
            category = items.get(case,itemData())
            tmp = row[1:5]
            tmp[2] = ur"%s"%tmp[2] # convert the regular expression string into a raw string
            item = contextItem(tmp)
            category.append(item)
            items[case] = category
        rownum += 1
    return items
