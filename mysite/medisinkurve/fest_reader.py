#!/usr/bin/env python3
import pickle
from pathlib import Path
import os
abs_path = os.path.abspath(os.path.dirname(__file__))
import xml.etree.ElementTree as ET



'''
TODO:
'''

class Interaksjon():
    def __init__(self, oppfinteraksjon_xml_object):
        self.oppfinteraksjon_xml_object = oppfinteraksjon_xml_object
        self.ns = {'spam': "http://www.kith.no/xmlstds/eresept/m30/2014-12-01", 'spam2': "http://www.kith.no/xmlstds/eresept/forskrivning/2014-12-01"}
        self.tidspunkt              = None
        self.status                 = None
        self.relevans               = None      # Tuple (str:value, str:relevans)
        self.kliniskkonsekvens      = None
        self.interaksjonsmekanisme  = None
        self.kildegrunnlag          = None      # Tuple (str:value, str:kildegrunnlag)
        self.handtering             = None
        self.referanser             = []        # Contains tuples with (str:Kilde, str:Lenke). One may be None.
        self.substansgruppe1        = []        # Contains tuples with (str:ATC, str:virkestoff). One may be None
        self.substansgruppe2        = []        # Contains tuples with (str:ATC, str:virkestoff). One may be None
        self.register_data()

    def __str__(self):
        my_string = ""
        helper_dic = {  "interaksjonsmekanisme: ":      self.interaksjonsmekanisme,
                        "relevans: ":                   self.relevans,
                        "substansgruppe1":              self.substansgruppe1[0],
                        "substansgruppe2":              self.substansgruppe2[0]}
        for key, value in helper_dic.items():
            my_string += f"{key:20}" + str(value) + '\n'
        my_string += "\n"
        return my_string

    def register_data(self):
        if self.oppfinteraksjon_xml_object == None: 
            return
        tidspunkt = self.oppfinteraksjon_xml_object.find("spam:Tidspunkt", self.ns)
        if tidspunkt != None:
            self.tidspunkt = tidspunkt.text[0:10]            
        interaksjon = self.oppfinteraksjon_xml_object.find("spam:Interaksjon", self.ns)
        if interaksjon == None: 
            return
        relevans = interaksjon.find("spam:Relevans", self.ns)
        if relevans != None:
            self.relevans = (relevans.attrib['V'], relevans.attrib['DN'])
        kliniskkonsekvens = interaksjon.find("spam:KliniskKonsekvens", self.ns)
        if kliniskkonsekvens != None:
            self.kliniskkonsekvens = kliniskkonsekvens.text
        interaksjonsmekanisme = interaksjon.find("spam:Interaksjonsmekanisme", self.ns)
        if interaksjonsmekanisme != None:
            self.interaksjonsmekanisme = interaksjonsmekanisme.text
        kildegrunnlag = interaksjon.find("spam:Kildegrunnlag", self.ns)
        if kildegrunnlag != None:
            self.kildegrunnlag = (kildegrunnlag.attrib['V'], kildegrunnlag.attrib['DN'])
        handtering = interaksjon.find("spam:Handtering", self.ns)
        if handtering != None:
            self.handtering = handtering.text
        referanser = interaksjon.findall("spam:Referanse", self.ns)
        if referanser != None:
            for referanse in referanser:
                kilde = referanse.find("spam:Kilde", self.ns)
                lenke = referanse.find("spam:Lenke", self.ns)
                if kilde != None and lenke != None:
                    self.referanser.append((kilde.text, lenke.attrib['V']))
                elif kilde == None and lenke == None:
                    pass
                elif kilde == None:
                    self.referanser.append((kilde, lenke.attrib['V']))
                elif lenke == None:
                    self.referanser.append((kilde.text, lenke))
        substansgrupper = interaksjon.findall("spam:Substansgruppe", self.ns)
        substansgruppe1 = substansgrupper[0]
        substansgruppe2 = substansgrupper[1]
        for substans in substansgruppe1:
            virkestoff = substans.find("spam:Substans", self.ns)
            atc        = substans.find("spam:Atc", self.ns)
            if atc != None:
                virkestoff_text = atc.attrib['DN']
                atc_text        = atc.attrib['V']
                self.substansgruppe1.append((atc_text, virkestoff_text))
            elif virkestoff != None:
                virkestoff_text = virkestoff.text
                self.substansgruppe1.append((None, virkestoff_text))
        for substans in substansgruppe2:
            virkestoff = substans.find("spam:Substans", self.ns)
            atc        = substans.find("spam:Atc", self.ns)
            if atc != None:
                virkestoff_text = atc.attrib['DN']
                atc_text        = atc.attrib['V']
                self.substansgruppe2.append((atc_text, virkestoff_text))
            elif virkestoff != None:
                virkestoff_text = virkestoff.text
                self.substansgruppe2.append((None, virkestoff_text))


