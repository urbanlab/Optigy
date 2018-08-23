import time
import json
import pickle
import numpy as np
from definition_patterns import liste_patterns
from fonctions_et_classes_main import Lecteur_Arduino, ajouter_pattern
from fonctions_desagregation import desagreger

# paramètres de la démo
duree_demo = 60
duree_seconde = duree_demo / (3600. * 24.)
chemin_resultats = '../data/serie.json'

# paramètres généraux
unite_seconde = 1
unite_journee = 24 *60 * 60
unite_temps = 1
duree_journee = int(unite_journee * unite_seconde / unite_temps)

# modèle utilisé
with open('Modele SVM.p', 'rb') as fichier_modele:
	modele = pickle.load(fichier_modele)

# Programme principal

# print('Début écoute port Serial')
lecteur_arduino = Lecteur_Arduino() 				# On commence à écouter le port Série
lecteur_arduino.start()

serie_temporelle = np.zeros(duree_journee)			# Liste des consommations de la journée, seconde par seconde

temps_debut_demo = time.time()						# Date de référence de la démo
temps = 0											# Temps depuis le début de la démo

while not(temps >= duree_demo):						# Seconde par seconde de la journée simulée,
	indice = int(temps / duree_seconde)				# (indice = numéro de la seconde de la journée simulée à laquelle on se situe)
	buffer_arduino = lecteur_arduino.extraire_buffer() # On obtient le dictionnaire qui contient l'ensemble des appareils activés cette seconde
	for cle in buffer_arduino:						# On ajoute à l'historique de consommation les patterns de chaque appareil du dictionnaire
		appareil = buffer_arduino[cle]
		ajouter_pattern(serie_temporelle, liste_patterns[appareil], indice)
	time.sleep(duree_seconde)								# On passe à la seconde simulée suivante
	temps = time.time() - temps_debut_demo

lecteur_arduino.stopper()
# print(serie_temporelle.sum()/ 3600. / 1000.)		# On arrête les mesures et on tue le thread d'acquisition
# print('Fin écoute port Serial')


# print('Début de la désagrégation')
consommations = desagreger(serie_temporelle, modele)
with open(chemin_resultats, 'w') as fichier_resultats:
	json.dump(consommations, fichier_resultats, ensure_ascii=False)
print('Fin de la désagrégation')
print(consommations)
