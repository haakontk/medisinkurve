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
        

def lage_pdf(kurveark, save_as_file=False):
    # create canvas
    fig_forside = plt.figure()
    fig_forside.set_size_inches(11.69*1.28,8.27*1.28)

    # finding amount of drugs
    antall_faste = (len(kurveark.faste_medisiner))
    antall_behovs = (len(kurveark.behovs_medisiner))

    #finding dates
    def lage_topdatoliste():
        topdatoliste=[]
        today = datetime.now()
        for i in range(10):
            aktuell_dato = today +timedelta(days=i)
            dato_riktig_format = str(aktuell_dato.day) +"/"+ str(aktuell_dato.month)
            topdatoliste.append(dato_riktig_format)
        return topdatoliste

    # datoutredning til årstall:
    year = datetime.now().year
    month = datetime.now().month
    day = datetime.now().day
    dagens_dato = (str(day) + "/" + str(month)) 

    # Schindler: (ObS, se på subling, der er "nylinje" lagt inn)
    datoliste = []
    medisinliste = []
    enhetsliste = []
    legemiddelformsliste = []
    doseliste0008 = []
    doseliste1420 = []
    doseliste0814 = []
    doseliste2024 = []
    doseliste = []
    administrasjonliste = [] 
    topdatoliste = lage_topdatoliste()
    notat = kurveark.notat

    #Her druses maten fra håkons ark inn i listene:
    for n in range (antall_faste):
        legemiddelnavn=kurveark.faste_medisiner[n].legemiddelnavn
        medisinliste.append(legemiddelnavn)
        legemiddelform=kurveark.faste_medisiner[n].legemiddelform
        legemiddelformsliste.append(legemiddelform)
        enhet=kurveark.faste_medisiner[n].enhet
        enhetsliste.append(enhet)
        administrasjonsform=kurveark.faste_medisiner[n].administrasjonsform
        administrasjonliste.append(administrasjonsform)
        dose0008=kurveark.faste_medisiner[n].dose0008
        doseliste0008.append(dose0008)
        dose1420=kurveark.faste_medisiner[n].dose1420
        doseliste1420.append(dose1420)
        dose0814=kurveark.faste_medisiner[n].dose0814
        doseliste0814.append(dose0814)
        dose2024=kurveark.faste_medisiner[n].dose2024
        doseliste2024.append(dose2024)
        ny=kurveark.faste_medisiner[n].ny
        datoliste.append(ny)

    # Her druses de ulike doselistene inn i hoveddoselisten: (øverst lages formatet i doseliste slik at det er rdy til å ta i mot info. 
    for n in range(antall_faste):
        doseliste.append([])
        dose0008 = doseliste0008[n]   #day = datetime.now()day
        doseliste[n].append(dose0008)
        dose0814 = doseliste0814[n]    
        doseliste[n].append(dose0814)
        dose1420 = doseliste1420[n]    
        doseliste[n].append(dose1420)
        dose2024 = doseliste2024[n]    
        doseliste[n].append(dose2024)

    #Årstall skrives inn på Pdf:
    plt.text(0.23,0.897,year,fontsize=11)    

    #topdato skrives inn på Pdf:
    for i in range(10):
        Y = 0.967
        X = 0.418+i*0.061
        plt.text(X,Y,topdatoliste[i], fontsize=11, va="top",ha="center")

    #Kurvenr skrives
    plt.text(0.07, 0.897, "1", fontsize=10)

    #diagnose og cave skrives
    diagnoselengde = len(kurveark.diagnose)
    if diagnoselengde > 25: 
        tekststr = 11*25/diagnoselengde
    else: 
        tekststr = 11
    plt.text(0.044, 0.6715, kurveark.diagnose, fontsize=tekststr)  
    cavelengde = len(kurveark.cave)
    if cavelengde > 25: 
        tekststr = 11*25/cavelengde
    else: 
        tekststr = 10  
    plt.text(0.044, 0.6244, kurveark.cave, fontsize=tekststr)    
         
    #Her skal jeg druse medisinliste inn i skrift på Pdf: (Oooog samtidig lagre textboxer av medisiner+enheter som stappes inn i hver sin schindler.):
    legemiddelform_textboxes = []
    for meds in range(antall_faste):
        Y = 0.487 -meds*0.0365
        if meds == 13:
            Y = Y + 0.003
        ordlengde = len(medisinliste[meds])
        grensemedisiner = 17
        grenselegemiddelform = 5
        grenseenhet = 4
        grenseadministrasjonsform = 4
        grensedose= 6    

        if ordlengde > grensemedisiner: 
            tekststr = 9*grensemedisiner/ordlengde
        else: 
            tekststr = 9
        plt.text(0.044, Y, medisinliste[meds], fontsize=tekststr) 
        
        ordlengde = len(enhetsliste[meds])
        if ordlengde > grenseenhet: tekststr = 8.5*grenseenhet/ordlengde
        else: tekststr = 8.5
        plt.text(0.224, Y, enhetsliste[meds], fontsize=tekststr, ha="right")

        for dose in range(4):
            ordlengde = len(doseliste[meds][dose])
            if ordlengde > grensedose: tekststr = 5.5*grensedose/ordlengde
            else: tekststr = 5.5
            if dose == 2 or dose == 3: Xdose = 0.28+0.0285
            else: Xdose = 0.2795  
            if dose == 0 or dose == 2: Ydose = Y+0.015        
            else: Ydose = Y-0.0017
            if doseliste[meds][dose]!="0":
                plt.text(Xdose,Ydose,doseliste[meds][dose], fontsize=tekststr, ha="center")

        ordlengde = len(administrasjonliste[meds])
        if ordlengde > grenseadministrasjonsform: 
            tekststr = 8.5*grenseadministrasjonsform/ordlengde
        else: 
            tekststr = 8.5
        plt.text(0.248, Y, administrasjonliste[meds], fontsize=tekststr, ha="center")

        ordlengde = len(legemiddelformsliste[meds])
        if ordlengde > grenselegemiddelform: tekststr = 8.5*grenselegemiddelform/ordlengde
        else: tekststr = 8.5
        legemiddelformtextbox=plt.text(0.155, Y, legemiddelformsliste[meds], fontsize=tekststr)
        legemiddelform_textboxes.append(legemiddelformtextbox)

        if datoliste[meds]: datotextbox=plt.text(0.023, Y+0.005, dagens_dato, fontsize=8.5, ha="center")
        else: 
            width=0.002
            head_width=4*width        
            plt.arrow(0.015, Y+0.008, 0.006, 0, width=width, head_width = head_width, head_length=1.1*head_width, fill=True, color="black")


    plt.margins=(0.0)
    plt.xticks([],[])
    plt.yticks([],[])
    plt.ylim(top=1, bottom=0)
    plt.xlim(right=1, left=0)

    #--------------------------------HeR StaRteR baKSIde-----------------------------------------

    fig_bakside = plt.figure()
    fig_bakside.set_size_inches(11.69*1.28,8.27*1.28)

    #Schindler: (ObS, se på subling, der er "nylinje" lagt inn)
    datoliste = []
    medisinliste = []
    enhetsliste = []
    legemiddelformsliste = []
    doseliste0008 = []
    doseliste1420 = []
    doseliste0814 = []
    doseliste2024 = []
    doseliste = []
    administrasjonliste = []
    fritekstliste = [] 

    #Her druses maten fra håkons ark inn i listene:
    for n in range (antall_behovs):
        legemiddelnavn=kurveark.behovs_medisiner[n].legemiddelnavn
        medisinliste.append(legemiddelnavn)
        legemiddelform=kurveark.behovs_medisiner[n].legemiddelform
        legemiddelformsliste.append(legemiddelform)
        enhet=kurveark.behovs_medisiner[n].enhet
        enhetsliste.append(enhet)
        administrasjonsform=kurveark.behovs_medisiner[n].administrasjonsform
        administrasjonliste.append(administrasjonsform)
        dose0008=kurveark.behovs_medisiner[n].dose0008
        doseliste0008.append(dose0008)
        dose1420=kurveark.behovs_medisiner[n].dose1420
        doseliste1420.append(dose1420)
        dose0814=kurveark.behovs_medisiner[n].dose0814
        doseliste0814.append(dose0814)
        dose2024=kurveark.behovs_medisiner[n].dose2024
        doseliste2024.append(dose2024)
        ny=kurveark.behovs_medisiner[n].ny
        datoliste.append(ny)
        fritekst=kurveark.behovs_medisiner[n].dose_fritekst
        fritekstliste.append(fritekst)
        #print (fritekstliste)

    # Her druses de ulike doselistene inn i hoveddoselisten: (øverst lages formatet i doseliste slik at det er rdy til å ta i mot info. 
    for n in range(antall_behovs):
        doseliste.append([])
        dose0008 = doseliste0008[n]   
        doseliste[n].append(dose0008)
        dose0814 = doseliste0814[n]    
        doseliste[n].append(dose0814)
        dose1420 = doseliste1420[n]    
        doseliste[n].append(dose1420)
        dose2024 = doseliste2024[n]    
        doseliste[n].append(dose2024)

    #Her skal jeg druse medisinliste inn i skrift på Pdf: (Oooog samtidig lagre textboxer av medisiner+enheter som stappes inn i hver sin schindler.):
    legemiddelform_textboxes = []
    for meds in range(antall_behovs):
        Y = 0.84-(7*0.0365) +meds*0.0365
        if meds == 13:
            Y = Y + 0.003
        ordlengde = len(medisinliste[meds])
        grensemedisiner = 17
        grenselegemiddelform = 5
        grenseenhet = 4
        grenseadmin = 4
        grensedose= 6    
        if ordlengde > grensemedisiner: forkort= 1
        else: forkort = 0 
        
        ordlengde = len(medisinliste[meds])
        if ordlengde > grensemedisiner: 
            tekststr = 9*grensemedisiner/ordlengde
        else: 
            tekststr = 9
        medisintextbox=plt.text(0.04, Y, medisinliste[meds], fontsize= tekststr) 
        
        ordlengde = len(enhetsliste[meds])
        if ordlengde > grenseenhet: tekststr = 8.5*grenseenhet/ordlengde
        else: tekststr = 8.5

        if meds < 4: enhettextbox=plt.text(0.2135, Y, enhetsliste[meds], fontsize=tekststr, ha="right")
        else: enhettextbox=plt.text(0.224, Y, enhetsliste[meds], fontsize=tekststr, ha="right")
        
        #total_fritekstlengde er antall bokstaver/tegn i friteksten. 
        total_fritekstlengde = len(fritekstliste[meds])
        plt.text(0.27, Y+0.019, make_mod_string(fritekstliste[meds]), fontsize=find_nice_font(fritekstliste[meds]), va="top", linespacing= (1.55*6/find_nice_font(fritekstliste[meds])))
                               
        ordlengde = len(administrasjonliste[meds])
        if ordlengde > grenseadmin: tekststr = 8.5*grenseadmin/ordlengde
        else: tekststr = 8.5

        plt.text(0.249, Y+0.005, administrasjonliste[meds], fontsize=tekststr, ha="center")

        ordlengde = len(legemiddelformsliste[meds])
        if ordlengde > grenselegemiddelform: tekststr = 8.5*grenselegemiddelform/ordlengde
        else: tekststr = 8.5

        legemiddelformtextbox=plt.text(0.155, Y, legemiddelformsliste[meds], fontsize=tekststr)
        legemiddelform_textboxes.append(legemiddelformtextbox)

        if datoliste[meds]: datotextbox=plt.text(0.0086, Y+0.003, dagens_dato, fontsize=5.5, ha="left")
        else: 
            width=0.002
            head_width=4*width        
            plt.arrow(0.015, Y+0.008, 0.006, 0, width=width, head_width = head_width, head_length=1.1*head_width, fill=True, color="black")

    #topdato skrives inn på Pdf:
    for i in range(10):
        Y = 0.985
        X = 0.418+i*0.061
        plt.text(X,Y,topdatoliste[i], fontsize=11, va="top",ha="center")

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




