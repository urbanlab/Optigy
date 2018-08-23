import numpy as np
from sklearn import svm
import pickle

import random
import matplotlib.pyplot as plt
import pandas as pd

from definition_patterns import nb_appareils, classes, liste_patterns

# paramètres généraux
unite_seconde = 1
unite_journee = 24 *60 * 60
unite_temps = 1
duree_journee = int(unite_journee * unite_seconde / unite_temps)

# Définition des paramètres d'entrainement
parametres_entrainement = {
	'fridge':{
		'numero':1,
		'nb_activations_min':3,
		'nb_activations_max':7,
	},
	'washing machine':{
		'numero':2,
		'nb_activations_min':1,
		'nb_activations_max':2,
	},
	'clim1':{
		'numero':3,
		'nb_activations_min':1,
		'nb_activations_max':2,
	},
	'clim2':{
		'numero':4,
		'nb_activations_min':1,
		'nb_activations_max':2,
	},
	'TV':{
		'numero':5,
		'nb_activations_min':1,
		'nb_activations_max':5,
	}
}


# Fonctions de création de journées d'entraînement

def journee(activations_appareils):
	conso_journee = np.zeros(duree_journee)
	for date in activations_appareils:
		ajouter_pattern(conso_journee, date, liste_patterns[activations_appareils[date]])
	return conso_journee


def ajouter_pattern(conso_journee, date, pattern_ajoute):
	taille_journee = len(conso_journee)
	taille_pattern = len(pattern_ajoute)
	place_disponible = taille_journee - date
	if taille_pattern > place_disponible:
		pattern_tronque = pattern_ajoute[0:place_disponible]
		conso_journee[date:] += pattern_tronque
	else:
		conso_journee[date:date + taille_pattern] += pattern_ajoute


def labeliser_journee(activations_appareils):
	labels = [[] for i in range(duree_journee)]
	for date in activations_appareils:
		appareil = activations_appareils[date]
		date_debut = date
		date_fin = min(duree_journee, date_debut + len(liste_patterns[appareil]))
		for i in range(date_debut, date_fin):
			labels[i].append(appareil)
	for liste in labels:
		liste.sort()
	return labels


def extraire_creneaux(conso_journee):
	dates_changement = [i for i in range(1, duree_journee - 1) if conso_journee[i] != conso_journee[i-1]]
	dates_changement = [0] + dates_changement + [duree_journee - 1]
	creneaux = [{'debut':dates_changement[i - 1], 'fin':dates_changement[i],
				 'duree':dates_changement[i] - dates_changement[i-1],
				 'niveau':conso_journee[dates_changement[i-1]]} for i in range(1, len(dates_changement))]
	creneaux_valides = [creneau for creneau in creneaux if creneau['niveau'] > 0]
	return creneaux_valides


def labeliser_creneaux(creneaux, labels_activations):
	labels = [[] for c in creneaux]
	nb_creneaux = len(creneaux)
	for i in range(nb_creneaux):
		labels[i] = labels_activations[creneaux[i]['debut']]
	return labels


def generer_journee(parametres):
	activations_appareils = {}
	for appareil in parametres:
		nb_activations = np.random.randint(parametres[appareil]['nb_activations_min'], parametres[appareil]['nb_activations_max'] + 1)
		duree_activation = len(liste_patterns[appareil])
		dates_activations_possibles = set(range(duree_journee))
		for i in range(nb_activations):
			date_activation = random.sample(dates_activations_possibles, 1)[0]
			activations_appareils[date_activation] = appareil
			dates_activations_possibles.difference_update(set(range(date_activation - duree_activation + 1, date_activation + duree_activation)))
	journee_generee = journee(activations_appareils)
	labels_activations = labeliser_journee(activations_appareils)
	creneaux = extraire_creneaux(journee_generee)
	labels_creneaux = labeliser_creneaux(creneaux, labels_activations) 
	return journee_generee, creneaux, labels_creneaux


