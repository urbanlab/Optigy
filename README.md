# Optigy

## Principe
---
Le déploiement des compteurs intelligents, en particulier l'implémentation du compteur Linky, rencontre une forte opposition en ce moment. Cela s'explique majoritairement par deux raisons:

- Les citoyens paient indirectement pour le déploiement de ces dispositifs, mais ont l'impression que ces derniers bénéficient uniquement aux gestionnaires des réseaux d'électricité, d'eau et de gaz.
- De nombreuses personnes craignent que leurs consommations d'eau, d'électricité et de gaz soient utilisées pour reconstruire leur comportement au quotidien et ainsi les espionner.

L'objectif d'Optigy est d'apporter une réponse à ces deux sources d'opposition en montrant comment un dispositif basé sur un compteur connecté peut aider les citoyens à modérer leur consommation d'énergie tout en conservant leurs données personnelles chez eux.


## Fonctionnement
---
En raison des limites du Workshop, Optigy se focalise la problématique de l'électricité et donc sur le compteur Linky. Il s'agit d'une maquette simulant la situation suivante:

- Au sein d'une maison, le compteur Linky est muni d'un module supplémentaire permettant d'en extraire, seconde par seconde, la consommation d'énergie totale. Ces données restent en local (Linky transmet à Enedis, sous réserve d'acceptation des usagers, les données de consommation demi-heure par demi-heure, ce qui est insuffisant pour notre analyse).
- Une intelligence artificielle retrouve la consommation de chaque appareil de la maison à partir de sa consommation totale: on dit qu'elle **désagrège** la consommation d'électricité totale de la maison.
- Les usagers disposent d'une application mobile qui affiche la consommation énergétique de chaque appareil, donne des conseils permettant d'économiser de l'énergie (éco-gestes, changements d'appareils, travaux à réaliser) et chiffre en euros les économies prédites.
- Enfin, un objet connecté permet aux usagers de se rendre compte à chaque instant de leur niveau de consommation électrique: il s'agit d'une "lampe à diodes" clignotant de manière d'autant plus chaotique que la consommation d'énergie instantanée est élevée.

L'interaction des visiteurs avec la maquette est guidée par un démonstrateur et se fait en trois temps:

1. Les usagers simulent la consommation d'énergie d'une maison sur une journée en "activant" des appareils électroniques de leur choix sur une maquette en carton (voir "Architecture").
2. Cette consommation d'énergie est ensuite désagrégée par une IA pré-entraînée. Les résultats de cette désagrégation s'affichent sur l'application mobile.
3. Les usagers consultent alors l'application pour visualiser leur journée et les conseils associés.


## Architecture
---
Le dispositif Optigy se compose de 5 éléments:

1. Une maquette en carton représentant l'intérieur d'une maison, sur laquelle des répliques en plastique d'appareils électriques sont disposées. Ces dernières fonctionnent comme des boutons: quand on appuie dessus, un signal électrique est généré et transmis au contrôleur de la maquette.
2. Un Arduino permettant de contrôler la maquette et de récupérer les moments auxquels chaque appareil électrique s'active.
3. Un ordinateur qui traite les données et fait office de serveur pour l'application mobile.
4. Une application mobile comportant 2 pages: une page affichant la consommation énergétique désagrégée de la journée et une page donnant et chiffrant des conseils d'économies d'énergie. (cette dernière page est pour l'instant simulée).
5. Une "lampe à diodes" construite en carton et à l'aide de LED, qui n'est pas connectée au reste de la démo (fonctionnement aléatoire).

En termes de programmation:

- Les Arduino fonctionnent avec Processing.
- L'acquisition et les calculs sont effectués grâce à un programme Python. On implémente une SVM via le module scikitlearn pour la désagrégation.
- L'application mobile fonctionne grâce au framework Ionic3 et un serveur NodeJS.
- La lampe est contrôlée par un Arduino.

A noter que la maquette a été conçue sous l'OS Ubuntu 16.04 (Linux).
