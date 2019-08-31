#!/usr/bin/env python3
import csv
import itertools


'''Todo: 
'''



if __name__ == '__main__': 
    from fest_reader import FestData, get_festdata, LegemiddelMerkevare, Virkestoffmedstyrke
    from pdf_generator import lage_pdf
else: 
    from .fest_reader import FestData, get_festdata, LegemiddelMerkevare, Virkestoffmedstyrke
    from .pdf_generator import lage_pdf

class Medikament():
    """
    Hver instans av Medikament vil tilsvare en legemiddelrad i kurven.
    All info om legemiddelraden er tilknyttet instanset.
    """
    def __init__(self, **kwargs):
        self.raw_legemiddelinput    = ''
        self.legemiddelnavn         = ''
        self.legemiddel_id          = ''
        self.legemiddelform         = ''
        self.enhet                  = ''
        self.administrasjonsform    = ''
        self.dose0008, self.dose0814, self.dose1420, self.dose2024, self.dose_fritekst = '', '', '', '', ''
        self.ny                     = False
        self.fast_medisin           = True

        if 'raw_legemiddelinput' in kwargs: self.raw_legemiddelinput = kwargs['raw_legemiddelinput']
        if 'legemiddelnavn' in kwargs: self.legemiddelnavn = kwargs['legemiddelnavn']
        if 'legemiddel_id' in kwargs: self.legemiddel_id = kwargs['legemiddel_id']
        if 'legemiddelform' in kwargs: self.legemiddelform = kwargs['legemiddelform']
        if 'enhet' in kwargs: self.enhet = kwargs['enhet']
        if 'administrasjonsform' in kwargs: self.administrasjonsform = kwargs['administrasjonsform']
        if 'dose0008' in kwargs: self.dose0008 = kwargs['dose0008']
        if 'dose0814' in kwargs: self.dose0814 = kwargs['dose0814']
        if 'dose1420' in kwargs: self.dose1420 = kwargs['dose1420']
        if 'dose2024' in kwargs: self.dose2024 = kwargs['dose2024']
        if 'dose_fritekst' in kwargs: self.dose_fritekst = kwargs['dose_fritekst']
        if 'ny_medisin' in kwargs: self.ny = kwargs['ny_medisin']
        if 'fast_medisin' in kwargs: self.fast_medisin = kwargs['fast_medisin']

        self.atc                    = None
        self.virkestoff             = None
        self.matching_word          = None      #This will become the part of raw_legemiddelinput that gave a hit in the ATC- or virkestoff-dicts in festdata.
        self.interaction_objects    = None      #If this remains None then the program unsucessfully tried to find interactions.
                                                #If it becomes an empty list the program sucessfully ruled out interactions.
        self.virkestoff_bool        = False
        self.merkenavn_bool         = False
        self.matching_legemiddelmerkevarer = None
        self.vesp                   = False
        self.no_of_times_a_day      = None
        self.equal_doses_each_day   = False
        self.unequal_doses_each_day = False
        self.floats_in_raw_input    = None
        self.multi_substance        = False
        self.proportion_of_tablet   = None      #Hvis input er 50mg og det finnes bare en tablett på 100mg blir denne verdien 0.5
        self.allow_proportions      = False     #True hvis det er lov med halve og doble tabletter. False hvis ikke.
        self.autofill_completed     = False
        self.kompaktdose            = self._make_compact_dose()

    def __str__(self):
        my_string = ""
        helper_dic = {  "input: ":              self.raw_legemiddelinput,
                        "fast: ":               self.fast_medisin,
                        "atc: ":                self.atc,
                        "virkestoff: ":         self.virkestoff,
                        "matching_word: ":      self.matching_word,
                        "legemiddelnavn: ":     self.legemiddelnavn,
                        "virkestoff_bool: ":    self.virkestoff_bool,
                        "merkenavn_bool: ":     self.merkenavn_bool,
                        "legemiddelform: ":     self.legemiddelform,
                        "no of times a day: ":  self.no_of_times_a_day,
                        "vesp: ":               self.vesp,
                        "proportion_of_tbl: ":  self.proportion_of_tablet,
                        "enhet: ":              self.enhet,
                        "adm_form: ":           self.administrasjonsform,
                        "multi_substance: ":    self.multi_substance,         
                        "dose0008: ":           self.dose0008,
                        "dose0814: ":           self.dose0814,
                        "dose1420: ":           self.dose1420,
                        "dose2024: ":           self.dose2024,
                        "dosefritekst: ":       self.dose_fritekst,
                        "autofill_success: ":   self.autofill_completed}
        for key, value in helper_dic.items():
            my_string += f"{key:20}" + str(value) + '\n'
        try:
            for oppflm in self.matching_legemiddelmerkevarer:
                my_string += oppflm.navnformstyrke.text + "\n"
        except Exception as e:
            print("Error in Medikament.__str__()", e)
        my_string += "\n"
        return my_string

    def init_autofill(self, festdata):
        def _common_tasks():
            self.refine_matches_based_on_floats()
            self.remove_similar_entries_in_lmmerkevarer()
            self.check_if_multi_substance_drug()
            self.try_to_fill_inn_legemiddelform(festdata)
            self.try_to_fill_in_enhet()
            self.find_proportion_of_tablet()
            self.try_to_fill_in_doses()
            self.try_to_fill_in_adm_mate()

        self.find_matching_legemiddelmerkevarer(festdata)
        if self.matching_legemiddelmerkevarer != None:
            if self.fast_medisin:
                self.refine_matching_legemiddelmerkevarer()
                self.get_no_of_times_a_day()                
                if self.equal_doses_each_day: self.find_non_no_of_times_a_day_floats()
                _common_tasks()
            else:
                self.refine_matching_legemiddelmerkevarer()
                _common_tasks()                
        if self.matching_legemiddelmerkevarer == None or self.matching_legemiddelmerkevarer == []: self.legemiddelnavn = self.raw_legemiddelinput
        self.check_if_autofill_is_successful()
        if self.autofill_completed == True: self._make_compact_dose()

    def find_non_no_of_times_a_day_floats(self):
        try:
            no_of_times_string = self.get_no_of_times_string()
            modified_input_string = self.get_modified_raw_input(self.raw_legemiddelinput, no_of_times_string)
            self.non_no_of_times_floats_in_input = self._get_floats_from_string(modified_input_string)
        except Exception as e:
            print("Warning in find_non_no_of_times_a_day_floats()", e, "legemiddelinput: ", self.raw_legemiddelinput)
            self.non_no_of_times_floats_in_input = None

    def check_if_autofill_is_successful(self):
        if self.fast_medisin:
            if all(dose == '' for dose in [self.dose0008, self.dose0814, self.dose1420, self.dose2024]):
                return
            elif any(thing == None or thing == '' for thing in [self.atc, self.matching_legemiddelmerkevarer, self.enhet, self.administrasjonsform]):
                return
            else:
                self.autofill_completed = True
        else:
            if any(thing == None or thing == '' for thing in [self.atc, self.matching_legemiddelmerkevarer, self.enhet, self.administrasjonsform]):
                return
            else:
                self.autofill_completed = True

    def check_if_multi_substance_drug(self):
        longest = 1
        try:
            for lmmerkevare in self.matching_legemiddelmerkevarer:
                if len(lmmerkevare.virkestoffmedstyrker) > longest: longest = len(lmmerkevare.virkestoffmedstyrker)
            if longest > 1: self.multi_substance = True
        except Exception as e:
           print("Error in Medikament.check_if_multi_substance_drug()", e) 

    def find_proportion_of_tablet(self):
        #Checking that we only have 1 item in matching_legemiddelmerkevarer and that it's a tablett.
        if len(self.matching_legemiddelmerkevarer) == 1 and self.matching_legemiddelmerkevarer[0].virkestoffmedstyrker[0][1].nevner_verdi == None:
            self.allow_proportions = True
            no_of_times_string = self.get_no_of_times_string()
            if no_of_times_string != None:
                raw_lm_input_without_no_of_times = self.get_modified_raw_input(self.raw_legemiddelinput, no_of_times_string)
                if len(self.matching_legemiddelmerkevarer[0].virkestoffmedstyrker) == 1:    #True if metoprolol 10, false if Targiniq 10/5
                    try:
                        lmmerkevare_floats = self._get_floats_from_string(self.matching_legemiddelmerkevarer[0].navnformstyrke.text)
                        raw_lm_input_floats = self._get_floats_from_string(raw_lm_input_without_no_of_times)
                        proportions = []
                        for lm_float in lmmerkevare_floats:
                            if lm_float in raw_lm_input_floats:
                                proportions.append(1)
                            if lm_float in [a/2 for a in raw_lm_input_floats]:
                                proportions.append(2)
                            if lm_float in [a*2 for a in raw_lm_input_floats]:
                                proportions.append(0.5)
                        proportions = list(set(proportions))
                        if len(proportions) == 1: self.proportion_of_tablet = proportions[0]
                    except Exception as e:
                        print("Error in Medikament.find_proportion_of_tablet(),", e)
                else:
                    pass #Make code here for multi-substance drugs

    def remove_similar_entries_in_lmmerkevarer(self):
        '''This will for example remove 'Glucophage Tab 500mg' if 'Metformin Tab 500mg' also is in the list'''

        def remove_stikkpiller_if_tabs_are_present(formulation_doses, refined_matching_lm_merkevarer):
            non_stikk_pille_matching_lmmerkevarer = []
            if any(e[1] == 'Tablett' for e in formulation_doses) and any(e[1] == 'Stikkpille' for e in formulation_doses):
                for form_dose, lmmerkevare in zip(formulation_doses, refined_matching_lm_merkevarer):
                    if form_dose[1] != 'Stikkpille':
                        non_stikk_pille_matching_lmmerkevarer.append(lmmerkevare)
                return non_stikk_pille_matching_lmmerkevarer
            else: return refined_matching_lm_merkevarer

        formulation_doses = [] #En enhet i denne listen er for eksempel ['Tab', '500']
        refined_matching_lm_merkevarer = []
        if self.matching_legemiddelmerkevarer != None:
            for lmmerkevare in self.matching_legemiddelmerkevarer:
                try:
                    if len(lmmerkevare.virkestoffmedstyrker) == 1:  #Only single active substances
                        styrke = lmmerkevare.virkestoffmedstyrker[0][1].teller_verdi
                        if styrke != None: 
                            entry = [styrke, lmmerkevare.legemiddelform_kort_value]
                            if entry not in formulation_doses:
                                formulation_doses.append(entry)
                                refined_matching_lm_merkevarer.append(lmmerkevare)
                    else:
                        pass #Make code here for multiple active substances.

                    if len(refined_matching_lm_merkevarer) > 0: self.matching_legemiddelmerkevarer = remove_stikkpiller_if_tabs_are_present(formulation_doses, refined_matching_lm_merkevarer)

                except Exception as e:
                    print("Error in Medikament.remove_similar_entries_in_lmmerkevarer()", e)

    def try_to_fill_in_adm_mate(self):

        def all_administrasjonsveier_in_matches_are_equal():
            if len(self.matching_legemiddelmerkevarer) == 0:
                return False
            else:
                first_adminvei = self.matching_legemiddelmerkevarer[0].administrasjonsveier
                for index, matching_legemiddel in enumerate(self.matching_legemiddelmerkevarer):
                    if index == 0: continue
                    if not self.matching_legemiddelmerkevarer[index].administrasjonsveier == first_adminvei:
                        return False
            return True

        helper_dic =    {"Oral bruk": "p.o.",
                        "Bruk på hud": "hud",
                        "Intravenøs bruk": "i.v.",
                        "Rektal bruk": "supp",
                        "Vaginal bruk": "vag",
                        "Nasal bruk": "nese",
                        "Subkutan bruk": "s.c.",
                        "Transdermal bruk": "hud",
                        "Okulær bruk": "øye",
                        "Sublingval bruk": "subl.",
                        "Intramuskulær bruk": "i.m.",
                        "Bruk til inhalasjon": "inh.",
                        "Bruk på hud": "hud"}
        try:
            if len(self.matching_legemiddelmerkevarer) < 3:
                if not all_administrasjonsveier_in_matches_are_equal():
                    return
                adminveier = self.matching_legemiddelmerkevarer[0].administrasjonsveier
                if all(adminvei != None for adminvei in adminveier) and len(adminveier) in [1,2]:
                    forkortet_adminveier = [helper_dic[adminvei] for adminvei in adminveier]
                    self.administrasjonsform = '/'.join(forkortet_adminveier)
                else:
                    print("lm_admform is None or not in adm_form helper_dic")
        except Exception as e:
            print("Error in Medikament.try_to_fill_in_adm_mate()", e)

    def remaining_matches_have_equal_legemiddelform(self):
        try:
            if self.matching_legemiddelmerkevarer == None: return False
            elif self.matching_legemiddelmerkevarer == []: return False
            else:
                #Prøver nå å finne forskjellige legemiddelformer
                first_legemiddelform = self.matching_legemiddelmerkevarer[0].legemiddelform_kort_value
                for legemiddelmerkevare in self.matching_legemiddelmerkevarer:
                    if legemiddelmerkevare.legemiddelform_kort_value != first_legemiddelform:
                        return False
            return True
        except Exception as e:
            print("Error in Medikament.remaining_matches_have_equal_legemiddelform() ", e)
            return False

    def try_to_fill_in_doses(self):
        '''This function fills in doses0008, etc. It also fills in the unit'''
        def _validate_that_floats_in_legemiddel_are_in_input():
            try:
                virkestoffmedstyrker_med_index = self.matching_legemiddelmerkevarer[0].virkestoffmedstyrker
                virkestoffmedstyrker_uten_index = [item[1] for item in virkestoffmedstyrker_med_index]
                for virkestoffmedstyrke in virkestoffmedstyrker_uten_index:
                    if virkestoffmedstyrke.nevner_verdi == None: #Sant hvis legemidlet ikke er en konsentrasjon
                        #Making all commas to punctuantions in legemiddelinput so that 2.5 and 2,5 are considered the same
                        non_comma_raw_legemiddelinput = ""
                        for char in self.raw_legemiddelinput:
                            if char == ',':
                                non_comma_raw_legemiddelinput += '.'
                            else:
                                non_comma_raw_legemiddelinput += char
                        if str(virkestoffmedstyrke.teller_verdi) not in non_comma_raw_legemiddelinput: #Sant hvis man f eks skriver Albyl-E 76 mg istedenfor 75.
                            if self.non_no_of_times_floats_in_input != None:
                                if len(self.non_no_of_times_floats_in_input) != 0:
                                    return False
                return True
            except Exception as e:
                print("Error in _validate_that_floats_in_legemiddel_are_in_input()", e)
                return False         

        def _helper_func3():
            #This function runs only for behovs-medisiner
            remaining_string_from_first_number = ''
            for index, char in enumerate(self.raw_legemiddelinput):                
                if char in [str(i) for i in range(9)]:
                    remaining_string_from_first_number = self.raw_legemiddelinput[index:]
                    break
            self.dose_fritekst = remaining_string_from_first_number                     

        def _helper_func2(doses):
            if all(f.is_integer() for f in doses): doses = [int(f) for f in doses]
            new_doses = []
            for dose in doses:
                if dose == 0 or dose == '0':
                    new_doses.append('')
                else:   
                    new_doses.append(dose)
            doses = new_doses
            if self.vesp: self.dose2024 = str(doses[0])
            elif self.no_of_times_a_day == 1: 
                self.dose0008 = str(doses[0])
            elif self.no_of_times_a_day == 2: 
                self.dose0008 = str(doses[0])
                self.dose2024 = str(doses[1])
            elif self.no_of_times_a_day == 3: 
                self.dose0008 = str(doses[0])
                self.dose1420 = str(doses[1])
                self.dose2024 = str(doses[2])
            elif self.no_of_times_a_day == 4: 
                self.dose0008 = str(doses[0])
                self.dose0814 = str(doses[1])
                self.dose1420 = str(doses[2])
                self.dose2024 = str(doses[3])

        def _helper_func1(floats_in_input=None):
            if not self.multi_substance:
                #Her kjører vi legemiddelstyrken i doseringsfeltet, istedenfor å skrive antall tabletter i doseringsfeltet.
                try:
                    if len(self.matching_legemiddelmerkevarer) > 0:
                        virkestoffmedstyrke = self.matching_legemiddelmerkevarer[0].virkestoffmedstyrker[0][1]
                        if virkestoffmedstyrke.nevner_verdi == None: #Sant hvis legemidlet ikke er en konsentrasjon
                            if virkestoffmedstyrke.teller_enhet == 'mikrog': self.enhet = 'mcg'
                            else: self.enhet = virkestoffmedstyrke.teller_enhet
                            if floats_in_input == None: 
                                doses = [float(virkestoffmedstyrke.teller_verdi) for i in range(4)] 
                            else: 
                                doses = floats_in_input
                            if self.proportion_of_tablet != None: doses = [i*self.proportion_of_tablet for i in doses]
                            _helper_func2(doses)
                        else: #Sant hvis legemidlet er en konsentrasjon
                            #Her her det litt farlig å programmere generelt. Velger derfor å progge vanlige special cases, f eks "duphalac
                            pass                                
                except Exception as e:
                    print("Error in Medikament._helper_func1() first error step,", e)
            else:
                #Denne fyrer hvis vi f eks har Calcigran Forte 1000/800. Da er det mer logisk å skrive antall tabletter i dosering.
                try:
                    virkestoffmedstyrke = self.matching_legemiddelmerkevarer[0].virkestoffmedstyrker[0][1]
                    if virkestoffmedstyrke.nevner_verdi == None: #Sant hvis legemidlet ikke er en konsentrasjon
                        #Finne ut av enhet
                        lm_enhet = self.matching_legemiddelmerkevarer[0].legemiddelform_kort_value
                        if "inhal" in lm_enhet.lower(): self.enhet = "dose"
                        elif "tbl" in self.legemiddelform.lower(): self.enhet = "tbl"
                        else: 
                            if self.legemiddelform != None:
                                self.enhet = self.legemiddelform
                        #Finne ut av legemiddelnavn. Vil at 'Targiniq' blir til 'Targiniq 10/5'.
                        lmmerkevare = self.matching_legemiddelmerkevarer[0]
                        antall_virkestoff = len(lmmerkevare.virkestoffmedstyrker)
                        styrke_floats = []      #Skal bli [10, 5] hvis input er 'Targiniq 10/5'
                        teller_verdier = []
                        for i in range(antall_virkestoff):
                            virkestoffmedstyrke = lmmerkevare.virkestoffmedstyrker[i][1]
                            styrke_floats.append(virkestoffmedstyrke.teller_verdi)
                            teller_verdier.append(virkestoffmedstyrke.teller_enhet)
                            samlet_liste = [a+b for a, b in zip(styrke_floats, teller_verdier)]
                        if any(item == None for item in styrke_floats):
                            pass
                        else:
                            self.legemiddelnavn += ' ' + '/'.join(samlet_liste)                            
                        #Finner ut av dosering
                        floats_in_lmmerkevare = self._get_floats_from_string(self.matching_legemiddelmerkevarer[0].navnformstyrke.text)
                        no_of_times_string = self.get_no_of_times_string()
                        modified_input_string = self.get_modified_raw_input(self.raw_legemiddelinput, no_of_times_string)
                        floats_in_input = self._get_floats_from_string(modified_input_string)
                        if len(floats_in_input) == len(floats_in_lmmerkevare)+1:
                            doses = [floats_in_input[-1] for _ in range(4)]                            
                        elif len(floats_in_input) == len(floats_in_lmmerkevare) or len(floats_in_input) == 0:
                            doses = [float(1) for _ in range(4)]
                        _helper_func2(doses)
                except Exception as e:
                    print("Error in Medikament._helper_func1() second error step", e)

        def _unusual_dosing():
            try:
                items = ['x1','x2','x3','x4','x 1','x 2','x 3','x 4', '+', 'vesp', 'kveld']
                if not any(item in self.raw_legemiddelinput.lower() for item in items):
                    return True
                return False    
            except Exception as e:
                print("Error in Medikament._unusual_dosing(),", e)
      
        def _fill_in_enhet():
            try:
                if len(self.matching_legemiddelmerkevarer) == 1:
                    if not self.multi_substance:
                        virkestoffmedstyrke = self.matching_legemiddelmerkevarer[0].virkestoffmedstyrker[0][1]
                        if virkestoffmedstyrke.nevner_verdi == None: #Sant hvis legemidlet ikke er en konsentrasjon
                            if virkestoffmedstyrke.teller_enhet == 'mikrog': self.enhet = 'mcg'
                            else: self.enhet = virkestoffmedstyrke.teller_enhet
            except Exception as e:
                print("Error in Medikament._fill_in_enhet(),", e)                        
            

        #Er det kun 1 match?? Høy sannsynlighet for at det er riktig legemiddel og dose
        one_match = len(self.matching_legemiddelmerkevarer) in [1]
        less_than_tree_matches = len(self.matching_legemiddelmerkevarer) in [1,2,3]

        if self.fast_medisin:
            if self.remaining_matches_have_equal_legemiddelform():
                if _unusual_dosing():
                    _fill_in_enhet()
                elif (self.equal_doses_each_day and one_match) or (not self.equal_doses_each_day and less_than_tree_matches):
                    if not _validate_that_floats_in_legemiddel_are_in_input():
                        return
                    if self.equal_doses_each_day:
                        _helper_func1()
                    elif self.unequal_doses_each_day:
                        try:
                            floats_in_input = self._get_floats_from_string(self.raw_legemiddelinput.lower())
                            no_of_plus = self.raw_legemiddelinput.lower().count('+')
                            self.no_of_times_a_day = no_of_plus+1
                            floats_in_input = floats_in_input[-(no_of_plus+1):]
                            _helper_func1(floats_in_input=floats_in_input)
                        except Exception as e:
                            print("Error in try_to_fill_in_doses, in class KurveArk", e)
        else:
            if self.remaining_matches_have_equal_legemiddelform(): _helper_func1()
            _helper_func3()

    def find_matching_legemiddelmerkevarer(self, festdata):
        self.matching_legemiddelmerkevarer = festdata.get_oppflegemiddel_objects(self.atc, 
                                                                                self.virkestoff,
                                                                                self.matching_word, 
                                                                                self.merkenavn_bool, 
                                                                                self.virkestoff_bool)

    def get_no_of_times_a_day(self):
        if 'vesp' in self.raw_legemiddelinput.lower() or 'kveld' in self.raw_legemiddelinput.lower(): 
            self.vesp = True
            self.no_of_times_a_day = 1
            self.equal_doses_each_day = True
        if 'x1' in self.raw_legemiddelinput.lower() or 'x 1' in self.raw_legemiddelinput.lower():
            self.no_of_times_a_day = 1
            self.equal_doses_each_day = True
        elif 'x2' in self.raw_legemiddelinput.lower() or 'x 2' in self.raw_legemiddelinput.lower(): 
            self.no_of_times_a_day = 2
            self.equal_doses_each_day = True
        elif 'x3' in self.raw_legemiddelinput.lower() or 'x 3' in self.raw_legemiddelinput.lower(): 
            self.no_of_times_a_day = 3
            self.equal_doses_each_day = True
        elif 'x4' in self.raw_legemiddelinput.lower() or 'x 4' in self.raw_legemiddelinput.lower(): 
            self.no_of_times_a_day = 4
            self.equal_doses_each_day = True
        elif '+' in self.raw_legemiddelinput.lower():
            self.unequal_doses_each_day = True

    def _get_floats_from_string(self, inputstring):
        new_list = []
        intermediate_list = []
        for index, char in enumerate(inputstring):
            if char.isdigit() or char == '.' or char == ',':
                intermediate_list.append((index, char))
        number = ""
        last_valid_pos = -1
        final_list = []
        for pos, char in intermediate_list:
            if number != "" and pos != last_valid_pos+1:            
                final_list.append(float(number))
                number = ""
            if char.isdigit():
                last_valid_pos = pos
                number += char
            elif last_valid_pos != -1:
                if pos == last_valid_pos+1:
                    number += '.'
                    last_valid_pos = pos
        if number != "":
            final_list.append(float(number))
        return final_list

    def get_modified_raw_input(self, inputstring, hit_string):
        #Returns raw_legemiddelinput_without_no_of_times
        if hit_string == None: return inputstring
        index = inputstring.find(hit_string)
        if len(inputstring) > (index + len(hit_string)):
            new_string = inputstring[:index] + inputstring[(index+len(hit_string)):]
        else:
            new_string = inputstring[:index]
        return new_string

    def get_no_of_times_string(self):
        try:
            if self.equal_doses_each_day:
                string1, string2 = 'x' + str(self.no_of_times_a_day), 'x ' + str(self.no_of_times_a_day)
                index1 = self.raw_legemiddelinput.lower().find(string1)
                index2 = self.raw_legemiddelinput.lower().find(string2)

                if index1 != -1:
                    no_of_times_string = string1
                elif index2 != -1:
                    no_of_times_string = string2
                elif self.vesp == True:
                    no_of_times_string = None
                return no_of_times_string
            else: return None
        except Exception as e:
            print("Error in Medikament.get_no_of_times_string(),", e)

    def refine_matches_based_on_floats(self):
        '''Gets relevant floats in the input and uses them to refine the possible legemiddel-hits.'''
        try:
            if self.equal_doses_each_day:
                raw_legemiddelinput_without_no_of_times = self.get_modified_raw_input(self.raw_legemiddelinput.lower(), self.get_no_of_times_string())
                self.floats_in_raw_input = self._get_floats_from_string(raw_legemiddelinput_without_no_of_times)
                #Now lets try to refine matching legemiddelmerkevarer again
            else: 
                self.floats_in_raw_input = self._get_floats_from_string(self.raw_legemiddelinput.lower())
            self.refine_matching_legemiddelmerkevarer()        
        except Exception as e:
            print("Non-fatal Error in Medikament.refine_matches_based_on_floats(),", e)


    def refine_matching_legemiddelmerkevarer(self):
        '''This function is supposed to remove hits in matching_legemiddelmerkevarer that cannot possibly match due to dosage, formulation etc.
           For example: 'paracetamol tbl 1g x 4' would produce a hit for liquid paracet formulations. 
           Neste oppgave er å forsøke å finne legemiddelform i raw_legemiddelinput, feks "tbl", "inj.v." osv.
        '''

        #This section will reduce the possible legemiddelmerkevarehits if the raw_input contains a legemiddelform that is found in the legemiddelvaremerker-list
        try:
            my_dict_priority = {"depot": "depot"}
            my_dict = {"tbl": "tablett",
                        "tbl.": "tablett", 
                        "enterotbl.": "enterotablett",
                        "tab": "tablett",
                        "brusetbl.": "brusetablett",
                        "t": "tablett", 
                        "inj": "væske", 
                        "væske": "væske",
                        "inj.v.": "væske",
                        "inf": "væske",
                        "inf.v": "væske",
                        "inf.v.": "væske",
                        "kapsel": "kapsel",
                        "kpsl": "kapsel",
                        "kps": "kapsel", 
                        "plaster": "plaster",
                        "mikstur": "mikstur",
                        "depottbl.": "depottablett"}
            new_list = []
            legemiddelform_found_in_input = False
            for key in my_dict_priority:
                if key in self.raw_legemiddelinput.lower():
                    legemiddelform_found_in_input = True
                    correct_form = my_dict_priority[key]
                    for legemiddelmerkevare in self.matching_legemiddelmerkevarer:
                        if correct_form in legemiddelmerkevare.legemiddelform_kort_value.lower():
                            new_list.append(legemiddelmerkevare)
            if len(new_list) == 0:
                for word in self.raw_legemiddelinput.split():
                    if word in my_dict:
                        legemiddelform_found_in_input = True
                        correct_form = my_dict[word.lower()]
                        for legemiddelmerkevare in self.matching_legemiddelmerkevarer:
                            if correct_form in legemiddelmerkevare.legemiddelform_kort_value.lower():
                                new_list.append(legemiddelmerkevare)
            if legemiddelform_found_in_input: 
                self.matching_legemiddelmerkevarer = new_list
            enhanced_hits_list = []
            exact_hits_list = []
            drugs_with_concentrations = []
            if self.floats_in_raw_input != None:

                if len(self.floats_in_raw_input) != 0:
                    #Lager en modifisert floats_in_raw_input for å ta høyde for deling av tabletter eller f eks at 2 tbl a 50mg kan passe med 100mg
                    enhanced_floats_in_raw_input = []
                    exact_floats_in_raw_input = self.floats_in_raw_input
                    for float_number in self.floats_in_raw_input:
                        enhanced_floats_in_raw_input.append(float_number/2)
                        enhanced_floats_in_raw_input.append(float_number)
                        enhanced_floats_in_raw_input.append(float_number*2)
                    for legemiddelmerkevare in self.matching_legemiddelmerkevarer:
                        drug_float_not_found_in_exact_raw_input = False
                        drug_float_not_found_in_enhanced_raw_input = False
                        floats_in_legemiddelmerkevare = self._get_floats_from_string(legemiddelmerkevare.navnformstyrke.text.lower())
                        #Nå skal jeg sjekke om alle doser i lmmerkevare gjenfinnes i raw_input_floats
                        for lmmerkevare_float in floats_in_legemiddelmerkevare:
                            if lmmerkevare_float not in enhanced_floats_in_raw_input:
                                drug_float_not_found_in_enhanced_raw_input = True
                            if lmmerkevare_float not in exact_floats_in_raw_input:
                                drug_float_not_found_in_exact_raw_input = True                        
                        if legemiddelmerkevare.virkestoffmedstyrker[0][1].nevner_verdi != None: #Vi tør ikke ekskludere konsentrasjoner.
                            if not legemiddelmerkevare.legemiddelform_kort_value == "Depotplaster": #Vi tør likevel å ekskludere depotplastere
                                drugs_with_concentrations.append(legemiddelmerkevare)                        
                        if not drug_float_not_found_in_exact_raw_input: exact_hits_list.append(legemiddelmerkevare) #If this is true we have found an exact hit
                        elif not drug_float_not_found_in_enhanced_raw_input: enhanced_hits_list.append(legemiddelmerkevare)
            #Dersom det finnes konsentrasjonsdrugs skal jeg ikke bruke floats til å snevre inn mulige matches
            if len(drugs_with_concentrations) > 0: pass
            elif len(exact_hits_list) > 0: self.matching_legemiddelmerkevarer = exact_hits_list
            elif len(enhanced_hits_list) > 0: self.matching_legemiddelmerkevarer = enhanced_hits_list
        except Exception as e:
            print("Error in Medikament.refine_matching_legemiddelmerkevarer(),", e)

    def try_to_fill_in_enhet(self):
        '''Denne funksjonen prøver å fylle inn enhet dersom dette ikke allerede er gjort
            og dersom alle mulige hits har samme enhet og dersom ingen av de er en konsentrasjon'''
        try:
            if self.enhet != '':
                return
            elif self.matching_legemiddelmerkevarer == None:
                return
            elif len(self.matching_legemiddelmerkevarer) == 0:
                return
            else:
                enheter = []
                for legemiddelmerkevare in self.matching_legemiddelmerkevarer:
                    if legemiddelmerkevare.virkestoffmedstyrker[0][1] != None:
                        if legemiddelmerkevare.virkestoffmedstyrker[0][1].nevner_verdi != None: return #Vi dropper det hvis det er en konsentrasjon
                        else:
                            enheter.append(legemiddelmerkevare.virkestoffmedstyrker[0][1].teller_enhet)
                if len(set(enheter)) == 1: #Sant hvis alle mulige matches har samme enhet, f eks "mg"
                    self.enhet = enheter[0]
        except Exception as e:
            print("Non-fatal Error in Medikament.try_to_fill_in_enhet(),", e)

    def try_to_fill_inn_legemiddelform(self, festdata):
        #Prøver å hente ut legemiddelform fra mulige legemiddelmerkevarehits
        formuleringer = []
        try:
            #Sjekker spesialkasus først
            if (self.atc, self.virkestoff, self.legemiddelnavn.lower()) == ('A06AD65', 'makrogol, kombinasjoner', 'movicol'): 
                self.legemiddelform = 'mikst'
                self.administrasjonsform = 'p.o.'

            #Sjekker først at det er en match mellom input og mulige hits
            for legemiddelmerkevare in self.matching_legemiddelmerkevarer:
                formuleringer.append(legemiddelmerkevare.legemiddelform_kort_value)
            unique_formuleringer = set(formuleringer)
            if(len(unique_formuleringer)) in [1,2,3]: 
                unique_ultrashort_formulations = []
                for i in range(len(unique_formuleringer)):
                    unique_ultrashort_formulations.append(festdata.get_ultrashort_legemiddelform(formuleringer[i]))#Henter korte legemiddelformer, ie "Tablett" blir "tbl"
