#!/usr/bin/env python3
from django.test import TestCase
from . import userinput

"""
TODO:
- Rett opp i alle feil
"""


class LegemiddelRecognitionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        meds1 = ['Inuxair 100 mcg/6mcg x 1',
                'Albyl-E tbl 75mg x 1',
                'Selo-zok depottbl 50mg x 1',
                'Somac tbl 20mg x 1',
                'Morfin inj.v. 5mg x 1',
                'atrovent 0,5mg/ml x 4',
                'Ventolin 5mg/ml kolbe x 4',
                'Vitamin B1 x 1',
                'TrioBe x 1']

        meds2 = ['Citalopram 10 mg x 1.',
                'Detrusitol 4 mg x 1.',
                'Furix 20 mg x 1.',
                'Lyrica 75 mg + 150mg.',
                'Palexia depot 50 + 100 mg.',
                'Paracet 1g x 4',
                'Somac 20 mg x1.',
                'Relvar 92/22mcg x1.']

        meds3 = ['Albyl-E 76mg x 1',
                'Seloken tbl 25 mg x 1',
                'Paracetamol inf.v. 1g x 4',
                'OxyNorm tbl 5 mg x 3,',
                'OxyNorm kps 5 mg x 3',
                'OxyNorm kapsel 5mg x 3']

        meds4_faste  = ['(NY!) Sobril 10 mg x 1 vesp',
                        'Calcigran Forte 1000/800mg/ie, 1tbl x 1',
                        'Eliquis tab 2,5 mg x 2',
                        '(NY DOSE!) Furix tab 40 mg + 20 mg + 0 + 0.',
                        '(NY DOSE!) Metoprolol depot 100 mg x 1',
                        'Paracetamol 1g x 4 po/iv',
                        '(NY DOSE!) Targiniq 10/5mg, 1 tbl x 2',
                        'Duphalac 15 ml x 2',
                        '(NY DOSE!) Metformin 500 mg x 3',
                        '(NY!) Cordarone 50 mg x 1',
                        'Aclasta inj. 5 mg x 1/år']
        meds4_behovs = ['(NY) Heminevrin 300mg vesp',
                        '(NY) Sobril 10mg x inntil 1',
                        '(NY) Furix 20-40 mg iv ved behov',
                        '(NY) Oxynorm tbl 5 mg v.b',
                        '(NY) Seloken inj.v. 2,5mg inntil x 3',
                        'Afipran inj.v. 10mg inntil x 3',
                        'Microlax']

        meds5_faste  = ['Fentanyl depottplaster 100mcg 2stk (skiftes hver 2. dag)',
                        'Klexane sc 40mg x 1',
                        'Lyrica tbl 125 mg x 2',
                        'Imdur depottbl 60mg x 1',
                        'Metoprolol depot tbl 50mg x 1',
                        'Simvastatin tbl 40mg x 1 vesp',
                        'Zopiclone tbl 7,5mg vesp',
                        'Folsyre tbl 1mg x 1',
                        'Levaxin tbl 150 mcg x 1',
                        'Pantoprazol tbl 40mg x 1',
                        'Burinex tbl 2 mg morgen 2 mg kl 13.',
                        'Albyl-E 75 mg x 1',
                        'Zometa infusjon 4 mg x 1 hver 4. måned',
                        'Laxoberal 20 dr kveld',
                        'Levolac mikst 15 ml x 3',
                        'Movicol 1 pose x3',
                        'Valtrex tab 250 mg x 2',
                        'Omnic tab 0,4 mg x 1',
                        'Ramipril tbl 2,5 mg + 1,25 mg ENDRET DOSERING']
        meds5_behovs = ['Furix iv 20 mg',
                        'Morfin 7,5 - 10 mg hvis OxyNorm ikke virker',
                        'Nitroglycerin sublingualt 0,5mg',
                        'Sobril 10 mg inntil x 1',
                        'Afipran 10 mg inntil x3',
                        'Paracet tbl 0,5-1 g x 3',
                        'OxyNorm 20 mg']

        meds6_faste  = ['Fentanyl plaster 50 µg/t, byttes hver tredje dag.',
                        'Somac 40 mg x 1.',
                        'Dexametason 2 mg x 2.',
                        'Furix 20 mg x 1.',
                        'Zovirax mikstur 2,5 ml x 4. Brukes til og med 05.04.',
                        'Mycostatin 1 ml x 4. Brukes til og med 05.04.']
        meds6_behovs = ['Afipran 10 mg inntil x 3.',
                        'Sobril 10 mg inntil x 2.']

        meds7_faste  = ['Hiprex tbl. 1g x 2',
                        'Pantoprazol enterotbl. 40 mg x 1',
                        'Selo-Zok depottbl. 150 mg x 1(NY DOSE)',
                        'Simvastatin tbl. 40 mg x 1',
                        'Furosemid tbl. 20 mg x 1',
                        'Eliquis tbl. 2,5 mg x 2',
                        'Selexid tbl 400mg x 3 i tre dagar etter utreise (KUR)'] 
        meds7_behovs  = ['Nitroglycerin subling. tbl.   0,25 mg x 1',
                        'Pursennid 12mg 3tbl hver 4 dag',
                        'Imovane 7,5mg en halv tab kveld',
                        'Sobril tbl. 10 mg inntil x 3',
                        'Paralgin forte tbl. 400/30 mg, 1-2 tbl. inntil x 3',
                        'Acetylcystein brusetbl. 200 mg inntil x 4 daglig']

        meds8_faste  = ['Metformin 500 mg x 1',
                        'Pantoprazol 20 mg x 1',
                        'Atorvastatin 80 mg x 1',
                        'Amlodipin 10 mg x 1',
                        'Atacand Plus 32/12,5 mg x 1',
                        'Albyl-E tbl 75 mg x 1',
                        'Victoza 1,8 mg x 1',
                        'NovoMix 30 inj. 60 IE morgen 40 IE kveld.',
                        'Taptiqom øyedråper 15 mcg/ml/5 mg/ml 1 dråpe daglig i hvert øye.',
                        'Ny! Persantin retard, 200/25 mg x2      	Blodplatehemmer, sekundærprofylakse slag.',
                        'Ny! Selo-zok depot, 100 mg x1             	Hypertensjon. Gjeninnsatt, autoseponert fra 50 mg x1.']

        meds9_faste = ['Fentanyl depotplaster, 2 plaster a 100mcg hver, totalt 200mcg. Skiftes hver andre dag, sist byttet 12.4',
                        'Klexane inj 40mg x 1 sc',
                        'Lyrica tabl 125mg x 2',
                        'Metoprolol  depottabl 50mg x 1',
                        'Simvastatin tabl 40mg x 1, til kvelden',
                        'Zopiklone 7,5mg x 1, til kvelden',
                        'Folsyre tabl 1mg x 1',
                        'Levaxin tabl 125mcg x 1',
                        'Pantoprazol tabl 40mg x 1',
                        'Burinex tabl 2mg morgen og 2 mg formiddag',
                        'Albyl E tabl 75mg x 1',
                        'Valtrex tabl 250mg x 2',
                        'Omnic tabl 0,4mg x 1',
                        'ENDRET DOSE: Ramipril tabl 1,25mg x 2']
        meds9_behovs = ['Nitroglycerin sublingualtablett 0,5mg ved press for brystet',
                        'Sobril tabl 10mg inntil x 2 mot uro',
                        'Afipran tabl 10mg inntil x 3 mot kvalme',
                        'Paracet tabl 0,5-1g inntil x 3 mot smerter',
                        'Oxynorm tabl 20mg inntil x 2 mot sterke smerter',
                        'Laxoberal 20 dråper kveld mot forstoppelse',
                        'Movicol 1 pose inntil x 3 mot forstoppelse']




        cls.kurveark = userinput.KurveArk()
        cls.kurveark.autofill_from_faste_meds('\n'.join(meds1))

        cls.kurveark2 = userinput.KurveArk()
        cls.kurveark2.autofill_from_faste_meds('\n'.join(meds2))

        cls.kurveark3 = userinput.KurveArk()
        cls.kurveark3.autofill_from_faste_meds('\n'.join(meds3))

        cls.kurveark4 = userinput.KurveArk()
        cls.kurveark4.autofill_from_faste_meds('\n'.join(meds4_faste))
        cls.kurveark4.autofill_from_behov_meds('\n'.join(meds4_behovs))

        cls.kurveark5 = userinput.KurveArk()
        cls.kurveark5.autofill_from_faste_meds('\n'.join(meds5_faste))
        cls.kurveark5.autofill_from_behov_meds('\n'.join(meds5_behovs))

        cls.kurveark6 = userinput.KurveArk()
        cls.kurveark6.autofill_from_faste_meds('\n'.join(meds6_faste))
        cls.kurveark6.autofill_from_behov_meds('\n'.join(meds6_behovs))

        cls.kurveark7 = userinput.KurveArk()
        cls.kurveark7.autofill_from_faste_meds('\n'.join(meds7_faste))
        cls.kurveark7.autofill_from_behov_meds('\n'.join(meds7_behovs))

        cls.kurveark8 = userinput.KurveArk()
        cls.kurveark8.autofill_from_faste_meds('\n'.join(meds8_faste))

        cls.kurveark9 = userinput.KurveArk()
        cls.kurveark9.autofill_from_faste_meds('\n'.join(meds9_faste))
        cls.kurveark9.autofill_from_behov_meds('\n'.join(meds9_behovs))


    def test_legemiddelnavn_correct_atc(self):
        """Controlling that certain legemiddelnavns produces correct ATC-code"""
        self.assertEqual(self.kurveark.faste_medisiner[0].atc, 'R03AK08')
        self.assertEqual(self.kurveark.faste_medisiner[1].atc, 'B01AC06')
        self.assertEqual(self.kurveark.faste_medisiner[2].atc, 'C07AB02')
        self.assertEqual(self.kurveark.faste_medisiner[3].atc, 'A02BC02')
        self.assertEqual(self.kurveark.faste_medisiner[4].atc, 'N02AA01')
        self.assertEqual(self.kurveark.faste_medisiner[5].atc, 'R01AX03')
        self.assertEqual(self.kurveark.faste_medisiner[6].atc, 'R03CC02')
        self.assertEqual(self.kurveark.faste_medisiner[7].atc, 'A11DA01')
        self.assertEqual(self.kurveark.faste_medisiner[8].atc, 'A11EA')

    def test_legemiddelnavn_correct_virkestoff(self):
        """Controlling that certain legemiddelnavns produces correct virkestoff"""
        self.assertEqual(self.kurveark.faste_medisiner[0].virkestoff, 'formoterol og beklometason')
        self.assertEqual(self.kurveark.faste_medisiner[1].virkestoff, 'acetylsalisylsyre')
        self.assertEqual(self.kurveark.faste_medisiner[2].virkestoff, 'metoprolol')
        self.assertEqual(self.kurveark.faste_medisiner[3].virkestoff, 'pantoprazol')
        self.assertEqual(self.kurveark.faste_medisiner[4].virkestoff, 'morfin')
        self.assertEqual(self.kurveark.faste_medisiner[5].virkestoff, 'ipratropiumbromid')
        self.assertEqual(self.kurveark.faste_medisiner[6].virkestoff, 'salbutamol')
        self.assertEqual(self.kurveark.faste_medisiner[7].virkestoff, 'tiamin (vit b1)')
        self.assertEqual(self.kurveark.faste_medisiner[8].virkestoff, 'vitamin b-kompleks, usammensatte preparater')

    def test_epikrisegjenkjenning_meds2(self):
        """Tester at medisinene i meds2 produserer ønsket medisinkurve"""
        #Legemiddelnavn
        self.assertEqual(self.kurveark2.faste_medisiner[0].legemiddelnavn, 'Citalopram')
        self.assertEqual(self.kurveark2.faste_medisiner[1].legemiddelnavn, 'Detrusitol')
        self.assertEqual(self.kurveark2.faste_medisiner[2].legemiddelnavn, 'Furix')
        self.assertEqual(self.kurveark2.faste_medisiner[3].legemiddelnavn, 'Lyrica')
        self.assertEqual(self.kurveark2.faste_medisiner[4].legemiddelnavn, 'Palexia depot')
        self.assertEqual(self.kurveark2.faste_medisiner[5].legemiddelnavn, 'Paracet')
        self.assertEqual(self.kurveark2.faste_medisiner[6].legemiddelnavn, 'Somac')
        self.assertEqual(self.kurveark2.faste_medisiner[7].legemiddelnavn, 'Relvar 92mikrog/22mikrog')
        #Legemiddelform
        self.assertEqual(self.kurveark2.faste_medisiner[0].legemiddelform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[1].legemiddelform, 'dp.kpsl')
        self.assertEqual(self.kurveark2.faste_medisiner[2].legemiddelform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[3].legemiddelform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[4].legemiddelform, 'depottbl')
        self.assertEqual(self.kurveark2.faste_medisiner[5].legemiddelform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[6].legemiddelform, 'ent.tbl')
        self.assertEqual(self.kurveark2.faste_medisiner[7].legemiddelform, 'inh.p.')
        #Enhet
        self.assertEqual(self.kurveark2.faste_medisiner[0].enhet, '')
        self.assertEqual(self.kurveark2.faste_medisiner[1].enhet, 'mg')
        self.assertEqual(self.kurveark2.faste_medisiner[2].enhet, '')
        self.assertEqual(self.kurveark2.faste_medisiner[3].enhet, '')
        self.assertEqual(self.kurveark2.faste_medisiner[4].enhet, 'mg')
        self.assertEqual(self.kurveark2.faste_medisiner[5].enhet, '')
        self.assertEqual(self.kurveark2.faste_medisiner[6].enhet, 'mg')
        self.assertEqual(self.kurveark2.faste_medisiner[7].enhet, 'dose')
        #Administrasjonsform
        self.assertEqual(self.kurveark2.faste_medisiner[0].administrasjonsform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[1].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark2.faste_medisiner[2].administrasjonsform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[3].administrasjonsform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[4].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark2.faste_medisiner[5].administrasjonsform, '')
        self.assertEqual(self.kurveark2.faste_medisiner[6].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark2.faste_medisiner[7].administrasjonsform, 'inh.')
        #Doser
        self.assertEqual(self.kurveark2.faste_medisiner[0].dose0008, '')
        self.assertEqual(self.kurveark2.faste_medisiner[0].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[0].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[0].dose2024, '')
        self.assertEqual(self.kurveark2.faste_medisiner[1].dose0008, '4')
        self.assertEqual(self.kurveark2.faste_medisiner[1].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[1].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[1].dose2024, '')
        self.assertEqual(self.kurveark2.faste_medisiner[2].dose0008, '')
        self.assertEqual(self.kurveark2.faste_medisiner[2].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[2].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[2].dose2024, '')
        self.assertEqual(self.kurveark2.faste_medisiner[3].dose0008, '')
        self.assertEqual(self.kurveark2.faste_medisiner[3].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[3].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[3].dose2024, '')
        self.assertEqual(self.kurveark2.faste_medisiner[4].dose0008, '50')
        self.assertEqual(self.kurveark2.faste_medisiner[4].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[4].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[4].dose2024, '100')
        self.assertEqual(self.kurveark2.faste_medisiner[5].dose0008, '')
        self.assertEqual(self.kurveark2.faste_medisiner[5].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[5].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[5].dose2024, '')
        self.assertEqual(self.kurveark2.faste_medisiner[6].dose0008, '20')
        self.assertEqual(self.kurveark2.faste_medisiner[6].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[6].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[6].dose2024, '')
        self.assertEqual(self.kurveark2.faste_medisiner[7].dose0008, '1')
        self.assertEqual(self.kurveark2.faste_medisiner[7].dose0814, '')
        self.assertEqual(self.kurveark2.faste_medisiner[7].dose1420, '')
        self.assertEqual(self.kurveark2.faste_medisiner[7].dose2024, '')
        
    def test_feilaktig_skrevne_medisiner(self):
        """Tester at algoritmen ikke gjenkjenner feilaktige doser og legemiddelnavn osv"""
        self.assertEqual(self.kurveark3.faste_medisiner[0].legemiddelnavn, 'Albyl-E')
        self.assertEqual(self.kurveark3.faste_medisiner[0].dose0008, '')
        self.assertEqual(self.kurveark3.faste_medisiner[1].legemiddelnavn, 'Seloken tbl 25 mg x 1')
        self.assertEqual(self.kurveark3.faste_medisiner[1].legemiddelform, '')
        self.assertEqual(self.kurveark3.faste_medisiner[2].legemiddelform, 'inf.v.')
        self.assertEqual(self.kurveark3.faste_medisiner[3].legemiddelform, '')
        self.assertEqual(self.kurveark3.faste_medisiner[4].legemiddelform, 'kapsel')
        self.assertEqual(self.kurveark3.faste_medisiner[5].legemiddelform, 'kapsel')

    def test_epikrisegjenkjenning_meds4(self):
        """Tester at medisinene i meds4 produserer ønsket medisinkurve"""
        ###FASTE###
        #Legemiddelnavn
        self.assertEqual(self.kurveark4.faste_medisiner[0].legemiddelnavn, 'Sobril')
        self.assertEqual(self.kurveark4.faste_medisiner[1].legemiddelnavn, 'Calcigran Forte 1000mg/800IE')
        self.assertEqual(self.kurveark4.faste_medisiner[2].legemiddelnavn, 'Eliquis')
        self.assertEqual(self.kurveark4.faste_medisiner[3].legemiddelnavn, 'Furix')
        self.assertEqual(self.kurveark4.faste_medisiner[4].legemiddelnavn, 'Metoprolol')
        self.assertEqual(self.kurveark4.faste_medisiner[5].legemiddelnavn, 'Paracetamol')
        self.assertEqual(self.kurveark4.faste_medisiner[6].legemiddelnavn, 'Targiniq 10mg/5mg')
        self.assertEqual(self.kurveark4.faste_medisiner[7].legemiddelnavn, 'Duphalac')
        self.assertEqual(self.kurveark4.faste_medisiner[8].legemiddelnavn, 'Metformin')
        self.assertEqual(self.kurveark4.faste_medisiner[9].legemiddelnavn, 'Cordarone')
        self.assertEqual(self.kurveark4.faste_medisiner[10].legemiddelnavn, 'Aclasta')
        #Legemiddelform
        self.assertEqual(self.kurveark4.faste_medisiner[0].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark4.faste_medisiner[1].legemiddelform, 'tyggetbl')
        self.assertEqual(self.kurveark4.faste_medisiner[2].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark4.faste_medisiner[3].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark4.faste_medisiner[4].legemiddelform, 'depottbl')
        self.assertEqual(self.kurveark4.faste_medisiner[5].legemiddelform, '')
        self.assertEqual(self.kurveark4.faste_medisiner[6].legemiddelform, 'depottbl')
        self.assertEqual(self.kurveark4.faste_medisiner[7].legemiddelform, 'mikst')
        self.assertEqual(self.kurveark4.faste_medisiner[8].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark4.faste_medisiner[9].legemiddelform, '')
        self.assertEqual(self.kurveark4.faste_medisiner[10].legemiddelform, 'inf.v.')
        #Enhet
        self.assertEqual(self.kurveark4.faste_medisiner[0].enhet, 'mg')
        self.assertEqual(self.kurveark4.faste_medisiner[1].enhet, 'tbl')
        self.assertEqual(self.kurveark4.faste_medisiner[2].enhet, 'mg')
        self.assertEqual(self.kurveark4.faste_medisiner[3].enhet, 'mg')
        self.assertEqual(self.kurveark4.faste_medisiner[4].enhet, 'mg')
        self.assertEqual(self.kurveark4.faste_medisiner[5].enhet, '')
        self.assertEqual(self.kurveark4.faste_medisiner[6].enhet, 'tbl')
        self.assertEqual(self.kurveark4.faste_medisiner[7].enhet, '')
        self.assertEqual(self.kurveark4.faste_medisiner[8].enhet, 'mg')
        self.assertEqual(self.kurveark4.faste_medisiner[9].enhet, '')
        self.assertEqual(self.kurveark4.faste_medisiner[10].enhet, '')
        #Administrasjonsform
        self.assertEqual(self.kurveark4.faste_medisiner[0].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[1].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[2].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[3].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[4].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[5].administrasjonsform, '')
        self.assertEqual(self.kurveark4.faste_medisiner[6].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[7].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[8].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.faste_medisiner[9].administrasjonsform, '')
        self.assertEqual(self.kurveark4.faste_medisiner[10].administrasjonsform, 'i.v.')
        #Doser
        self.assertEqual(self.kurveark4.faste_medisiner[0].dose0008, '')
        self.assertEqual(self.kurveark4.faste_medisiner[0].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[0].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[0].dose2024, '10')
        self.assertEqual(self.kurveark4.faste_medisiner[1].dose0008, '1')
        self.assertEqual(self.kurveark4.faste_medisiner[1].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[1].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[1].dose2024, '')
        self.assertEqual(self.kurveark4.faste_medisiner[2].dose0008, '2.5')
        self.assertEqual(self.kurveark4.faste_medisiner[2].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[2].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[2].dose2024, '2.5')
        self.assertEqual(self.kurveark4.faste_medisiner[3].dose0008, '40')
        self.assertEqual(self.kurveark4.faste_medisiner[3].dose0814, '20')
        self.assertEqual(self.kurveark4.faste_medisiner[3].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[3].dose2024, '')
        self.assertEqual(self.kurveark4.faste_medisiner[4].dose0008, '100')
        self.assertEqual(self.kurveark4.faste_medisiner[4].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[4].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[4].dose2024, '')
        self.assertEqual(self.kurveark4.faste_medisiner[5].dose0008, '')
        self.assertEqual(self.kurveark4.faste_medisiner[5].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[5].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[5].dose2024, '')
        self.assertEqual(self.kurveark4.faste_medisiner[6].dose0008, '1')
        self.assertEqual(self.kurveark4.faste_medisiner[6].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[6].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[6].dose2024, '1')
        self.assertEqual(self.kurveark4.faste_medisiner[7].dose0008, '')
        self.assertEqual(self.kurveark4.faste_medisiner[7].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[7].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[7].dose2024, '')
        self.assertEqual(self.kurveark4.faste_medisiner[8].dose0008, '500')
        self.assertEqual(self.kurveark4.faste_medisiner[8].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[8].dose1420, '500')
        self.assertEqual(self.kurveark4.faste_medisiner[8].dose2024, '500')
        self.assertEqual(self.kurveark4.faste_medisiner[9].dose0008, '')
        self.assertEqual(self.kurveark4.faste_medisiner[9].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[9].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[9].dose2024, '')
        self.assertEqual(self.kurveark4.faste_medisiner[10].dose0008, '')
        self.assertEqual(self.kurveark4.faste_medisiner[10].dose0814, '')
        self.assertEqual(self.kurveark4.faste_medisiner[10].dose1420, '')
        self.assertEqual(self.kurveark4.faste_medisiner[10].dose2024, '')
        ###BEHOVS###
        #Legemiddelnavn
        self.assertEqual(self.kurveark4.behovs_medisiner[0].legemiddelnavn, 'Heminevrin')
        self.assertEqual(self.kurveark4.behovs_medisiner[1].legemiddelnavn, 'Sobril')
        self.assertEqual(self.kurveark4.behovs_medisiner[2].legemiddelnavn, 'Furix')
        self.assertEqual(self.kurveark4.behovs_medisiner[3].legemiddelnavn, '(NY) Oxynorm tbl 5 mg v.b')
        self.assertEqual(self.kurveark4.behovs_medisiner[4].legemiddelnavn, 'Seloken')
        self.assertEqual(self.kurveark4.behovs_medisiner[5].legemiddelnavn, 'Afipran')
        self.assertEqual(self.kurveark4.behovs_medisiner[6].legemiddelnavn, 'Microlax')
        #Legemiddelform
        self.assertEqual(self.kurveark4.behovs_medisiner[0].legemiddelform, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[1].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark4.behovs_medisiner[2].legemiddelform, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[3].legemiddelform, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[4].legemiddelform, 'inj.v.')
        self.assertEqual(self.kurveark4.behovs_medisiner[5].legemiddelform, 'inj.v.')
        self.assertEqual(self.kurveark4.behovs_medisiner[6].legemiddelform, 'rekt.v.')
        #Enhet
        self.assertEqual(self.kurveark4.behovs_medisiner[0].enhet, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[1].enhet, 'mg')
        self.assertEqual(self.kurveark4.behovs_medisiner[2].enhet, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[3].enhet, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[4].enhet, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[5].enhet, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[6].enhet, '')
        #Administrasjonsform
        self.assertEqual(self.kurveark4.behovs_medisiner[0].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.behovs_medisiner[1].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark4.behovs_medisiner[2].administrasjonsform, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[3].administrasjonsform, '')
        self.assertEqual(self.kurveark4.behovs_medisiner[4].administrasjonsform, 'i.v.')
        self.assertEqual(self.kurveark4.behovs_medisiner[5].administrasjonsform, 'i.m./i.v.')
        self.assertEqual(self.kurveark4.behovs_medisiner[6].administrasjonsform, 'supp')
        #Doseringfritekst
        self.assertEqual(self.kurveark4.behovs_medisiner[0].dose_fritekst, '300mg vesp')
        self.assertEqual(self.kurveark4.behovs_medisiner[1].dose_fritekst, '10mg x inntil 1')
        self.assertEqual(self.kurveark4.behovs_medisiner[2].dose_fritekst, '20-40 mg iv ved behov')
        self.assertEqual(self.kurveark4.behovs_medisiner[3].dose_fritekst, '5 mg v.b')
        self.assertEqual(self.kurveark4.behovs_medisiner[4].dose_fritekst, '2,5mg inntil x 3')
        self.assertEqual(self.kurveark4.behovs_medisiner[5].dose_fritekst, '10mg inntil x 3')
        self.assertEqual(self.kurveark4.behovs_medisiner[6].dose_fritekst, '')

    def test_epikrisegjenkjenning_meds5(self):
        """Tester at medisinene i meds5 produserer ønsket medisinkurve"""
        ###FASTE###
        #Legemiddelnavn
        self.assertEqual(self.kurveark5.faste_medisiner[0].legemiddelnavn, 'Fentanyl')
        self.assertEqual(self.kurveark5.faste_medisiner[1].legemiddelnavn, 'Klexane')
        self.assertEqual(self.kurveark5.faste_medisiner[2].legemiddelnavn, 'Lyrica tbl 125 mg x 2')
        self.assertEqual(self.kurveark5.faste_medisiner[3].legemiddelnavn, 'Imdur')
        self.assertEqual(self.kurveark5.faste_medisiner[4].legemiddelnavn, 'Metoprolol')
        self.assertEqual(self.kurveark5.faste_medisiner[5].legemiddelnavn, 'Simvastatin')
        self.assertEqual(self.kurveark5.faste_medisiner[6].legemiddelnavn, 'Zopiclone')
        self.assertEqual(self.kurveark5.faste_medisiner[7].legemiddelnavn, 'Folsyre')
        self.assertEqual(self.kurveark5.faste_medisiner[8].legemiddelnavn, 'Levaxin')
        self.assertEqual(self.kurveark5.faste_medisiner[9].legemiddelnavn, 'Pantoprazol')
        self.assertEqual(self.kurveark5.faste_medisiner[10].legemiddelnavn, 'Burinex')
        self.assertEqual(self.kurveark5.faste_medisiner[11].legemiddelnavn, 'Albyl-E')
        self.assertEqual(self.kurveark5.faste_medisiner[12].legemiddelnavn, 'Zometa')
        self.assertEqual(self.kurveark5.faste_medisiner[13].legemiddelnavn, 'Laxoberal')
        self.assertEqual(self.kurveark5.faste_medisiner[14].legemiddelnavn, 'Levolac')
        self.assertEqual(self.kurveark5.faste_medisiner[15].legemiddelnavn, 'Movicol')
        self.assertEqual(self.kurveark5.faste_medisiner[16].legemiddelnavn, 'Valtrex')
        self.assertEqual(self.kurveark5.faste_medisiner[17].legemiddelnavn, 'Omnic')
        self.assertEqual(self.kurveark5.faste_medisiner[18].legemiddelnavn, 'Ramipril')
        #Legemiddelform
        self.assertEqual(self.kurveark5.faste_medisiner[0].legemiddelform, 'dept.plst')
        self.assertEqual(self.kurveark5.faste_medisiner[1].legemiddelform, 'inj.v.')
        self.assertEqual(self.kurveark5.faste_medisiner[2].legemiddelform, '')
        self.assertEqual(self.kurveark5.faste_medisiner[3].legemiddelform, 'depottbl')
        self.assertEqual(self.kurveark5.faste_medisiner[4].legemiddelform, 'depottbl')
        self.assertEqual(self.kurveark5.faste_medisiner[5].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[6].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[7].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[8].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[9].legemiddelform, 'ent.tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[10].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[11].legemiddelform, 'ent.tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[12].legemiddelform, 'inf.v.')
        self.assertEqual(self.kurveark5.faste_medisiner[13].legemiddelform, 'dråper')
        self.assertEqual(self.kurveark5.faste_medisiner[14].legemiddelform, 'mikst')
        self.assertEqual(self.kurveark5.faste_medisiner[15].legemiddelform, 'mikst')
        self.assertEqual(self.kurveark5.faste_medisiner[16].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.faste_medisiner[17].legemiddelform, 'depottbl')
        self.assertEqual(self.kurveark5.faste_medisiner[18].legemiddelform, 'tbl')
        #Enhet
        self.assertEqual(self.kurveark5.faste_medisiner[0].enhet, '')
        self.assertEqual(self.kurveark5.faste_medisiner[1].enhet, '')
        self.assertEqual(self.kurveark5.faste_medisiner[2].enhet, '')
        self.assertEqual(self.kurveark5.faste_medisiner[3].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[4].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[5].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[6].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[7].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[8].enhet, 'mcg')
        self.assertEqual(self.kurveark5.faste_medisiner[9].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[10].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[11].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[12].enhet, '')
        self.assertEqual(self.kurveark5.faste_medisiner[13].enhet, '')
        self.assertEqual(self.kurveark5.faste_medisiner[14].enhet, '')
        self.assertEqual(self.kurveark5.faste_medisiner[15].enhet, '')
        self.assertEqual(self.kurveark5.faste_medisiner[16].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[17].enhet, 'mg')
        self.assertEqual(self.kurveark5.faste_medisiner[18].enhet, 'mg')
        #Administrasjonsform
        self.assertEqual(self.kurveark5.faste_medisiner[0].administrasjonsform, 'hud')
        self.assertEqual(self.kurveark5.faste_medisiner[1].administrasjonsform, '')
        self.assertEqual(self.kurveark5.faste_medisiner[2].administrasjonsform, '')
        self.assertEqual(self.kurveark5.faste_medisiner[3].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[4].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[5].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[6].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[7].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[8].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[9].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[10].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[11].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[12].administrasjonsform, 'i.v.')
        self.assertEqual(self.kurveark5.faste_medisiner[13].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[14].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[15].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[16].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[17].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.faste_medisiner[18].administrasjonsform, 'p.o.')
        #Dosering
        self.assertEqual(self.kurveark5.faste_medisiner[0].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[0].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[0].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[0].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[1].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[1].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[1].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[1].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[2].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[2].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[2].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[2].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[3].dose0008, '60')
        self.assertEqual(self.kurveark5.faste_medisiner[3].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[3].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[3].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[4].dose0008, '50')
        self.assertEqual(self.kurveark5.faste_medisiner[4].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[4].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[4].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[5].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[5].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[5].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[5].dose2024, '40')
        self.assertEqual(self.kurveark5.faste_medisiner[6].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[6].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[6].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[6].dose2024, '7.5')
        self.assertEqual(self.kurveark5.faste_medisiner[7].dose0008, '1')
        self.assertEqual(self.kurveark5.faste_medisiner[7].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[7].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[7].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[8].dose0008, '150')
        self.assertEqual(self.kurveark5.faste_medisiner[8].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[8].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[8].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[9].dose0008, '40')
        self.assertEqual(self.kurveark5.faste_medisiner[9].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[9].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[9].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[10].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[10].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[10].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[10].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[11].dose0008, '75')
        self.assertEqual(self.kurveark5.faste_medisiner[11].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[11].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[11].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[12].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[12].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[12].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[12].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[13].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[13].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[13].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[13].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[14].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[14].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[14].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[14].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[15].dose0008, '')
        self.assertEqual(self.kurveark5.faste_medisiner[15].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[15].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[15].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[16].dose0008, '250')
        self.assertEqual(self.kurveark5.faste_medisiner[16].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[16].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[16].dose2024, '250')
        self.assertEqual(self.kurveark5.faste_medisiner[17].dose0008, '0.4')
        self.assertEqual(self.kurveark5.faste_medisiner[17].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[17].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[17].dose2024, '')
        self.assertEqual(self.kurveark5.faste_medisiner[18].dose0008, '2.5')
        self.assertEqual(self.kurveark5.faste_medisiner[18].dose0814, '')
        self.assertEqual(self.kurveark5.faste_medisiner[18].dose1420, '')
        self.assertEqual(self.kurveark5.faste_medisiner[18].dose2024, '1.25')
        ###BEHOV###
        #Legemiddelnavn
        self.assertEqual(self.kurveark5.behovs_medisiner[0].legemiddelnavn, 'Furix')
        self.assertEqual(self.kurveark5.behovs_medisiner[1].legemiddelnavn, 'Morfin')
        self.assertEqual(self.kurveark5.behovs_medisiner[2].legemiddelnavn, 'Nitroglycerin')
        self.assertEqual(self.kurveark5.behovs_medisiner[3].legemiddelnavn, 'Sobril')
        self.assertEqual(self.kurveark5.behovs_medisiner[4].legemiddelnavn, 'Afipran')
        self.assertEqual(self.kurveark5.behovs_medisiner[5].legemiddelnavn, 'Paracet')
        self.assertEqual(self.kurveark5.behovs_medisiner[6].legemiddelnavn, 'OxyNorm')
        #Legemiddelform
        self.assertEqual(self.kurveark5.behovs_medisiner[0].legemiddelform, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[1].legemiddelform, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[2].legemiddelform, 'subl.tbl')
        self.assertEqual(self.kurveark5.behovs_medisiner[3].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.behovs_medisiner[4].legemiddelform, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[5].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark5.behovs_medisiner[6].legemiddelform, '')
        #Enhet
        self.assertEqual(self.kurveark5.behovs_medisiner[0].enhet, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[1].enhet, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[2].enhet, 'mg')
        self.assertEqual(self.kurveark5.behovs_medisiner[3].enhet, 'mg')
        self.assertEqual(self.kurveark5.behovs_medisiner[4].enhet, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[5].enhet, 'g')
        self.assertEqual(self.kurveark5.behovs_medisiner[6].enhet, '')
        #Administrasjonsform
        self.assertEqual(self.kurveark5.behovs_medisiner[0].administrasjonsform, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[1].administrasjonsform, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[2].administrasjonsform, 'subl.')
        self.assertEqual(self.kurveark5.behovs_medisiner[3].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.behovs_medisiner[4].administrasjonsform, '')
        self.assertEqual(self.kurveark5.behovs_medisiner[5].administrasjonsform, 'p.o.')
        self.assertEqual(self.kurveark5.behovs_medisiner[6].administrasjonsform, '')
        #Dosering
        self.assertEqual(self.kurveark5.behovs_medisiner[0].dose_fritekst, '20 mg')
        self.assertEqual(self.kurveark5.behovs_medisiner[1].dose_fritekst, '7,5 - 10 mg hvis OxyNorm ikke virker')
        self.assertEqual(self.kurveark5.behovs_medisiner[2].dose_fritekst, '0,5mg')
        self.assertEqual(self.kurveark5.behovs_medisiner[3].dose_fritekst, '10 mg inntil x 1')
        self.assertEqual(self.kurveark5.behovs_medisiner[4].dose_fritekst, '10 mg inntil x3')
        self.assertEqual(self.kurveark5.behovs_medisiner[5].dose_fritekst, '0,5-1 g x 3')
        self.assertEqual(self.kurveark5.behovs_medisiner[6].dose_fritekst, '20 mg')

    def test_epikrisegjenkjenning_meds6(self):
        """Tester at medisinene i meds6 produserer ønsket medisinkurve"""
        ###FASTE###
        #Legemiddelnavn
        self.assertEqual(self.kurveark6.faste_medisiner[0].legemiddelnavn, 'Fentanyl')
        self.assertEqual(self.kurveark6.faste_medisiner[1].legemiddelnavn, 'Somac')
        self.assertEqual(self.kurveark6.faste_medisiner[2].legemiddelnavn, 'Dexametason')
        self.assertEqual(self.kurveark6.faste_medisiner[3].legemiddelnavn, 'Furix')
        self.assertEqual(self.kurveark6.faste_medisiner[4].legemiddelnavn, 'Zovirax')
        self.assertEqual(self.kurveark6.faste_medisiner[5].legemiddelnavn, 'Mycostatin')
        #Legemiddelform
        self.assertEqual(self.kurveark6.faste_medisiner[0].legemiddelform, 'dept.plst')
        self.assertEqual(self.kurveark6.faste_medisiner[1].legemiddelform, '')
        self.assertEqual(self.kurveark6.faste_medisiner[2].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark6.faste_medisiner[3].legemiddelform, '')
        self.assertEqual(self.kurveark6.faste_medisiner[4].legemiddelform, 'mikst')
        self.assertEqual(self.kurveark6.faste_medisiner[5].legemiddelform, 'mikst')
        #Legemiddelform
        self.assertEqual(self.kurveark6.faste_medisiner[0].enhet, '')
        self.assertEqual(self.kurveark6.faste_medisiner[1].enhet, 'mg')
        self.assertEqual(self.kurveark6.faste_medisiner[2].enhet, 'mg')
        self.assertEqual(self.kurveark6.faste_medisiner[3].enhet, '')
        self.assertEqual(self.kurveark6.faste_medisiner[4].enhet, '')
        self.assertEqual(self.kurveark6.faste_medisiner[5].enhet, '')
        #Dosering
        self.assertEqual(self.kurveark6.faste_medisiner[0].dose0008, '')
        self.assertEqual(self.kurveark6.faste_medisiner[0].dose0814, '')
        self.assertEqual(self.kurveark6.faste_medisiner[0].dose1420, '')
        self.assertEqual(self.kurveark6.faste_medisiner[0].dose2024, '')
        self.assertEqual(self.kurveark6.faste_medisiner[1].dose0008, '')
        self.assertEqual(self.kurveark6.faste_medisiner[1].dose0814, '')
        self.assertEqual(self.kurveark6.faste_medisiner[1].dose1420, '')
        self.assertEqual(self.kurveark6.faste_medisiner[1].dose2024, '')
        self.assertEqual(self.kurveark6.faste_medisiner[2].dose0008, '')
        self.assertEqual(self.kurveark6.faste_medisiner[2].dose0814, '')
        self.assertEqual(self.kurveark6.faste_medisiner[2].dose1420, '')
        self.assertEqual(self.kurveark6.faste_medisiner[2].dose2024, '')
        self.assertEqual(self.kurveark6.faste_medisiner[3].dose0008, '')
        self.assertEqual(self.kurveark6.faste_medisiner[3].dose0814, '')
        self.assertEqual(self.kurveark6.faste_medisiner[3].dose1420, '')
        self.assertEqual(self.kurveark6.faste_medisiner[3].dose2024, '')
        self.assertEqual(self.kurveark6.faste_medisiner[4].dose0008, '')
        self.assertEqual(self.kurveark6.faste_medisiner[4].dose0814, '')
        self.assertEqual(self.kurveark6.faste_medisiner[4].dose1420, '')
        self.assertEqual(self.kurveark6.faste_medisiner[4].dose2024, '')
        self.assertEqual(self.kurveark6.faste_medisiner[5].dose0008, '')
        self.assertEqual(self.kurveark6.faste_medisiner[5].dose0814, '')
        self.assertEqual(self.kurveark6.faste_medisiner[5].dose1420, '')
        self.assertEqual(self.kurveark6.faste_medisiner[5].dose2024, '')
        ###BEHOV###
        #Legemiddelnavn
        self.assertEqual(self.kurveark6.behovs_medisiner[0].legemiddelnavn, 'Afipran')
        self.assertEqual(self.kurveark6.behovs_medisiner[1].legemiddelnavn, 'Sobril')
        #Legemiddelform
        self.assertEqual(self.kurveark6.behovs_medisiner[0].legemiddelform, '')
        self.assertEqual(self.kurveark6.behovs_medisiner[1].legemiddelform, 'tbl')
        #Enhet
        self.assertEqual(self.kurveark6.behovs_medisiner[0].enhet, '')
        self.assertEqual(self.kurveark6.behovs_medisiner[1].enhet, 'mg')
        #Dosering
        self.assertEqual(self.kurveark6.behovs_medisiner[0].dose_fritekst, '10 mg inntil x 3.')
        self.assertEqual(self.kurveark6.behovs_medisiner[1].dose_fritekst, '10 mg inntil x 2.')

    def test_epikrisegjenkjenning_meds7(self):
        """Tester at medisinene i meds7 produserer ønsket medisinkurve"""
        ###FASTE###
        #Legemiddelnavn
        self.assertEqual(self.kurveark7.faste_medisiner[0].legemiddelnavn, 'Hiprex')
        self.assertEqual(self.kurveark7.faste_medisiner[1].legemiddelnavn, 'Pantoprazol')
        self.assertEqual(self.kurveark7.faste_medisiner[2].legemiddelnavn, 'Selo-Zok')
        self.assertEqual(self.kurveark7.faste_medisiner[3].legemiddelnavn, 'Simvastatin')
        self.assertEqual(self.kurveark7.faste_medisiner[4].legemiddelnavn, 'Furosemid')
        self.assertEqual(self.kurveark7.faste_medisiner[5].legemiddelnavn, 'Eliquis')
        self.assertEqual(self.kurveark7.faste_medisiner[6].legemiddelnavn, 'Selexid')
        #Legemiddelform
        self.assertEqual(self.kurveark7.faste_medisiner[0].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.faste_medisiner[1].legemiddelform, 'ent.tbl')
        self.assertEqual(self.kurveark7.faste_medisiner[2].legemiddelform, 'depottbl')
        self.assertEqual(self.kurveark7.faste_medisiner[3].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.faste_medisiner[4].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.faste_medisiner[5].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.faste_medisiner[6].legemiddelform, 'tbl')
        #Enhet
        self.assertEqual(self.kurveark7.faste_medisiner[0].enhet, 'g')
        self.assertEqual(self.kurveark7.faste_medisiner[1].enhet, 'mg')
        self.assertEqual(self.kurveark7.faste_medisiner[2].enhet, 'mg')
        self.assertEqual(self.kurveark7.faste_medisiner[3].enhet, 'mg')
        self.assertEqual(self.kurveark7.faste_medisiner[4].enhet, 'mg')
        self.assertEqual(self.kurveark7.faste_medisiner[5].enhet, 'mg')
        self.assertEqual(self.kurveark7.faste_medisiner[6].enhet, 'mg')
        #Dosering
        self.assertEqual(self.kurveark7.faste_medisiner[0].dose0008, '1')
        self.assertEqual(self.kurveark7.faste_medisiner[0].dose0814, '')
        self.assertEqual(self.kurveark7.faste_medisiner[0].dose1420, '')
        self.assertEqual(self.kurveark7.faste_medisiner[0].dose2024, '1')
        self.assertEqual(self.kurveark7.faste_medisiner[1].dose0008, '40')
        self.assertEqual(self.kurveark7.faste_medisiner[1].dose0814, '')
        self.assertEqual(self.kurveark7.faste_medisiner[1].dose1420, '')
        self.assertEqual(self.kurveark7.faste_medisiner[1].dose2024, '')
        self.assertEqual(self.kurveark7.faste_medisiner[2].dose0008, '')
        self.assertEqual(self.kurveark7.faste_medisiner[2].dose0814, '')
        self.assertEqual(self.kurveark7.faste_medisiner[2].dose1420, '')
        self.assertEqual(self.kurveark7.faste_medisiner[2].dose2024, '')
        self.assertEqual(self.kurveark7.faste_medisiner[3].dose0008, '40')
        self.assertEqual(self.kurveark7.faste_medisiner[3].dose0814, '')
        self.assertEqual(self.kurveark7.faste_medisiner[3].dose1420, '')
        self.assertEqual(self.kurveark7.faste_medisiner[3].dose2024, '')
        self.assertEqual(self.kurveark7.faste_medisiner[4].dose0008, '20')
        self.assertEqual(self.kurveark7.faste_medisiner[4].dose0814, '')
        self.assertEqual(self.kurveark7.faste_medisiner[4].dose1420, '')
        self.assertEqual(self.kurveark7.faste_medisiner[4].dose2024, '')
        self.assertEqual(self.kurveark7.faste_medisiner[5].dose0008, '2.5')
        self.assertEqual(self.kurveark7.faste_medisiner[5].dose0814, '')
        self.assertEqual(self.kurveark7.faste_medisiner[5].dose1420, '')
        self.assertEqual(self.kurveark7.faste_medisiner[5].dose2024, '2.5')
        self.assertEqual(self.kurveark7.faste_medisiner[6].dose0008, '400')
        self.assertEqual(self.kurveark7.faste_medisiner[6].dose0814, '')
        self.assertEqual(self.kurveark7.faste_medisiner[6].dose1420, '400')
        self.assertEqual(self.kurveark7.faste_medisiner[6].dose2024, '400')
        ###BEHOV###
        #Legemiddelnavn
        self.assertEqual(self.kurveark7.behovs_medisiner[0].legemiddelnavn, 'Nitroglycerin')
        self.assertEqual(self.kurveark7.behovs_medisiner[1].legemiddelnavn, 'Pursennid')
        self.assertEqual(self.kurveark7.behovs_medisiner[2].legemiddelnavn, 'Imovane')
        self.assertEqual(self.kurveark7.behovs_medisiner[3].legemiddelnavn, 'Sobril')
        self.assertEqual(self.kurveark7.behovs_medisiner[4].legemiddelnavn, 'Paralgin forte 400mg/30mg')
        self.assertEqual(self.kurveark7.behovs_medisiner[5].legemiddelnavn, 'Acetylcystein')
        #Legemiddelform
        self.assertEqual(self.kurveark7.behovs_medisiner[0].legemiddelform, 'subl.tbl')
        self.assertEqual(self.kurveark7.behovs_medisiner[1].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.behovs_medisiner[2].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.behovs_medisiner[3].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.behovs_medisiner[4].legemiddelform, 'tbl')
        self.assertEqual(self.kurveark7.behovs_medisiner[5].legemiddelform, 'brusetbl.')
        #Enhet
        self.assertEqual(self.kurveark7.behovs_medisiner[0].enhet, 'mg')
        self.assertEqual(self.kurveark7.behovs_medisiner[1].enhet, 'mg')
        self.assertEqual(self.kurveark7.behovs_medisiner[2].enhet, 'mg')
        self.assertEqual(self.kurveark7.behovs_medisiner[3].enhet, 'mg')
        self.assertEqual(self.kurveark7.behovs_medisiner[4].enhet, 'tbl')
        self.assertEqual(self.kurveark7.behovs_medisiner[5].enhet, 'mg')
        #Dosering
        self.assertEqual(self.kurveark7.behovs_medisiner[0].dose_fritekst, '0,25 mg x 1')
        self.assertEqual(self.kurveark7.behovs_medisiner[1].dose_fritekst, '12mg 3tbl hver 4 dag')
        self.assertEqual(self.kurveark7.behovs_medisiner[2].dose_fritekst, '7,5mg en halv tab kveld')
        self.assertEqual(self.kurveark7.behovs_medisiner[3].dose_fritekst, '10 mg inntil x 3')
        self.assertEqual(self.kurveark7.behovs_medisiner[4].dose_fritekst, '400/30 mg, 1-2 tbl. inntil x 3')
        self.assertEqual(self.kurveark7.behovs_medisiner[5].dose_fritekst, '200 mg inntil x 4 daglig')















