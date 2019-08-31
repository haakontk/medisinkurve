#!/usr/bin/env python3


from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta
import io

def make_dummy_notat():
    import random
    import string
    alphabet = string.ascii_lowercase
    my_string = ""
    while my_string.count("\n") < 10:
        my_string += alphabet[random.randrange(0,26)]
        if random.randrange(0,26) > 20: my_string += " "
        if len(my_string) > 24 and not "\n" in my_string[-25:]:
            my_string += "\n"
    return my_string


def make_mod_string(input_string):
    if len(input_string) < 14: return input_string
    if len(input_string.split()) == 1:
        top_word, bottom_word = input_string[:len(input_string)//2], input_string[len(input_string)//2:]
        return top_word + "-\n" + bottom_word        
    else: 
        start = len(input_string)//2+1
        for n in range(start):
            finder = input_string.find(" ", start-n, start+n)
            if finder == -1:
                continue
            else: 
                break
        top_word = input_string[:finder]
        bottom_word = input_string[finder+1:]
        return top_word + "\n" + bottom_word           
            
def find_nice_font(input_string):
    mod_string = make_mod_string(input_string)
    if "\n" not in mod_string:
        lengste_linje = len(input_string)
    else:
        if len(mod_string.split("\n")[0]) > len(mod_string.split("\n")[1]):
            lengste_linje = len(mod_string.split("\n")[0])
        else: 
            lengste_linje = len(mod_string.split("\n")[0])       
    fontsize = 6    
    if lengste_linje > 13:  
        fontsize = 6 * (14 / lengste_linje)
    return fontsize 
        


def lage_pdf(userinputobject, save_as_file=False):
    fig_forside = plt.figure()
    fig_forside.set_size_inches(11.69*1.28,8.27*1.28)

    antall_faste = (len(userinputobject.faste_medisiner))
    antall_behovs = (len(userinputobject.behovs_medisiner))

    #Datoutregning til Topdato:
    def lage_topdatoliste():
        #Her gjøres utregning:
        Topdatoliste=[]
        today = datetime.now()
        for i in range(10):
            aktuell_dato = today +timedelta(days=i)
            dato_riktig_format = str(aktuell_dato.day) +"/"+ str(aktuell_dato.month)
            Topdatoliste.append(dato_riktig_format)
        return Topdatoliste

    #Datoutredning til årstall:
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    dagens_dato = (str(day) + "/" + str(month)) 

    #Schindler: (OBS, se på subling, der er "nylinje" lagt inn)
    Datoliste = []
    Medisinliste = []
    Enhetsliste = []
    Legemiddelformsliste = []
    Doseliste0008 = []
    Doseliste1420 = []
    Doseliste0814 = []
    Doseliste2024 = []
    Doseliste = []
    Administrasjonliste = [] 
    Topdatoliste = lage_topdatoliste()
    Kurvenr = []
   
    notat = userinputobject.notat


    #Her druses maten fra håkons ark inn i listene:
    for n in range (antall_faste):
        legemiddelnavn=userinputobject.faste_medisiner[n].legemiddelnavn
        Medisinliste.append(legemiddelnavn)
        legemiddelform=userinputobject.faste_medisiner[n].legemiddelform
        Legemiddelformsliste.append(legemiddelform)
        enhet=userinputobject.faste_medisiner[n].enhet
        Enhetsliste.append(enhet)
        administrasjonsform=userinputobject.faste_medisiner[n].administrasjonsform
        Administrasjonliste.append(administrasjonsform)
        dose0008=userinputobject.faste_medisiner[n].dose0008
        Doseliste0008.append(dose0008)
        dose1420=userinputobject.faste_medisiner[n].dose1420
        Doseliste1420.append(dose1420)
        dose0814=userinputobject.faste_medisiner[n].dose0814
        Doseliste0814.append(dose0814)
        dose2024=userinputobject.faste_medisiner[n].dose2024
        Doseliste2024.append(dose2024)
        ny=userinputobject.faste_medisiner[n].ny
        Datoliste.append(ny)

    # Her druses de ulike doselistene inn i hoveddoselisten: (øverst lages formatet i Doseliste slik at det er rdy til å ta i mot info. 
    for n in range(antall_faste):
        Doseliste.append([])
        dose0008 = Doseliste0008[n]   #day = datetime.now()day
        Doseliste[n].append(dose0008)
        dose0814 = Doseliste0814[n]    
        Doseliste[n].append(dose0814)
        dose1420 = Doseliste1420[n]    
        Doseliste[n].append(dose1420)
        dose2024 = Doseliste2024[n]    
        Doseliste[n].append(dose2024)

    #Årstall skrives inn på PDF:
    plt.text(0.23,0.897,year,fontsize=11)    

    #Topdato skrives inn på PDF:
    for i in range(10):
        Y = 0.967
        X = 0.418+i*0.061
        plt.text(X,Y,Topdatoliste[i], fontsize=11, va="top",ha="center")

    #Kurvenr skrives
    plt.text(0.07, 0.897, "1", fontsize=10)

    #Diagnose og Cave skrives
    diagnoselengde = len(userinputobject.diagnose)
    if diagnoselengde > 25: tekststr = 11*25/diagnoselengde
    else: tekststr = 11
    plt.text(0.044, 0.6715, userinputobject.diagnose, fontsize=tekststr)  
    cavelengde = len(userinputobject.cave)
    if cavelengde > 25: tekststr = 11*25/cavelengde
    else: tekststr = 10  
    plt.text(0.044, 0.6244, userinputobject.cave, fontsize=tekststr)    
         

    #Her skal jeg druse Medisinliste inn i skrift på PDF: (Oooog samtidig lagre textboxer av medisiner+enheter som stappes inn i hver sin schindler.):
    medisin_textboxes = []
    enhet_textboxes = []
    admin_textboxes = []
    legemiddelform_textboxes = []
    for meds in range(antall_faste):
        Y = 0.487 -meds*0.0365
        if meds == 13:
            Y = Y + 0.003
        ordlengde = len(Medisinliste[meds])
        grensemedisiner = 17
        grenselegemiddelform = 5
        grenseenhet = 4
        grenseadministrasjonsform = 4
        grensedose= 6    

        if ordlengde > grensemedisiner: tekststr = 9*grensemedisiner/ordlengde
        else: tekststr = 9
        medisintextbox=plt.text(0.044, Y, Medisinliste[meds], fontsize=tekststr) 
        medisin_textboxes.append(medisintextbox) 
        
        ordlengde = len(Enhetsliste[meds])
        if ordlengde > grenseenhet: tekststr = 8.5*grenseenhet/ordlengde
        else: tekststr = 8.5
        enhettextbox=plt.text(0.224, Y, Enhetsliste[meds], fontsize=tekststr, ha="right")
        enhet_textboxes.append(enhettextbox)

        for dose in range(4):
            ordlengde = len(Doseliste[meds][dose])
            if ordlengde > grensedose: tekststr = 5.5*grensedose/ordlengde
            else: tekststr = 5.5
            if dose == 2 or dose == 3: Xdose = 0.28+0.0285
            else: Xdose = 0.2795  
            if dose == 0 or dose == 2: Ydose = Y+0.015        
            else: Ydose = Y-0.0017
            if Doseliste[meds][dose]!="0":
                plt.text(Xdose,Ydose,Doseliste[meds][dose], fontsize=tekststr, ha="center")

        ordlengde = len(Administrasjonliste[meds])
        if ordlengde > grenseadministrasjonsform: tekststr = 8.5*grenseadministrasjonsform/ordlengde
        else: tekststr = 8.5
        admintextbox=plt.text(0.248, Y, Administrasjonliste[meds], fontsize=tekststr, ha="center")
        admin_textboxes.append(admintextbox)

        ordlengde = len(Legemiddelformsliste[meds])
        if ordlengde > grenselegemiddelform: tekststr = 8.5*grenselegemiddelform/ordlengde
        else: tekststr = 8.5
        legemiddelformtextbox=plt.text(0.155, Y, Legemiddelformsliste[meds], fontsize=tekststr)
        legemiddelform_textboxes.append(legemiddelformtextbox)

        if Datoliste[meds]: datotextbox=plt.text(0.023, Y+0.005, dagens_dato, fontsize=8.5, ha="center")
        else: 
            width=0.002
            head_width=4*width        
            plt.arrow(0.015, Y+0.008, 0.006, 0, width=width, head_width = head_width, head_length=1.1*head_width, fill=True, color="black")


    plt.margins=(0.0)
    plt.xticks([],[])
    plt.yticks([],[])
    plt.ylim(top=1, bottom=0)
    plt.xlim(right=1, left=0)

    #--------------------------------HER STARTER BAKSIDE-----------------------------------------

    fig_bakside = plt.figure()
    fig_bakside.set_size_inches(11.69*1.28,8.27*1.28)

    #Schindler: (OBS, se på subling, der er "nylinje" lagt inn)
    Datoliste = []
    Medisinliste = []
    Enhetsliste = []
    Legemiddelformsliste = []
    Doseliste0008 = []
    Doseliste1420 = []
    Doseliste0814 = []
    Doseliste2024 = []
    Doseliste = []
    Administrasjonliste = []
    Fritekstliste = [] 

    #Her druses maten fra håkons ark inn i listene:
    for n in range (antall_behovs):
        legemiddelnavn=userinputobject.behovs_medisiner[n].legemiddelnavn
        Medisinliste.append(legemiddelnavn)
        legemiddelform=userinputobject.behovs_medisiner[n].legemiddelform
        Legemiddelformsliste.append(legemiddelform)
        enhet=userinputobject.behovs_medisiner[n].enhet
        Enhetsliste.append(enhet)
        administrasjonsform=userinputobject.behovs_medisiner[n].administrasjonsform
        Administrasjonliste.append(administrasjonsform)
        dose0008=userinputobject.behovs_medisiner[n].dose0008
        Doseliste0008.append(dose0008)
        dose1420=userinputobject.behovs_medisiner[n].dose1420
        Doseliste1420.append(dose1420)
        dose0814=userinputobject.behovs_medisiner[n].dose0814
        Doseliste0814.append(dose0814)
        dose2024=userinputobject.behovs_medisiner[n].dose2024
        Doseliste2024.append(dose2024)
        ny=userinputobject.behovs_medisiner[n].ny
        Datoliste.append(ny)
        fritekst=userinputobject.behovs_medisiner[n].dose_fritekst
        Fritekstliste.append(fritekst)
        #print (Fritekstliste)

    # Her druses de ulike doselistene inn i hoveddoselisten: (øverst lages formatet i Doseliste slik at det er rdy til å ta i mot info. 
    for n in range(antall_behovs):
        Doseliste.append([])
        dose0008 = Doseliste0008[n]   
        Doseliste[n].append(dose0008)
        dose0814 = Doseliste0814[n]    
        Doseliste[n].append(dose0814)
        dose1420 = Doseliste1420[n]    
        Doseliste[n].append(dose1420)
        dose2024 = Doseliste2024[n]    
        Doseliste[n].append(dose2024)

    #Her skal jeg druse Medisinliste inn i skrift på PDF: (Oooog samtidig lagre textboxer av medisiner+enheter som stappes inn i hver sin schindler.):
    medisin_textboxes = []
    enhet_textboxes = []
    admin_textboxes = []
    legemiddelform_textboxes = []
    for meds in range(antall_behovs):
        Y = 0.84-(7*0.0365) +meds*0.0365
        if meds == 13:
            Y = Y + 0.003
        ordlengde = len(Medisinliste[meds])
        grensemedisiner = 17
        grenselegemiddelform = 5
        grenseenhet = 4
        grenseadmin = 4
        grensedose= 6    
        if ordlengde > grensemedisiner: forkort= 1
        else: forkort = 0 
        
        ordlengde = len(Medisinliste[meds])
        if ordlengde > grensemedisiner: tekststr = 9*grensemedisiner/ordlengde
        else: tekststr = 9
        medisintextbox=plt.text(0.04, Y, Medisinliste[meds], fontsize= tekststr) 
        medisin_textboxes.append(medisintextbox) 
        
        ordlengde = len(Enhetsliste[meds])
        if ordlengde > grenseenhet: tekststr = 8.5*grenseenhet/ordlengde
        else: tekststr = 8.5

        if meds < 4: enhettextbox=plt.text(0.2135, Y, Enhetsliste[meds], fontsize=tekststr, ha="right")
        else: enhettextbox=plt.text(0.224, Y, Enhetsliste[meds], fontsize=tekststr, ha="right")
        enhet_textboxes.append(enhettextbox)
        
        
        #total_fritekstlengde er antall bokstaver/tegn i friteksten. 
        total_fritekstlengde = len(Fritekstliste[meds])
        plt.text(0.27, Y+0.019, make_mod_string(Fritekstliste[meds]), fontsize=find_nice_font(Fritekstliste[meds]), va="top", linespacing= (1.55*6/find_nice_font(Fritekstliste[meds])))
                               
        ordlengde = len(Administrasjonliste[meds])
        if ordlengde > grenseadmin: tekststr = 8.5*grenseadmin/ordlengde
        else: tekststr = 8.5

        admintextbox=plt.text(0.249, Y+0.005, Administrasjonliste[meds], fontsize=tekststr, ha="center")
        admin_textboxes.append(admintextbox)

        ordlengde = len(Legemiddelformsliste[meds])
        if ordlengde > grenselegemiddelform: tekststr = 8.5*grenselegemiddelform/ordlengde
        else: tekststr = 8.5

        legemiddelformtextbox=plt.text(0.155, Y, Legemiddelformsliste[meds], fontsize=tekststr)
        legemiddelform_textboxes.append(legemiddelformtextbox)

        if Datoliste[meds]: datotextbox=plt.text(0.0086, Y+0.003, dagens_dato, fontsize=5.5, ha="left")
        else: 
            width=0.002
            head_width=4*width        
            plt.arrow(0.015, Y+0.008, 0.006, 0, width=width, head_width = head_width, head_length=1.1*head_width, fill=True, color="black")

    #Topdato skrives inn på PDF:
    for i in range(10):
        Y = 0.985
        X = 0.418+i*0.061
        plt.text(X,Y,Topdatoliste[i], fontsize=11, va="top",ha="center")

    plt.text(0.04 , 0.47, notat)

    plt.margins=(0.0)
    plt.xticks([],[])
    plt.yticks([],[])
    plt.ylim(top=1, bottom=0)
    plt.xlim(right=1, left=0)

    if save_as_file:
        with PdfPages('multipage.pdf') as pdf:
            pdf.savefig(fig_forside, bbox_inches='tight', pad_inches=0)
            pdf.savefig(fig_bakside, bbox_inches='tight', pad_inches=0)
        
    else:    
        buf = io.BytesIO()
        with PdfPages(buf) as pdf:
            fig_forside.savefig(pdf, bbox_inches='tight', pad_inches=0, format='pdf')
            fig_bakside.savefig(pdf, bbox_inches='tight', pad_inches=0, format='pdf')

        buf.seek(0)
        return buf


if __name__ == '__main__':
    from userinput import return_prototype_kurveark
    prototype = return_prototype_kurveark()
    lage_pdf(prototype, save_as_file=True)




