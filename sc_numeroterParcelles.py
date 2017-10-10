# -*- coding: utf-8 -*-

import os
import pickle

def numeroterParcelles(fichier='Feuille CL0180000A01 AULAN - 026/26041010180000A01.LOC', dossier='/home/martin/Documents/Permagro/Mission1_PALUD/donnees'):
    os.chdir(dossier)
    loc=open(fichier,r)