# Fonction d'entrainement d'un modèle de désagrégation quelconque
def entrainer_modeles(modeles, parametres_entrainement, nb_journees=100):
	Xi = [[] for jour in range(nb_journees)]
	yi = [[] for jour in range(nb_journees)]

	for jour in range(nb_journees):
		print('Avancement: {}%'.format(int(jour / nb_journees * 100)))
		creneaux, labels = generer_journee(parametres_entrainement)[1:]
		durees = [creneau['duree'] for creneau in creneaux]
		# niveaux = [creneau['niveau'] for creneau in creneaux]
		# Xi[jour] = np.transpose([durees, niveaux])
		niveaux = [[creneau['niveau']] for creneau in creneaux]
		Xi[jour] = np.array(niveaux)
		yi[jour] = [[] for label in labels]
		nb_creneaux = len(yi[jour])
		for i in range(nb_creneaux):
			yi[jour][i] = [parametres_entrainement[label]['numero'] for label in labels[i]]
			yi[jour][i] = [(1 if j in yi[jour][i] else 0) for j in range(1, nb_appareils + 1)]

		yi[jour] = np.array(yi[jour])

	X = np.concatenate(Xi)
	y = np.concatenate(yi)
	y = np.transpose(y)
	for i in range(5):
		modeles[i].fit(X, y[i])

	return X, y

# programme principal: création et entraînement d'un modèle

modeles = [svm.SVC(decision_function_shape='ovo') for i in range(nb_appareils)]
X, y = entrainer_modeles(modeles, parametres_entrainement, 500)
scores = [modeles[i].score(X, y[i]) for i in range(nb_appareils)]
print('scores: ', {'min':np.min(scores), 'mean':np.mean(scores), 'max':np.max(scores)})

retenir_modele = bool(eval(input('Retenir modèle ? (0 ou 1) :')))
if retenir_modele:
	with open('Modele SVM.p', 'wb') as fichier_modele:
		pickle.dump(modeles, fichier_modele)

"""Phase d'essai du modèle -> si besoin"""

# with open('Modele SVM.p', 'rb') as fichier_modele:
# 	modele = pickle.load(fichier_modele)


# def essayer_modele(modeles, parametres_entrainement):
# 	plt.ion()
# 	arret = False
# 	while not(arret):
# 		journee_conso, creneaux, labels = generer_journee(parametres_entrainement)
# 		durees = [creneau['duree'] for creneau in creneaux]
# 		# niveaux = [creneau['niveau'] for creneau in creneaux]
# 		# X = np.transpose([durees, niveaux])
# 		niveaux = [[creneau['niveau']] for creneau in creneaux]
# 		X = np.array(niveaux)
# 		predictions = np.zeros((len(X), 5))
# 		for i in range(5):
# 			predictions[:, i] = modeles[i].predict(X)
# 		predictions = [[classes[i+1] for i in range(5) if pred[i] == 1] for pred in predictions]
# 		visualisation = pd.DataFrame(data={'Prédictions':predictions, 'Réalité':labels})
# 		print(visualisation)
# 		plt.plot(journee_conso)
# 		plt.plot(reconstituer_signal(creneaux, predictions))
# 		# plt.plot(journee_conso - reconstituer_signal(creneaux, predictions))
# 		plt.show()
# 		print('---------------------------------------------------------------------------')
# 		arret = bool(eval(input('Arrêter ? (0 ou 1): ')))
# 		print('---------------------------------------------------------------------------')
# 		plt.clf()

# def reconstituer_signal(creneaux, predictions):
# 	creneaux_reconstitues = [creneau for creneau in creneaux if creneau['niveau'] != 0]
# 	signal_reconstitue = np.zeros(duree_journee)
# 	for i in range(len(creneaux_reconstitues)):
# 		creneau = creneaux_reconstitues[i]
# 		creneau['niveau'] = np.sum([max(liste_patterns[pred]) for pred in predictions[i]])
# 		signal_reconstitue[creneau['debut']:creneau['fin']] = creneau['niveau']
# 	return signal_reconstitue

# parametres_test = {
# 	'fridge':{
# 		'numero':1,
# 		'nb_activations_min':5,
# 		'nb_activations_max':10,
# 	},
# 	'washing machine':{
# 		'numero':2,
# 		'nb_activations_min':1,
# 		'nb_activations_max':2,
# 	},
# 	'clim1':{
# 		'numero':3,
# 		'nb_activations_min':1,
# 		'nb_activations_max':2,
# 	},
# 	'clim2':{
# 		'numero':4,
# 		'nb_activations_min':1,
# 		'nb_activations_max':2,
# 	},
# 	'TV':{
# 		'numero':5,
# 		'nb_activations_min':2,
# 		'nb_activations_max':4,
# 	}
# }

# essayer_modele(modele, parametres_test)