class Virkestoffmedstyrke():
    def __init__(self, virkestoffmedstyrke_object):
        self.ns = {'spam': "http://www.kith.no/xmlstds/eresept/m30/2014-12-01", 'spam2': "http://www.kith.no/xmlstds/eresept/forskrivning/2014-12-01"}
        self.register_data(virkestoffmedstyrke_object)

    def register_data(self, virkestoffmedstyrke_object):
        self.nevner_verdi, self.nevner_enhet = None, None
        styrke_teller = virkestoffmedstyrke_object.find("spam2:Styrke", self.ns)
        styrke_nevner = virkestoffmedstyrke_object.find("spam2:StyrkeNevner", self.ns)
        self.teller_verdi, self.teller_enhet = styrke_teller.attrib['V'], styrke_teller.attrib['U']
        if styrke_nevner != None: self.nevner_verdi, self.nevner_enhet = styrke_nevner.attrib['V'], styrke_nevner.attrib['U']


class LegemiddelMerkevare():
    def __init__(self, oppflegemiddelmerkevare_xml_object, root, idref_sortertvirkestoffmedstyrke):
        self.opflm = oppflegemiddelmerkevare_xml_object
        self.ns = {'spam': "http://www.kith.no/xmlstds/eresept/m30/2014-12-01", 'spam2': "http://www.kith.no/xmlstds/eresept/forskrivning/2014-12-01"}
        self.register_data(root)
        self.attach_virkestoffmedstyrke_data_to_oppflegemiddelmerkevare(idref_sortertvirkestoffmedstyrke)
        del self.opflm

    def register_data(self, root):
        lm = self.opflm.find("spam2:LegemiddelMerkevare", self.ns)
        self.navnformstyrke = lm.find("spam2:NavnFormStyrke", self.ns)  #Is never None
        self.varenavn = lm.find("spam2:Varenavn", self.ns)              #Is never None
        self.atcobj = lm.find("spam2:Atc", self.ns)                     #Is sometimes None
        administreringlegemiddel = lm.find("spam2:AdministreringLegemiddel", self.ns)
        self.atc, self.virkestoff, self.legemiddelform_kort_value = None, None, None
        self.sortertvirkestoffmedstyrker_id = []  #First item is string format of an integer designating the index of virkestoff, second item is IDREF.
        sortertvirkestoffmedstyrker = lm.findall("spam2:SortertVirkestoffMedStyrke", self.ns)
        if sortertvirkestoffmedstyrker != None: 
            for sortertvirkestoffmedstyrke in sortertvirkestoffmedstyrker:
                sorting_int = sortertvirkestoffmedstyrke.find("spam2:Sortering", self.ns).text
                idref_virkestoffmedstyrke = sortertvirkestoffmedstyrke.find("spam2:RefVirkestoffMedStyrke", self.ns).text
                self.sortertvirkestoffmedstyrker_id.append((sorting_int, idref_virkestoffmedstyrke))

        self.bare_ett_virkestoff = len(self.sortertvirkestoffmedstyrker_id) == 1

        if self.atcobj != None: 
            self.atc, self.virkestoff = self.atcobj.attrib['V'], self.atcobj.attrib['DN']
        self.legemiddelformkort = lm.find("spam2:LegemiddelformKort", self.ns)
        if self.legemiddelformkort != None:
            self.legemiddelform_kort_value = self.legemiddelformkort.attrib['DN']
        if administreringlegemiddel != None:
            self.administrasjonsveiobjects = administreringlegemiddel.findall("spam2:Administrasjonsvei", self.ns)
            try:
                self.administrasjonsveier = []
                for administrasjonsveiobject in self.administrasjonsveiobjects:
                    self.administrasjonsveier.append(administrasjonsveiobject.attrib['DN'])
            except Exception as e:
                print("Error in LegemiddelMerkevare.register_data(),", e)
            

    def attach_virkestoffmedstyrke_data_to_oppflegemiddelmerkevare(self, idref_sortertvirkestoffmedstyrke):
        self.virkestoffmedstyrker = []
        for index, idref in self.sortertvirkestoffmedstyrker_id:
            if idref in idref_sortertvirkestoffmedstyrke:
                self.virkestoffmedstyrker.append((index, idref_sortertvirkestoffmedstyrke[idref]))
            else: 
                self.virkestoffmedstyrker.append((index, None))
            

