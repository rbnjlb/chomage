Projet : Analyse du chômage par pays

Ce projet vise à analyser et comparer l’évolution du taux de chômage entre plusieurs pays sur une longue période, à partir des données publiques de la World Bank.
L’objectif principal est de mettre en évidence les dynamiques relatives du chômage, indépendamment des niveaux structurels propres à chaque pays.

Données utilisées :

Source : API de la World Bank
Indicateur : Unemployment, total (% of total labor force) – ILO estimate
Pays étudiés : pays développés et émergents (France, Allemagne, Japon, Nigeria, Éthiopie, Nouvelle-Zélande, Thaïlande, Costa Rica, Argentine, etc.)
Période : selon la disponibilité des données par pays



Méthodologie :

Récupération automatique des données de chômage via l’API World Bank
Construction d’un DataFrame panel (pays × années)
Calcul de statistiques par pays (moyenne, écart-type)
Normalisation du chômage (z-score) afin de comparer les chocs relatifs entre pays
Visualisation des séries temporelles avec un affichage clair et comparable


