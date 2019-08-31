from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.forms import formset_factory
from django.urls import reverse
from .forms import FastMedisinForm
from .userinput import KurveArk
from .pdf_generator import lage_pdf
import os
import csv

# Global variables
abs_path = os.path.abspath(os.path.dirname(__file__))

def metode(request, sykehus):
    try:
        return render(request, 'medisinkurve/metode.html', {'sykehus': sykehus})
    except Exception as e:
        print("Error in metode() view.", e)        
        return HttpResponse("<h2>Something went wrong. Error in metode() view. " + str(e) + "</h2>")


def index(request):
    try:
        with open(os.path.join(abs_path, "forbidden_agents.csv"), newline='') as csvfile:
            agentreader = csv.reader(csvfile, delimiter=',')
            for clean_list_of_agents in agentreader:
                for agent in clean_list_of_agents:
                    if agent == request.META['HTTP_USER_AGENT']:
                        return render(request, 'medisinkurve/forbidden_agent.html', {})
    except Exception as e:
        print("Error in sykehus() view.", e)        
    return render(request, 'medisinkurve/sykehus.html', {})


def faq(request):
    try:
        return render(request, 'medisinkurve/faq.html')
    except Exception as e:
        print("Error in faq() view.", e)
        return HttpResponse("<h2>Something went wrong. Error in faq() view. " + str(e) + "</h2>")

def om(request):
    try:
        return render(request, 'medisinkurve/om.html')
    except Exception as e:
        print("Error in om() view.", e)
        return HttpResponse("<h2>Something went wrong. Error in om() view. " + str(e) + "</h2>")

def manual(request, sykehus, kurveark=None):

    def default_render():
        print("running default_render")
        return render(request, 'medisinkurve/manual.html', {'kurveark': kurveark, 
                                                            'formset': formset,
                                                            'sykehus': sykehus})

    extra_forms = 24
    if request.method == 'POST':
        print("running manual(request) with method=POST")
        data = {'form-TOTAL_FORMS': str(extra_forms),
                'form-INITIAL_FORMS': '0',
                'form-MAX_NUM_FORMS': ''}
        for key, value in request.POST.dict().items():
            data[key] = value
        Unready_FormSet = formset_factory(FastMedisinForm, extra=extra_forms)
        formset = Unready_FormSet(data)
        # print("Printing request.POST: ")
        # print(request.POST.dict().items())
        if formset.is_valid():
            if kurveark == None: 
                kurveark = KurveArk(sykehus=sykehus)
            else: 
                # Populating kurveark from autofill() function.
                for index, fast_medisin in enumerate(kurveark.faste_medisiner):
                    form_no = index+1
                    data['form-' + str(form_no) + '-legemiddelnavn'     ] = fast_medisin.legemiddelnavn
                    data['form-' + str(form_no) + '-legemiddelform'     ] = fast_medisin.legemiddelform
                    data['form-' + str(form_no) + '-enhet'              ] = fast_medisin.enhet
                    data['form-' + str(form_no) + '-administrasjonsform'] = fast_medisin.administrasjonsform
                    data['form-' + str(form_no) + '-dose0008'           ] = fast_medisin.dose0008
                    data['form-' + str(form_no) + '-dose0814'           ] = fast_medisin.dose0814
                    data['form-' + str(form_no) + '-dose1420'           ] = fast_medisin.dose1420
                    data['form-' + str(form_no) + '-dose2024'           ] = fast_medisin.dose2024
                    if index > 13: break #We don't accept more than 14 faste medikamenter
                for index, behovs_medisin in enumerate(kurveark.behovs_medisiner):
                    form_no = index+15
                    data['form-' + str(form_no) + '-legemiddelnavn'     ] = behovs_medisin.legemiddelnavn
                    data['form-' + str(form_no) + '-legemiddelform'     ] = behovs_medisin.legemiddelform
                    data['form-' + str(form_no) + '-enhet'              ] = behovs_medisin.enhet
                    data['form-' + str(form_no) + '-administrasjonsform'] = behovs_medisin.administrasjonsform
                    data['form-' + str(form_no) + '-dose_fritekst'      ] = behovs_medisin.dose_fritekst
                    if index > 23: break #We don't accept more than 8 behovs medikamenter
            for index, form in enumerate(formset):
                user_input = form.cleaned_data
                if user_input:
                    if index == 0:
                        kurveark.diagnose = user_input['diagnose']
                        kurveark.cave = user_input['cave']
                    elif index < 15: 
                        kurveark.legg_til_medikament(faste = True, **user_input)
                    elif index < 23: 
                        kurveark.legg_til_medikament(faste = False, **user_input)
                    elif index == 23: 
                        notat = ''
                        for char in user_input['notat']:
                            if char != '\r':
                                notat += char
                        kurveark.notat = notat


            if 'liste' in request.POST.dict():
                print('Liste was clicked')
                kurveark.create_compact_doses()
                return default_render()
            elif 'pdf' in request.POST.dict():
                print('PDF was clicked')
                buf = lage_pdf(kurveark)
                return FileResponse(buf, as_attachment=True, filename='Medisinkurve.pdf')
            elif 'autofill' in request.POST.dict():
                print('autofill used in manual()-view')
                return default_render()
            elif 'interaksjoner' in request.POST.dict():
                print('interaksjoner was clicked')
                # Do interaction stuff here
                return default_render()
                
        else:
            print(formset.errors)
            return HttpResponse("<h2>Something went wrong :( (Form is invalid)</h2>")
    else:
        Unready_FormSet = formset_factory(FastMedisinForm, extra=extra_forms)
        formset = Unready_FormSet()
        raw_kurveark = KurveArk(sykehus=sykehus)
        return default_render()

def autofill(request, sykehus):
    try:
        extra_forms = 1
        def get_default_view():
            Unready_FormSet = formset_factory(FastMedisinForm, extra=extra_forms)
            formset = Unready_FormSet()
            return render(request, 'medisinkurve/autofill.html', {'formset': formset,
                                                                    'sykehus': sykehus})        
        if request.method == 'POST':
            data = {'form-TOTAL_FORMS': str(extra_forms),
                    'form-INITIAL_FORMS': '0',
                    'form-MAX_NUM_FORMS': ''}
            for key, value in request.POST.dict().items():
                data[key] = value
            Unready_FormSet = formset_factory(FastMedisinForm, extra=extra_forms)
            formset = Unready_FormSet(data)
            if 'autofill' in request.POST.dict():
                print('Autofill was clicked')            
                if formset.is_valid():
                    form = formset[0]
                    user_input = form.cleaned_data
                    if 'autofill_faste' or 'autofill_behov' in user_input:    #This is true if the input text is non-empty
                        kurveark = KurveArk(sykehus=sykehus)
                        if 'autofill_faste' in user_input:
                            text = user_input['autofill_faste']
                            kurveark.autofill_from_faste_meds(text)
                        if 'autofill_behov' in user_input:
                            text = user_input['autofill_behov']
                            kurveark.autofill_from_behov_meds(text)
                        return manual(request, sykehus, kurveark=kurveark)
                    else:
                        return get_default_view()
                else:
                    print("Error: form was invalid.")
                    return HttpResponse("<h2>Something went wrong. The form was invalid.</h2>")
            else:
                return HttpResponse("<h2>Something went wrong. POST was sent, but without 'autofill'.</h2>")
        else:
            return get_default_view()
    except Exception as e:
        print("Error in autofill() view.", e)
        return HttpResponse("<h2>Something went wrong. Error in autofill() view. " + str(e) + "</h2>")
