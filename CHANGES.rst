=========
CHANGELOG
=========

0.2.1 (unreleased)
------------------

**🐛 Corrections**

*

0.2.0 (2020-02-20)
------------------

**🐛 Corrections**

* Compatibilité GeoNature 2.3.1
* Optimisation et non prise en compte des communes non actives
* Révision de la documentation d'installation et de mise à jour

0.1.0 (2019-09-12)
------------------

Première version fonctionnelle du module GeoNature de tableau de bord, développé par @ElsaGuilley. 
Compatible avec la version de 2.2.1 de GeoNature.

Démo vidéo : https://geonature.fr/docs/img/2019-09-GN-dashboard-0.1.0.gif

**Fonctionnalités**

* Création d'un schéma dédié ``gn_dashboard`` avec les vues et vues matérialisées nécessaires aux graphiques et cartes de synthèse du module (#1)
* Histogramme du nombre d'observations/nombre de taxons par année
* Carte du nombre d'observations/nombre de taxons par commune ou autre types de zonage (définis en paramètre)
* Répartition des observations par rang taxonomique ou groupe INPN
* Histogramme du nombre d'observations par cadre d'acquisition et par année
* Répartition du nombre d’espèces recontactés, non recontactés ou nouvelles par année
* Filtres par rang taxonomique, groupe ou taxon et par période