#                print(unique_formuleringer, unique_ultrashort_formulations)
                my_dict_words   = {"tbl": "tbl", #Krever at disse ordene er selvstendige ord i input-tekst
                                "t": "tbl", 
                                "tab": "tbl", 
                                "inj": "inj", 
                                "inj.v": "inj", 
                                "inj.v.": "inj",
                                "inf": "inf",
                                "inf.v": "inf",
                                "inf.v.": "inf"}

                my_dict_chars   = {"plaster": "plst"} #Krever at disse kun er tilstede i input-teksten (altså at 'depotplaster' gir en hit)


                input_words = [word.lower() for word in self.raw_legemiddelinput.split()]
                for word in input_words:    #Prøver her å finne riktig legemiddel ut ifra legemiddelform i input-tekst
                    if word in my_dict_words:
                        for unique_ultrashort_formulation in unique_ultrashort_formulations:
                            if my_dict_words[word] in unique_ultrashort_formulation:
                                self.legemiddelform = unique_ultrashort_formulation
                                return
                for key in my_dict_chars:
                    if key in self.raw_legemiddelinput.lower():
                        for unique_ultrashort_formulation in unique_ultrashort_formulations:
                            if my_dict_chars[key] in unique_ultrashort_formulation:
                                self.legemiddelform = unique_ultrashort_formulation
                                return
                        
                if not any(word.lower() in my_dict_words for word in self.raw_legemiddelinput.split()): #Dersom vi har kommet hit står ingen av key-ordene i my_dict_words i input.
                    if not any(key in self.raw_legemiddelinput.lower() for key in my_dict_chars): #Dersom vi har kommet hit står ingen av key-ordene i my_dict_words i input.
                        if len(unique_ultrashort_formulations) == 1:
                            self.legemiddelform = unique_ultrashort_formulations[0]
                            return                        
