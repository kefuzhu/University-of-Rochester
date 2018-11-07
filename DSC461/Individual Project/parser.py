
"""
FILE: parser.py
------------------
Author: Garrett Schlesinger (gschles@cs.stanford.edu)
Author: Chenyu Yang (chenyuy@stanford.edu)
Modified: 10/13/2012

parser for csc261 adapted from (cs145 programming project 1 offered by stanford).
Has useful imports and functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay xml files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the xml files store dollar value amounts in 
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the xml files store dates/ times in the form 
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.
4) A function to get the #PCDATA of a given element (returns the empty string
if the element is not of #PCDATA type)
5) A function to get the #PCDATA of the first subelement of a given element with
a given tagname. (returns the empty string if the element doesn't exist or 
is not of #PCDATA type)
6) A function to get all elements of a specific tag name that are children of a
given element
7) A function to get only the first such child

You can use the file as it is. 
"""

import sys
from xml.dom.minidom import parse
from re import sub

columnSeparator = "<>"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
                'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}


"""
Returns true if a file ends in .xml
"""
def isXml(f):
    return len(f) > 4 and f[-4:] == '.xml'


# DOM traversal
"""
Non-recursive (NR) version of dom.getElementsByTagName(...)
"""
def getElementsByTagNameNR(elem, tagName):
    elements = []
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            elements.append(child)
    return elements

"""
Returns the first subelement of elem matching the given tagName,
or null if one does not exist.
"""
def getElementByTagNameNR(elem, tagName):
    children = elem.childNodes
    for child in children:
        if child.nodeType == child.ELEMENT_NODE and child.tagName == tagName:
            return child
    return None

"""
Parses out the PCData of an xml element
"""
def pcdata(elem):
        return elem.toxml().replace('<'+elem.tagName+'>','').replace('</'+elem.tagName+'>','').replace('<'+elem.tagName+'/>','')

"""
Return the text associated with the given element (which must have type
#PCDATA) as child, or "" if it contains no text.
"""
def getElementText(elem):
    if len(elem.childNodes) == 1:
        return pcdata(elem) 
    return ''

"""
Returns the text (#PCDATA) associated with the first subelement X of e
with the given tagName. If no such X exists or X contains no text, "" is
returned.
"""
def getElementTextByTagNameNR(elem, tagName):
    curElem = getElementByTagNameNR(elem, tagName)
    if curElem != None:
        return pcdata(curElem)
    return ''



# String formatting

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon] 
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""
def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)



# Initialize output files, one for each relation/table
item_file = open('item.dat', 'w')
category_file = open('category.dat', 'w')
user_file = open('user.dat', 'w')
bid_file = open('bid.dat', 'w')

# Write one line to the file corresponding to one tuple with the given attributes
# Attributes are written in order, separated by delimiter '<>'
def writeLine(dataFile, attributes):
    line = columnSeparator.join(attributes)
    dataFile.write(line)
    dataFile.write('\n')


def writeItem(item):
    itemID = item.getAttribute('ItemID')
    sellerID = item.getElementsByTagName('Seller')[0].getAttribute('UserID')
    name = getElementTextByTagNameNR(item,'Name')
    currently = transformDollar(getElementTextByTagNameNR(item,'Currently'))
    buy_price = transformDollar(getElementTextByTagNameNR(item,'Buy_Price'))
    if (buy_price == ''): buy_price = 'NULL'
    first_bid = transformDollar(getElementTextByTagNameNR(item, 'First_Bid'))
    started = transformDttm(getElementTextByTagNameNR(item, 'Started'))
    ends = transformDttm(getElementTextByTagNameNR(item, 'Ends'))
    description = getElementTextByTagNameNR(item, 'Description')

    writeLine(item_file, [itemID, name, currently, buy_price, first_bid, started, ends, sellerID, description])


def writeSeller(item):
    seller = item.getElementsByTagName('Seller')[0]
    userID = seller.getAttribute('UserID')
    rating = seller.getAttribute('Rating')
    location = getElementTextByTagNameNR(item, 'Location')
    country = getElementTextByTagNameNR(item, 'Country')
    writeLine(user_file, [userID, rating, location, country])


def writeBid(bid, itemID):
    bidder = bid.getElementsByTagName('Bidder')[0]
    userID = bidder.getAttribute('UserID')
    time = transformDttm(getElementTextByTagNameNR(bid, 'Time'))
    amount = transformDollar(getElementTextByTagNameNR(bid, 'Amount'))
    writeLine(bid_file, [itemID, userID, time, amount])


def itemID(item):
    return item.getAttribute('ItemID')

def sellerID(item):
    return item.getElementsByTagName('Seller')[0].getAttribute('UserID')

def bidderID(bid):
    return bid.getElementsByTagName('Bidder')[0].getAttribute('UserID')

def bidderRating(bid):
    return bid.getElementsByTagName('Bidder')[0].getAttribute('Rating')

def writeCategories(item):
    itemID = item.getAttribute('ItemID')
    categories = []
    for node in item.getElementsByTagName('Category'):
        category = getElementText(node)
        if (category not in categories):
            categories.append(category)
            writeLine(category_file, [itemID, category])


def writeNonSellers():
    for userID in users.keys():
        writeLine(user_file, [userID, users[userID], 'NULL', 'NULL'])



sellers = []
users = {}

"""
Parses a single xml file. 
"""
def parseXml(f):
    dom = parse(f) # creates a dom object for the supplied xml file
    """
    TO DO: traverse the dom tree to extract information for your SQL tables
    """

    Items = dom.getElementsByTagName('Item')


    for item in Items:

        # write tuple into Item table
        writeItem(item)

        # write all tuples into Category table
        writeCategories(item)

        # Keep track of previously encountered sellers
        if (sellerID(item) not in sellers):
            sellers.append(sellerID(item))
            if (sellerID(item) in users): del users[sellerID(item)] # If user both bidder/seller, use seller
            writeSeller(item) # write tuple into User table


        # write all tuples into Bid table
        for bid in item.getElementsByTagName('Bid'):
            writeBid(bid, itemID(item))

            # store bidderID for later processing
            if (bidderID(bid) not in sellers): 
                users[bidderID(bid)] = bidderRating(bid)




"""
Loops through each xml files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_parser.py <path to xml files>'
        sys.exit(1)
    # loops over all .xml files in the argument
    for f in argv[1:]:
        if isXml(f):
            parseXml(f)
            print "Success parsing " + f

    # after all items have been processed, write user tuples for
    # remaining bidderIDs that were not also sellerIDs
    writeNonSellers()

if __name__ == '__main__':
    main(sys.argv)