class FestData():
    '''
    Class that parses FEST-data from SLV (Statens legemiddelverk) and makes the xml-data useful for medisinkurve.no
    '''
    def __init__(self, fest_xml_source_filepath='./fest/fest251.xml'):
        #Initialize starting point for xml-parsing
        self.tree = ET.parse(fest_xml_source_filepath)
        self.root = self.tree.getroot()
        self.ns = {'spam': "http://www.kith.no/xmlstds/eresept/m30/2014-12-01", 'spam2': "http://www.kith.no/xmlstds/eresept/forskrivning/2014-12-01"}

        #Initialize lists
        self.legemiddelmerkevarer = []
        self.legemiddelformkortliste =  []

        #Initialize dicts
        self.merkenavn_ATC_dic_lowered = {}
        self.virkestoff_ATC_dic_lowered = {}
        self.merkenavn_virkestoff_dic_lowered = {}
        self.idref_sortertvirkestoffmedstyrke = {}  #Key is IDREF, value is instance of class Virkestoffmedstyrke

        #Fill in dicts
        self.fill_in_idref_sortervirkestoffmedstyrke()   
        self.make_ATC_dic_from_katlegemiddelmerkevare()
        self.make_ATC_dic_from_katlegemiddelvirkestoff()

        #Fill in lists
        self.make_legemiddelformkortliste()

        # Create placeholder katinteraksjon
        self.katInteraksjon = self.get_katinteraksjon_from_root()

        #Delete unecessary variables (saves a lot of time when serializing and de-serializing FestData()
        del self.tree
        del self.root
        del self.idref_sortertvirkestoffmedstyrke


    def fill_in_idref_sortervirkestoffmedstyrke(self):
        katvirkestoff = self.root.find("spam:KatVirkestoff", self.ns)
        for oppfvirkestoff in katvirkestoff:
            virkestoffmedstyrke = oppfvirkestoff.find("spam2:VirkestoffMedStyrke", self.ns)
            if virkestoffmedstyrke != None:
                idref = virkestoffmedstyrke.find("spam2:Id", self.ns)
                self.idref_sortertvirkestoffmedstyrke[idref.text] = Virkestoffmedstyrke(virkestoffmedstyrke)


    def get_oppflegemiddel_objects(self, atc, virkestoff, matching_word, merkenavn_bool, virkestoff_bool):
        list_of_hits = []

        def navnformstyrke_already_in_list(input_oppflegemiddelmerkevare):
            for item in list_of_hits:
                if input_oppflegemiddelmerkevare.navnformstyrke.text == item.navnformstyrke.text:
                    return True
            else: return False            

        if virkestoff_bool:
            #Returns objects that have identical atc
            for oppflegemiddelmerkevare in self.legemiddelmerkevarer:
                if atc != None and atc == oppflegemiddelmerkevare.atc:
                    if not navnformstyrke_already_in_list(oppflegemiddelmerkevare):
                        list_of_hits.append(oppflegemiddelmerkevare)
            return list_of_hits
        elif merkenavn_bool:
            #Returns objects that have (partially) matching varenavn and identical atc.
            for oppflegemiddelmerkevare in self.legemiddelmerkevarer:
                if atc != None and atc == oppflegemiddelmerkevare.atc:
                    if matching_word != None and matching_word.lower() in oppflegemiddelmerkevare.varenavn.text.lower(): 
                        if not navnformstyrke_already_in_list(oppflegemiddelmerkevare):
                            list_of_hits.append(oppflegemiddelmerkevare)
                elif virkestoff != None and oppflegemiddelmerkevare.virkestoff != None:
                    if virkestoff.lower() == oppflegemiddelmerkevare.virkestoff.lower():
                        if matching_word != None and matching_word.lower() in oppflegemiddelmerkevare.varenavn.text.lower(): 
                            if not navnformstyrke_already_in_list(oppflegemiddelmerkevare):
                                list_of_hits.append(oppflegemiddelmerkevare)
            
            return list_of_hits
        else:
            return None

    def get_katinteraksjon_from_root(self):
        print("Forsøker å kjøre get_katinteraksjon_from_root()")
        # tree = ET.parse(os.path.join(abs_path, 'fest/katinteraksjon.xml'))
        # root = tree.getroot()
        # ns = {'spam': "http://www.kith.no/xmlstds/eresept/m30/2014-12-01", 'spam2': "http://www.kith.no/xmlstds/eresept/forskrivning/2014-12-01"}
        katinteraksjon = self.root.find("spam:KatInteraksjon", self.ns)
        print("KatInteraksjon: ", katinteraksjon)
        if katinteraksjon == None:
            print("Fatal Error in get_katinteraksjon_from_root, Katinteraksjon was None.")
        return katinteraksjon

    def get_interaction_objects(self, input_atc, input_virkestoff):
        """Inputs ATC-name and virkestoff (representing a drug). One or both of them can be None.
        The function returns either None or a list of tuples. Each tuple contains 1 interaction object, 1 ID-string and 1 int.
        The possible values for int is 0 and 1. This ties the drug in question to the first (0) or second (1)
        substansgruppe. The ID-string correspons to the oppfinteraksjon-ID in the FEST-data."""
        if input_atc == None and input_virkestoff == None: return None
        oppfinteraksjon_hits = []
        if self.katInteraksjon == None: self.katInteraksjon = self.get_katinteraksjon()
        for oppfinteraksjon in self.katInteraksjon:
            oppfinteraksjon_ID = oppfinteraksjon.find("spam:Id", self.ns)
            interaksjon = oppfinteraksjon.find("spam:Interaksjon", self.ns)
            if interaksjon == None: continue   
     
            substansgrupper = interaksjon.findall("spam:Substansgruppe", self.ns)
            for index, substansgruppe in enumerate(substansgrupper):
                substanser = substansgruppe.findall("spam:Substans", self.ns)
                for substans in substanser:
                    atc = substans.find("spam:Atc", self.ns)
                    virkestoff = substans.find("spam:Substans", self.ns).text.lower()
                    if input_atc != None and atc != None and atc.attrib['V'] == input_atc:
                        oppfinteraksjon_hits.append((Interaksjon(oppfinteraksjon), oppfinteraksjon_ID.text, index))
                    elif input_virkestoff != None and virkestoff == input_virkestoff: 
                        oppfinteraksjon_hits.append((Interaksjon(oppfinteraksjon), oppfinteraksjon_ID.text, index))
        return oppfinteraksjon_hits

    def make_legemiddelformkortliste(self):
        katkodeverk = self.root.find("spam:KatKodeverk", self.ns)
        oppfkodeverk_lmformkort = None
        for oppfkodeverk in katkodeverk:
            info = oppfkodeverk.find("spam:Info", self.ns)
            if info.find("spam:Kortnavn", self.ns).text == 'Kortform':
                oppfkodeverk_lmformkort = oppfkodeverk
                break
        if oppfkodeverk_lmformkort == None: print("Could not find oppfkodeverk for legemiddelformkort in make_legemiddelformkortliste()")       
        else:
            for child in oppfkodeverk_lmformkort:
                if child.tag == "{" + self.ns['spam'] + "}" + "Element":
                    element = child
                    kode = element.find("spam:Kode", self.ns)
                    term = element.find("spam:Term", self.ns)
                    term2 = term.find("spam:Term", self.ns) #Note that Term2 is nested in Term
                    self.legemiddelformkortliste.append((kode.text, term2.text))

    def get_ultrashort_legemiddelform(self, lmform):
        my_dict = {"Tablett": "tbl", "Tyggetablett": "tyggetbl", "Depottablett": "depottbl", "Enterotablett": "ent.tbl",
        "Vaginaltablett": "vag.tbl", "Kapsel": "kapsel", "Depotkapsel": "dp.kpsl", "Infusjonsvæske": "inf.v.",
        "Injeksjonsvæske": "inj.v.", "Inhalasjonsvæske til nebulisator": "inh.v.", "Pulver til infusjonsvæske": "inf.v.",
        "Pulver til injeksjonsvæske": "inj.v.", "Inhalasjonsvæske": "inh.v", "Pulver til injeksjons-/infusjonsvæske": "inj.v.",
        "Injeksjonsvæske/konsentrat til infusjonsvæske": "inj.v.", "Injeksjons-/infusjonsvæske": "inj.v.",
        "Pulver og væske til infusjonsvæske": "inj.v.", "Pulver og væske til injeksjons-/infusjonsvæske": "inj.v.",
        "Pulver og væske til injeksjonsvæske": "inj.v.", "Pulver til konsentrat til infusjonsvæske": "inj.v.",
        "Pulver og væske til konsentrat til infusjonsvæske": "inj.v.", "Konsentrat til injeksjonsvæske": "inj.v.",
        "Konsentrat til infusjonsvæske": "inf.v.", "Konsentrat til injeksjons-/infusjonsvæske": "inj.v.",
        "Konsentrat og væske til infusjonsvæske": "inf.v.", "Infusjonsvæske/konsentrat til infusjonsvæske": "inf.v.",
        "Pulver til konsentrat til injeksjons-/infusjonsvæske": "inj.v.", "Konsentrat og væske til konsentrat til infusjonsvæske": "inf.v",
        "Pulver til konsentrat og væske til infusjonsvæske": "inf.v", "Sublingvalspray": "subl.spr", "Sublingvaltablett": "subl.tbl",
        "Mikstur": "mikst", "Rektalvæske": "rekt.v.", "Inhalasjonspulver": "inh.p.", "Depotplaster": "dept.plst",
        "Brusetablett": "brusetbl."}
        if lmform in my_dict:
            return my_dict[lmform]
        else:
            return lmform.lower()

    def make_ATC_dic_from_katlegemiddelmerkevare(self):
        katlegemiddelmerkevare = self.root.find("spam:KatLegemiddelMerkevare", self.ns)    
        for oppflmmerkevare in katlegemiddelmerkevare:
            lmmerkevare = oppflmmerkevare.find("spam2:LegemiddelMerkevare", self.ns)
            varenavn = lmmerkevare.find("spam2:Varenavn", self.ns)
            atc = lmmerkevare.find("spam2:Atc", self.ns)
            if atc != None: 
                self.merkenavn_ATC_dic_lowered[varenavn.text.lower()] = atc.attrib['V']
                self.virkestoff_ATC_dic_lowered[atc.attrib['DN'].lower()] = atc.attrib['V']
                self.merkenavn_virkestoff_dic_lowered[varenavn.text.lower()] = atc.attrib['DN'].lower()        
            else: 
                self.merkenavn_ATC_dic_lowered[varenavn.text.lower()] = None
            self.legemiddelmerkevarer.append(LegemiddelMerkevare(oppflmmerkevare, self.root, self.idref_sortertvirkestoffmedstyrke))         

    def make_ATC_dic_from_katlegemiddelvirkestoff(self):
        katlegemiddelvirkestoff = self.root.find("spam:KatLegemiddelVirkestoff", self.ns)
        for oppflegemiddelvirkestoff in katlegemiddelvirkestoff:
            lmvirkestoff = oppflegemiddelvirkestoff.find("spam2:LegemiddelVirkestoff", self.ns)
            atc = lmvirkestoff.find("spam2:Atc", self.ns)
            self.virkestoff_ATC_dic_lowered[atc.attrib['DN'].lower()] = atc.attrib['V'] 

    def get_ATC_from_virkestoff(self, virkestoff, allow_partial_hits=False):
        if virkestoff.lower() in self.virkestoff_ATC_dic_lowered: return self.virkestoff_ATC_dic_lowered[virkestoff.lower()]
        else: return None        

    def get_ATC_from_merkenavn(self, merkenavn, allow_partial_hits=False):
        if merkenavn.lower() in self.merkenavn_ATC_dic_lowered: return self.merkenavn_ATC_dic_lowered[merkenavn.lower()]
        elif allow_partial_hits:
            smallest_key = 10000
            for key, value in self.merkenavn_ATC_dic_lowered.items():
                if merkenavn.lower() in key: 
                    return value
        else: return None

    def get_virkestoff_from_merkenavn(self, merkenavn, allow_partial_hits=False):
        if merkenavn.lower() in self.merkenavn_virkestoff_dic_lowered: return self.merkenavn_virkestoff_dic_lowered[merkenavn.lower()]
        elif allow_partial_hits:
            for key, value in self.merkenavn_virkestoff_dic_lowered.items():
                if merkenavn.lower() in key: return value
        else: return None

    def get_virkestoff_from_virkestoff(self, virkestoff, allow_partial_hits=False):
        if virkestoff.lower() in self.virkestoff_ATC_dic_lowered: return virkestoff
        else: return None

    def get_virkestoff_from_merkenavn_or_virkestoff(self, merkenavn_or_virkestoff, allow_partial_hits=False):
        from_virkestoff = self.get_virkestoff_from_virkestoff(merkenavn_or_virkestoff, allow_partial_hits=allow_partial_hits)
        from_merkenavn  = self.get_virkestoff_from_merkenavn(merkenavn_or_virkestoff, allow_partial_hits=allow_partial_hits)
        if not from_merkenavn == None: return from_merkenavn
        else: return from_virkestoff

    def get_ATC_from_merkenavn_or_virkestoff(self, merkenavn_or_virkestoff, allow_partial_hits=False):
        from_virkestoff = self.get_ATC_from_virkestoff(merkenavn_or_virkestoff, allow_partial_hits=allow_partial_hits)
        from_merkenavn  = self.get_ATC_from_merkenavn(merkenavn_or_virkestoff, allow_partial_hits=allow_partial_hits)

        if not from_virkestoff == None: return from_virkestoff
        else: return from_merkenavn

    def get_ATC(self, raw_merkenavn_or_virkestoff, return_match=False):
        no_words = len(raw_merkenavn_or_virkestoff.split())
        #First trying to find exact hits
        for m in range(no_words):
            for i in range(no_words-m):        
                first_split = raw_merkenavn_or_virkestoff.split()[:(no_words-i)]
                second_split = first_split[m:]
                search_word = ' '.join(second_split)
                atc = self.get_ATC_from_merkenavn_or_virkestoff(search_word)
                if not atc == None: 
                    if return_match: return search_word
                    else: return atc