#                print(self.raw_legemiddelinput, word, "not in unique formulation")
        except Exception as e:
            print("Error in Medikament.try_to_fill_in_legemiddelform()", e)

    def find_atc_virkestoff_matching_word_virkestoff(self, festdata):
        if self.raw_legemiddelinput !='':
            self.atc = festdata.get_ATC(self.raw_legemiddelinput)
            self.virkestoff = festdata.get_virkestoff(self.raw_legemiddelinput)
            self.matching_word = festdata.get_matching_word(self.raw_legemiddelinput)
        else:
            self.atc = festdata.get_ATC(self.legemiddelnavn)
            self.virkestoff = festdata.get_virkestoff(self.legemiddelnavn)
            self.matching_word = festdata.get_matching_word(self.legemiddelnavn)
        try:
            self.merkenavn_bool, self.virkestoff_bool = festdata.matching_word_is_merkenavn_or_virkestoff(self.matching_word)
        except Exception as e:
            self.merkenavn_bool, self.virkestoff_bool = False, False
            print("Error in Medikament.find_atc_virkestoff_matching_word_virkestoff", e)
        if self.matching_word != None: self.legemiddelnavn = self.matching_word

    def find_interaction_objects(self, festdata):
        if self.atc != None or self.virkestoff != None:
            self.interaction_objects = festdata.get_interaction_objects(self.atc, self.virkestoff)
        else:
            print("Not trying to find interaction objects for {} as neither atc of active substance was found)".format(self.legemiddelnavn))

    def _make_compact_dose(self):
        if self.dose_fritekst != '':
            return(self.dose_fritekst)
        doses = [self.dose0008, self.dose0814, self.dose1420, self.dose2024]
        non_empty_doses = [dose for dose in doses if dose!='']
        non_empty_doses_all_equal = len(set(non_empty_doses)) == 1
        if self.dose0008 == '' and self.dose0814 == '' and self.dose1420 == '' and self.dose2024 != '':
            return(self.dose2024 + self.enhet + ' x 1 vesp')
        if non_empty_doses_all_equal:
            return(non_empty_doses[0]+self.enhet + ' x ' + str(len(non_empty_doses)))
        else:
            return("+".join(non_empty_doses) + " " + self.enhet)


