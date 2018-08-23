import numpy as np
import pickle
from definition_patterns import nb_appareils, liste_appareils, liste_patterns


# paramètres généraux
unite_seconde = 1
unite_journee = 24 *60 * 60
unite_temps = 1
duree_journee = int(unite_journee * unite_seconde / unite_temps)

def extraire_creneaux(conso_journee):
	dates_changement = [i for i in range(1, duree_journee - 1) if conso_journee[i] != conso_journee[i-1]]
	dates_changement = [0] + dates_changement + [duree_journee - 1]
	creneaux = [{'debut':dates_changement[i - 1], 'fin':dates_changement[i],
				 'duree':dates_changement[i] - dates_changement[i-1],
				 'niveau':conso_journee[dates_changement[i-1]]} for i in range(1, len(dates_changement))]
	creneaux_valides = [creneau for creneau in creneaux if creneau['niveau'] > 0]
	return creneaux_valides

def appliquer_modele(modele, creneaux):
	nb_appareils = len(liste_appareils) # = len(modele)
	nb_creneaux = len(creneaux)
	X = [[creneau['niveau']] for creneau in creneaux]
	y = [modele[i].predict(X)for i in range(nb_appareils)]
	activations_appareils_deduites = {}
	for i in range(nb_creneaux):
		date = creneaux[i]['debut']
		appareils = [liste_appareils[j] for j in range(nb_appareils) if y[j][i] == 1]
		activations_appareils_deduites[date] = appareils
	return activations_appareils_deduites


def calculer_consommations_prevues(patterns_appareils, activations_appareils):
	consommations = {appareil:0 for appareil in patterns_appareils}
	consommations['totale'] = 0
	for date in activations_appareils:
		espace_restant = duree_journee - date
		for appareil in activations_appareils[date]:
			pattern = liste_patterns[appareil]
			pattern_ajoute = (pattern if len(pattern) <= espace_restant else pattern[0:espace_restant])
			conso_pattern = np.sum(pattern_ajoute) / 3600. / 1000.
			consommations[appareil] += conso_pattern
			consommations['totale'] += conso_pattern
	return consommations

def desagreger(conso_journee, modele):
	creneaux = extraire_creneaux(conso_journee)
	activations_appareils = appliquer_modele(modele, creneaux)
	consommations = calculer_consommations_prevues(liste_patterns, activations_appareils)
	return consommations