#        Now we're trying to find partial hits, e.g. that 'Relvar' will match with 'Rellvar Ellipta'. Use with caution
        for m in range(no_words):
            for i in range(no_words-m):        
                first_split = raw_merkenavn_or_virkestoff.split()[:(no_words-i)]
                second_split = first_split[m:]
                search_word = ' '.join(second_split)
                if len(search_word) < 6: break
                atc = self.get_ATC_from_merkenavn_or_virkestoff(search_word, allow_partial_hits=True)
                if not atc == None:
                    if return_match: return search_word
                    else: return atc
        return None

    def get_virkestoff(self, raw_merkenavn_or_virkestoff, return_match=False):
        no_words = len(raw_merkenavn_or_virkestoff.split())
        #First trying to find exact hits
        for m in range(no_words):
            for i in range(no_words-m):        
                first_split = raw_merkenavn_or_virkestoff.split()[:(no_words-i)]
                second_split = first_split[m:]
                search_word = ' '.join(second_split)
                virkestoff = self.get_virkestoff_from_merkenavn_or_virkestoff(search_word)
                if not virkestoff == None: 
                    if return_match: return search_word
                    else: return virkestoff

        #Now we're trying to find partial hits, e.g. that 'Relvar' will match with 'Rellvar Ellipta'. Use with caution
        for m in range(no_words):
            for i in range(no_words-m):        
                first_split = raw_merkenavn_or_virkestoff.split()[:(no_words-i)]
                second_split = first_split[m:]
                search_word = ' '.join(second_split)
                if len(search_word) < 6: break
                virkestoff = self.get_virkestoff_from_merkenavn_or_virkestoff(search_word, allow_partial_hits=True)
                if not virkestoff == None: return virkestoff
        return None

    def get_matching_word(self, raw_merkenavn_or_virkestoff):
        matching_word = self.get_ATC(raw_merkenavn_or_virkestoff, return_match=True)
        if matching_word != None: return matching_word
        matching_word = self.get_virkestoff(raw_merkenavn_or_virkestoff, return_match=True)
        return matching_word

    def matching_word_is_merkenavn_or_virkestoff(self, matching_word):
        merkenavn_bool  = False
        virkestoff_bool = False
        try:
            if matching_word == None: return merkenavn_bool, virkestoff_bool
            if matching_word.lower() in self.virkestoff_ATC_dic_lowered: virkestoff_bool = True
            if matching_word.lower() in self.merkenavn_virkestoff_dic_lowered: merkenavn_bool = True
            for key, value in self.merkenavn_virkestoff_dic_lowered.items():
                if matching_word.lower() in key:
                    merkenavn_bool = True
                    break
            return merkenavn_bool, virkestoff_bool
        except Exception as e:
            print("Error in FestData.matching_word_is_merkenavn_or_virkestoff", e)            

