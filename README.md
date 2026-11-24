# Projet Bistrots et bulletins (2ème année Ensae)

## Contexte et problématisation

Après avoir officialisé sa candidature à la présidentielle de 2027 le 22 mai 2026, Gabriel Attal a lancé l'opération « 1000 bistrots », dont l'objectif est d'aller à la rencontre des Français. Cette démarche, à visée démocratique, a pour objectif de « créer des espaces de discussion accessibles à tous et permettre à chacun de faire entendre sa voix » [1]. Si l'accès à un bistrot semble en effet accessible à un grand nombre de personnes (majeures), il semble réducteur d'affirmer qu'ils sont accessibles à toustes. L'absence de bistrot dans certaines communes, si elle est combinée à des difficultés de mobilité, peut freiner la création d'un dialogue citoyen dans le cadre restreint de l'opération « 1000 bistrots ».

Par ailleurs, d'autres barrières, notamment des barrières symboliques, peuvent désinciter des individus de fréquenter certains établissements, notamment les bistrots. En effet, le bistrot est historiquement un lieu de rassemblement des milieux ouvriers, donc en majorité des hommes issus de classe populaire urbaine. En particulier, la littérature sur le sujet met en évidence le fait que fréquenter les bistrots est une pratique genrée. Ainsi, il est clair que l'ensemble des villes et villages ne sont pas également dotés en bistrots, et que les citoyen.ne.s qui les fréquentent ne sont pas le miroir de la population française, en particulier en termes de caractéristiques socio-démographiques.
  
Sans pour autant avoir la prétention de rassembler tous les Français, il reste que les bistrots, au sein des communes qui les abritent, sont des lieux d'échange privilégiés où le lien se créée et le tissu social se maintient. En lien avec ces considérations, le sociologue et chercheur à l'université de Zurich, Hugo Subtil, étudie le lien entre le vote français et la disparition des bars-tabacs entre 1997 et 2022 [2]. La fermeture des bars-tabacs est ici utilisée comme proxy de l'érosion du lien social dans les communes, favorisant la progression du vote d'extrême droite en France. Dans le contexte de la préparation à la campagne présidentielle de 2027, nous avons souhaité nous inspirer de cette étude dynamique réalisée à partir des données des élections législatives afin d'étudier, en statique, les liens entre la présence de bistrots dans les communes et l'existence d'un vote de droite ou d'extrême droite. Ainsi, nous tenterons de répondre aux questions suivantes : 	(i) existe-t-il un lien entre le nombre de bistrots dans une ville et l'issue des élections municipales de 2026 ? (ii) quelle stratégie Gabriel Attal aurait-il pu mettre en place pour que son parti remporte davantage de communes ? 

En premier lieu, nous préparerons les diverses sources mobilisées afin de réaliser cette étude. En deuxième lieu, l'analyse étant menée sur un sous-échantillon de villes, nous réaliserons une analyse descriptive comparative de celui-ci avec l'ensemble des villes françaises. En troisième lieu, nous étudierons l'effet de la présence de bistrots sur l'existence d'un vote de droite et d’extrême droite dans les communes, à partir d'outils économétriques. Enfin, nous proposerons une application interactive permettant à nos lecteurs avertis de simuler une stratégie de campagne pour Gabriel Attal, avec pour objectif de maximiser le nombre de communes remportées grâce à des visites de bistrots. 

## Attendus en matière d’évaluation 
Le projet présenté articulera pleinement 2 des 4 dimensions attendues (la récupération de données issues de plusieurs sources ; l’exploration de l’information présente dans celles-ci), tandis que les deux autres (la présentation des résultats et la modélisation) sont abordées de manière plus limitée. En effet, la présentation des résultats repose principalement sur quelques statistiques descriptives univariées, sous forme de tableaux et de graphiques simples. La partie modélisation s'appuie sur plusieurs régressions logistiques visant à déterminer si la densité de bistrots peut contribuer à expliquer le vote à droite, et ce, en utilisant plusieurs variables cibles. Toutefois, les résultats obtenus ne permettent pas de tirer de conclusion. Cette analyse aurait notamment pu être approfondie en intégrant d'autres variables susceptibles d'influencer le vote, telles que la superficie des communes, leur structure par âge ou leur taux de criminalité. Ces éléments n'ont cependant pas été intégrés dans le temps imaparti.  Néanmoins, le projet développe une cinquième dimension, celle de l'utilisation d'une application interactive permettant, en modulant certains paramètres, de visualiser des résultats fictifs d'une campagne hypothétique de Gabriel Attal. 

## Pour reproduire ces résultats 
* Le kernel doit tourner sur Python 3.13.15
* Le repo doit être cloné sur le datalab Onyxia pour accéder à Minio. En effet, le nombre de requête étant fortement limité sur le site mettant a disposition les sources, ces dernières ont été copiées sur un bucket Onyxia par souci d'efficacité.

### Sources & données

#### Bibliographie
[1] Attal Président : https://attalpresident.fr/actualites/1-000-bistrots-partout-en-france-la-campagne-de-gabriel-attal-vient-a-votre-rencontre
[2] Subtil, H. (2026, 30 janvier). Quand les bars-tabacs ferment : l’érosion du lien social local et la progression du vote d’extrême droite en France. Observatoire du bien-être, CEPREMAP, note n° 2026-02.

#### Résultats des élections municipales
https://www.data.gouv.fr/datasets/elections-municipales-2026-resultats-du-premier-tour
https://www.data.gouv.fr/datasets/elections-municipales-2026-resultats-du-second-tour

### Analyse statistique
https://eric.univ-lyon2.fr/ricco/tanagra/fichiers/fr_Tanagra_Python_Regression_Logistique.pdf

#### Sirene & NAF
https://www.data.gouv.fr/datasets/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret
https://www.insee.fr/fr/metadonnees/nafr2/sousClasse/56.30Z

#### Données Filosofi
https://www.insee.fr/fr/metadonnees/source/serie/s1172
https://catalogue-donnees.insee.fr/fr/catalogue/recherche/DS_FILOSOFI_CC