class KurveArk():
    """
    Klasse som skal inneholde all user-input om medisinkurven.
    Obs kan inneholde info om mer enn 1 fysisk kurve (dvs f eks over 14 faste medikamenter.
    I KurveArk brukes Medikament-klassen for medikamentene.
    """
    
    def __init__(self, diagnose = '', cave = '', notat = '', sykehus=''):
        self.diagnose           = diagnose
        self.cave               = cave
        self.notat              = notat
        self.sykehus            = sykehus
        self.ids                = []    #List of legemiddel id-s (int) currently in use. 
        self.faste_medisiner    = []
        self.behovs_medisiner   = []
        self.alle_medisiner     = []

        self.actual_interactions= [] #A list of tuples containing (medikament1, medikament2, interaction object). 
        self.medisiner_ukjente  = [] #A list containing the drugs where no atc-code or active substance was found.
        self.autofill_has_been_run = False

    def __str__(self):
        my_string = ""
        for drug in self.alle_medisiner:
            my_string += drug.__str__()
            my_string += "\n"
        return my_string

    def autofill_from_faste_meds(self, string):
        self.entire_raw_input_string_faste = string
        self.input_meds_faste = []
        for line in string.split("\n"):
            self.input_meds_faste.append(line)
            self.legg_til_medikament(raw_legemiddelinput = line)
        self.init_festdata()
        for drug in self.faste_medisiner:
            try:
                drug.find_atc_virkestoff_matching_word_virkestoff(self.festdata)
                drug.init_autofill(self.festdata)
                self.autofill_has_been_run = True
            except Exception as e:
                print("Error in KurveArk.auto_fill_from_faste_meds()", e)

    def autofill_from_behov_meds(self, string):
        self.entire_raw_input_string_behov = string
        self.input_meds_behov = []
        for line in string.split("\n"):
            self.input_meds_behov.append(line)
            self.legg_til_medikament(faste = False, raw_legemiddelinput = line)
        self.init_festdata()
        for drug in self.behovs_medisiner:
            try:
                drug.find_atc_virkestoff_matching_word_virkestoff(self.festdata)
                drug.init_autofill(self.festdata)
                self.autofill_has_been_run = True
            except Exception as e:
                print("Error in KurveArk.auto_fill_from_behov_meds()", e)
        

    def init_festdata(self):
        self.festdata = get_festdata()

    def init_interaction_analysis(self):
        self.init_festdata()
        print("Ferdig å loade festdata")
        self._retrieve_atc_virkestoff_matching_word_info_for_all_meds()
        self._retrieve_interaction_objects_for_all_meds()
        self._find_actual_interactions()

    def _retrieve_interaction_objects_for_all_meds(self):
        for drug in self.alle_medisiner:            
            drug.find_interaction_objects(self.festdata)
            if drug.atc == None and drug.virkestoff == None:
                self.medisiner_ukjente.append(drug)

    def _find_actual_interactions(self):
        drugs_with_potential_interactions = [drug for drug in self.alle_medisiner if drug.interaction_objects != None and len(drug.interaction_objects) > 0]
        for drug_pair in list(itertools.combinations(drugs_with_potential_interactions, 2)): #Finding all pairwise combinations of drugs
            for interaction_object_A in drug_pair[0].interaction_objects:
                for interaction_object_B in drug_pair[1].interaction_objects:
                    if interaction_object_A[1] == interaction_object_B[1]:
                        if interaction_object_A[2] != interaction_object_B[2]:
                            #This if-statement is true if an interaction has been detected.
                            self.actual_interactions.append((drug_pair[0], drug_pair[1], interaction_object_A))

    def legg_til_medikament(self, faste=True, **kwargs):
        legemiddel_id = self.find_suitable_id()
        legemiddel = Medikament(legemiddel_id = legemiddel_id, fast_medisin = faste, **kwargs)
        if faste: self.faste_medisiner.append(legemiddel)
        else: self.behovs_medisiner.append(legemiddel)
        self.alle_medisiner.append(legemiddel)

    def modify_notat(self):
        if len(self.notat) < 26: pass
        else:
            modified_notat = ''
            for char in self.notat:
                modified_notat += char
                if len(modified_notat) > 24 and not "\n" in modified_notat[-25:]:
                    modified_notat += "\n"
            self.notat = modified_notat
         
    def find_suitable_id(self):
        for m in range(1000):
            if not m in self.ids:
                self.ids.append(m)
                return m     

def return_prototype_kurveark():
    kurveark = KurveArk()
    kurveark.diagnose = 'Hjerteinfarkt'
    kurveark.cave = 'Penicillin'
    with open('./userdata.txt', 'r') as f:
        datareader = csv.reader(f, delimiter='\t')
        row_no = 1
        my_dic = {}
        for row in datareader:
            my_dic[row[0]] = row[1]
            if row_no%8==0:
                kurveark.legg_til_medikament(**my_dic)
                if len(kurveark.behovs_medisiner) < 8:
                    kurveark.legg_til_medikament(faste = False, **my_dic)
            row_no +=1
    return kurveark

if __name__ == '__main__':
    kurveark = KurveArk()
    mystring = 'Hiprex tbl. 1g x 2'
    kurveark.autofill_from_faste_meds(mystring)
    print(kurveark.alle_medisiner[0])



















