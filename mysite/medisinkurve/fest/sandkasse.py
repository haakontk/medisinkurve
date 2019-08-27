#!/usr/bin/env python3

import xml.etree.ElementTree as ET


tree = ET.parse('fest251.xml')
root = tree.getroot()
ns = {'spam': "http://www.kith.no/xmlstds/eresept/m30/2014-12-01", 'spam2': "http://www.kith.no/xmlstds/eresept/forskrivning/2014-12-01"}
katinteraksjon = root.find("spam:KatInteraksjon", ns)
marevan_atc = "B01AA03"
antall_marevan_hits = 0




try:
    for child in katinteraksjon:
        substansgruppe_liste = []
        
        for grandchild in child:
            if grandchild.tag == "{http://www.kith.no/xmlstds/eresept/m30/2014-12-01}Interaksjon":
                interaksjon = grandchild
                for child in interaksjon:
                    if child.tag == "{http://www.kith.no/xmlstds/eresept/m30/2014-12-01}Substansgruppe":
                        substansgruppe_liste.append(child)


        substansgruppe1 = substansgruppe_liste[0]
        substansgruppe2 = substansgruppe_liste[1]

        for child in substansgruppe1:
            for grandchild in child:
                if grandchild.tag == "{http://www.kith.no/xmlstds/eresept/m30/2014-12-01}Atc":
                    atc = grandchild
                    print(atc.attrib['V'])
                    if atc.attrib['V'] == marevan_atc:
                        antall_marevan_hits += 1


        for child in substansgruppe2:
            for grandchild in child:
                if grandchild.tag == "{http://www.kith.no/xmlstds/eresept/m30/2014-12-01}Atc":
                    atc = grandchild
                    print(atc.attrib['V'])
                    if atc.attrib['V'] == marevan_atc:
                        antall_marevan_hits += 1
except Exception as e:
    print(e)

print(antall_marevan_hits)

#class FestData():
#    '''
#    Class that parses FEST-data from SLV (Statens legemiddelverk) and makes the xml-data useful for medisinkurve.no
#    '''
#    def __init__(self, fest_xml_source_filepath='./fest/fest251.xml'):
#        #Initialize starting point for xml-parsing
#        self.tree = ET.parse(fest_xml_source_filepath)
#        self.root = self.tree.getroot()
#        self.ns = {'spam': "http://www.kith.no/xmlstds/eresept/m30/2014-12-01", 'spam2': "http://www.kith.no/xmlstds/eresept/forskrivning/2014-12-01"}


