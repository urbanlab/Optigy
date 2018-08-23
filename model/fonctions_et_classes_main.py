import numpy as np
import pandas as pd
import pytz
import threading
import serial
import time

# Constantes associées aux classes et fonctions définies ici

duree_journee = 24 * 60 * 60


# Classes et fonctions auxiliaires utilisées dans main.py

class Lecteur_Arduino(threading.Thread):

	"""
	Classe qui gère la communication de l'ordinateur avec l'Arduino. Lorsqu'un bouton est pressé, l'objet Lecteur_Arduino
	ajoute le nom de l'appareil correspondant à un dictionnaire global buffer_arduino. Il est détruit à la fin de la démo.
	"""

	def __init__(self):
		""" Initialise la connection au port série """
		threading.Thread.__init__(self)
		self.terminer_acquisition = False  # Variable-sentinelle qui, réglée sur True depuis l'extérieur de l'objet, arrête l'acquisition
		self.buffer = dict()           # Buffer de communication entre le thread d'acquisition et le reste du programme
		self.ser = serial.Serial()     # Crée un objet qui écoute le port Série 
		self.ser.port = '/dev/ttyACM0' # chemin vers le port USB connecté avec l'Arduino. Il peut changer pour /dev/ttyS0. A trouver si on utilise une autre machine.  Avant la démo entrer: 'sudo chmod 777 /dev/ttyACM0'
		self.ser.baudrate = 9600       # Baud Rate de la communication Serial avec l'Arduino.
		self.ser.open()
		self.setDaemon(True)		   # Permet que le thread s'arrête automatiquement à la fin de la démo
		self.ser.flushInput()          # Vide le buffer du port Série au début de la démo.

	def run(self):
		""" Fonction qui définit ce que fait l'objet Lecteur_Arduino lorqu'il est lancé"""
		while(not(self.terminer_acquisition)):
			ligne = self.ser.readline()  # Attend que le buffer du port série se remplisse puis lit son contenu
			self.ser.flushInput()        # Vide le buffer du port série
			if self.terminer_acquisition:
				return
			try:
				appareil_active = self.extraire_donnees(ligne)  # En extrait le nom de l'appareil activé
				date = time.time()
				self.buffer[date] = appareil_active             # L'ajoute au contenu du buffer
			except:
				print('action annulée')                         # En cas d'échec de la lecture l'affiche sur la console

	def extraire_donnees(self, paquet_arduino):
		""" Fonction qui transforme le message sur le port Série en un nom d'appareil utilisé """
		donnees = str(paquet_arduino)  # Le format de données est : "b\'appareil\\message de retour à la ligne'"
		donnees = donnees.split('\\')[0]
		donnees = donnees.lstrip('b\'')
		print(donnees)
		return donnees

	def extraire_buffer(self):
		"""Communique le contenu du buffer au programme principal puis le vide"""
		copie_buffer = self.buffer.copy()
		self.buffer = dict()
		return copie_buffer

	def stopper(self):
		""" Fonction qui arrête l'acquisition lorsqu'elle est appelée """
		self.terminer_acquisition = True



def ajouter_pattern(serie_temporelle, pattern, indice):
	"""
	Fonction qui ajoute à partir de la date indice le pattern de consommation pattern à la série temporelle d'une durée de 24h
	serie_temporelle. Gère les effets de bords.
	"""
	offset = indice
	avant = np.zeros(offset)
	place_apres = len(serie_temporelle) - len(pattern) - offset
	if place_apres > 0:
		apres = np.zeros(len(serie_temporelle) - len(pattern) - offset)
	place_restante = len(serie_temporelle) - offset
	pattern_adapte = np.concatenate([avant, pattern[0:place_restante]])
	if place_apres > 0:
		pattern_adapte = np.concatenate([pattern_adapte, apres])
	serie_temporelle += pattern_adapte