def get_festdata(make_new_anyways=False):
    print("running get_festdata()")
    abs_pickle_path = os.path.join(abs_path, 'fest/festdata.pickle')
    abs_xml_path = os.path.join(abs_path, 'fest/fest251.xml')
    my_file = Path(abs_pickle_path)

    def make_new_pickle_file():
        new_festdata = FestData(fest_xml_source_filepath=abs_xml_path)  
        with open(abs_pickle_path, 'wb') as f:
            pickle.dump(new_festdata, f)
        print('Lagde ny fest_data.') 
        return new_festdata              

    try:
        my_abs_path = my_file.resolve(strict=True)
        if make_new_anyways:
            print("Lager ny pickle-fil etter ordre fra kwargs i get_festdata() til tross for at pickle-filen allerede finnes")
            return make_new_pickle_file()
    except FileNotFoundError:
        print("festdata.pickle eksisterer ikke, forsøker å lage ny")
        return make_new_pickle_file()
    else:
        print('Prøver å åpne pickled festdata')
        try:
            with open(abs_pickle_path, 'rb') as f:
                old_festdata = pickle.load(f)
                print('Suksess, returnerer pickled festdata')
                return old_festdata
        except ModuleNotFoundError:
            new_festdata = FestData(fest_xml_source_filepath=abs_xml_path)    
            with open(abs_pickle_path, 'wb') as f:
                pickle.dump(new_festdata, f)
            print('Måtte lage ny fest_data og pickle på nytt. Virker som det var fordi .pickle-filen ble laget fra et annet program sist gang.') 
            return new_festdata
        except Exception as e:
            print('Warning, unexpected error in trying to retrieve festdata. Trying to make a new one')
            return make_new_pickle_file()

if __name__ == '__main__':
    festdata = get_festdata(make_new_anyways=False)
    festdata.get_interaction_objects(None, 'warfarin')