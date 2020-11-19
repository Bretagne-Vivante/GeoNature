================
API DOCS (draft)
================

Api post synthese
=================

Données nomenclature
--------------------

* Tous les champs de type nomenclature (dont le nom commence par ``id_nomenclature_<nom_nomenclature>`` doivent être remplacés 
par des champs dont le nom est de la forme ``cd_nomenclature_<nom_nomenclature>``
* Ces champs contiennent le code des nomenclaure et non les id des nomenclatures.


Les erreurs
-----------

Quand la route revoie une réponse ``status_code=500``.
Les données renvoyées sont de la forme: ``{msg: '<message pour expliquer l'erreur>', code:'<code pour identifier l'erreur>'}``

Les codes correspondent au cas suivants:

* 1 : pas de correspondance trouvée pour au moins un des codes nomenclature fourni 
* 2 : pas de source trouvée pour l'id_source fourni
* 3 : pas de JDD trouvé pour l'id_dataset fourni 
