import numpy as np

# paramètres généraux
unite_seconde = 1
unite_journee = 24 *60 * 60
unite_temps = 1
duree_journee = int(unite_journee * unite_seconde / unite_temps)

# fonctions utilisées (création de patterns)
def periode(niveau_bas, niveau_haut, duree_bas, duree_haut):
	duree = duree_bas + duree_haut
	motif_periode = np.zeros(duree)
	motif_periode[0:duree_haut] = niveau_haut
	motif_periode[duree_haut:duree] = niveau_bas
	return motif_periode


def pattern(niveau_bas, niveau_haut, duree_bas, duree_haut, nb_periodes):
	return np.concatenate([periode(niveau_bas, niveau_haut, duree_bas, duree_haut) for i in range(nb_periodes)])

# Définition des patterns associés à chaque appareil de la maison
pattern_fridge = pattern(0, 120, 0, 60*20, 1)
pattern_washing_machine = pattern(0, 170, 0, 60*60, 1)
pattern_clim1 = pattern(0, 1700, 0, 3*60*60, 1)
pattern_clim2 = pattern(0, 1500, 0, 30*60, 1)
pattern_TV = pattern(0, 75, 0, 60*60, 1)

nb_appareils = 5
liste_appareils = ['fridge', 'washing machine', 'clim1', 'clim2', 'TV']
classes ={1:'fridge', 2:'washing machine', 3:'clim1', 4:'clim2', 5:'TV'}
liste_patterns = {'fridge':pattern_fridge, 'washing machine':pattern_washing_machine, 'clim1':pattern_clim1, 'clim2':pattern_clim2, 'TV':pattern_TV}