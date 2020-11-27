================
API DOCS (draft)
================

Api post synthese
=================

 
Le format d'échange
-------------------

* Données nomenclature

  * Tous les champs de type nomenclature (dont le nom commence par ``id_nomenclature_<nom_nomenclature>`` doivent être remplacés 
par des champs dont le nom est de la forme ``cd_nomenclature_<nom_nomenclature>``
  * Ces champs contiennent le code des nomenclaure et non les id des nomenclatures.

* Les jeux de données et sources sont précicés par  ``id_dataset`` et ``id_source``.
  * Les JDD peuvent être entrés dans le module métadonnées
  * Il y a une route pour pouvoir poster/modifier une source (voir ci-dessous)

Les routes
----------
* Synthese :
  * ``GET`` : récupère les données d'une ligne de la synthèse au format d'échange
    * ``/exchanges/synthese/<int:id_synthese>``: à partir de la clé primaire ``id_synthese``
    * ``/exchanges/synthese/<string:unique_id_sinp>`` : à partir de l'uuid
    * ``/exchanges/synthese/<int:id_source>/<int:entity_source_pk_value>`` : à partir du couple ``(id_source, entity_source_pk_value)``

  * ``POST/PATCH`` : pour mettre une nouvelle données, modifier une donnée existante
    * ``/exchanges/synthese/``: 
      * les données doivent être au format d'échange
      * possibilité d'identifier une ligne de la synthèse à partir de (en ordre de priorité:
        * ``id_synthese``
        * ``unique_id_sinp``
        * ``(id_source, entity_source_pk_value)``

  * ``DELETE`` : supprime une ligne de la synthèse
    * ``/exchanges/synthese/<int:id_synthese>``: à partir de la clé primaire ``id_synthese``
    * ``/exchanges/synthese/<string:unique_id_sinp>`` : à partir de l'uuid
    * ``/exchanges/synthese/<int:id_source>/<int:entity_source_pk_value>`` : à partir du couple ``(id_source, entity_source_pk_value)``


* Source : 
  * ``GET/DELETE`` : ``/source/<int:id_source>``
  * ``POST/PATCH`` : ``/source/``
    * exemple de données : 

.. code-block:: JSON

    {
        'name_source': 'Source test',
        'desc_source': 'Ceci est un source pour faire un test',
        'entity_source_pk_field': 'id_bidule',
        'url_source': '???'
    }


Les erreurs
-----------

Quand la route revoie une réponse ``status_code=500``.
Les données renvoyées sont de la forme: ``{msg: '<message pour expliquer l'erreur>', code:'<code pour identifier l'erreur>'}``

Les codes correspondent au cas suivants:

* ``1`` : pas de correspondance trouvée pour au moins un des codes nomenclature fourni 
* ``2`` : pas de source trouvée pour l'id_source fourni
* ``3`` : pas de JDD trouvé pour l'id_dataset fourni 

TODO
====

* Renseingner des utilisateurs à partir des ``id_role``
  * ajout relation observers au modèles
* from_dict -> schémas
* Lien url vers la source dans la fiche synhtèse ???
