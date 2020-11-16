'''
    test pour l'api post synthese
    comme matiere a tester on prend des donnée issues de la synthese pour tester les différentes routes
    leur bon état de marche comme les erreurs attendues

    - recupération d'une donnée de la synthèse

    - test get pour les trois cas
      - id_synthese
      - uuid
      - id_source et entity_pk_value

    - test post d'un nouvelle donnée avec une donnée de la synthese
    - test patchs dans les 3 cas
    - test erreurs
      - source non définie
      - jdd dnon defini
    - test delete 
'''



from geonature.core.gn_synthese.exchanges.models import Synthese

import os
import json
import io
from pathlib import Path

import pytest
from flask import url_for
from sqlalchemy.sql import text
from sqlalchemy.sql.expression import cast

from .bootstrap_test import app, post_json, json_of_response, get_token


from geonature.core.gn_commons.repositories import TMediaRepository
from geonature.utils.env import BACKEND_DIR, DB
from geonature.utils.errors import GeoNatureError



        # import pdb; pdb.set_trace()
@pytest.mark.usefixtures("client_class")
class TestAPIExchanges:

    _data_synthese=None

    def data_synthese(self):
        return {
            key: self._data_synthese[key]
            for key in self._data_synthese.keys()
        }

    def _get_synthese_sample(self):

        synthese = DB.session.query(Synthese).limit(1).one()
        id_synthese = synthese.id_synthese
        assert(id_synthese is not None)
 
        url_id_synthese = '/exchanges/synthese/{}'.format(id_synthese)
        response = self.client.get(url_id_synthese)
        assert(response.status_code == 200)
        self._data_synthese = json_of_response(response)
        assert(self._data_synthese['id_synthese'] == id_synthese)

        url_uuid = '/exchanges/synthese/{}'.format(self._data_synthese['unique_id_sinp'])
        response = self.client.get(url_uuid)
        assert(response.status_code == 200)
        response_data = json_of_response(response)
        assert(self._data_synthese['unique_id_sinp'] == response_data['unique_id_sinp'])

        url_source = '/exchanges/synthese/{}/{}'.format(self._data_synthese['id_source'], self._data_synthese['entity_source_pk_value'])
        response = self.client.get(url_source)
        assert(response.status_code == 200)
        response_data = json_of_response(response)
        assert(self._data_synthese['id_synthese'] == response_data['id_synthese'])

    def _post_synthese(self):

        url_synthese = '/exchanges/synthese/'
        id_synthese = self._data_synthese['id_synthese']
        for key in ['id_synthese', 'unique_id_sinp']:
            del self._data_synthese[key]

        max_of_source_plus_one = (
            DB.session.query(
                cast(Synthese.entity_source_pk_value, DB.Integer) + 1
                )
            .filter_by(id_source=self._data_synthese['id_source'])
            .order_by(
                cast(Synthese.entity_source_pk_value, DB.Integer)
                .desc()
            )
            .first()[0]
        )

        self._data_synthese['entity_source_pk_value'] = str(max_of_source_plus_one)
        response = post_json(
            self.client,
            url_synthese,
            self._data_synthese
        )
        assert(response.status_code == 200)
        self._data_synthese = json_of_response(response)
        assert(self._data_synthese['id_synthese'] != id_synthese)


    def _patch_synthese(self):

        url_synthese = '/exchanges/synthese/'
        
        id_synthese = self._data_synthese['id_synthese']
        for key in ['id_synthese', 'unique_id_sinp']:
            del self._data_synthese[key]
        response = self.client.patch(
            url_synthese,
            data=json.dumps(self._data_synthese),
            content_type="application/json",
        )
        assert(response.status_code == 200)
        self._data_synthese = json_of_response(response)
        assert(self._data_synthese['id_synthese'] == id_synthese)

        id_synthese = self._data_synthese['id_synthese']
        for key in ['id_synthese']:
            del self._data_synthese[key]
        response = self.client.patch(
            url_synthese,
            data=json.dumps(self._data_synthese),
            content_type="application/json",
        )
        assert(response.status_code == 200)
        self._data_synthese = json_of_response(response)
        assert(self._data_synthese['id_synthese'] == id_synthese)

        id_synthese = self._data_synthese['id_synthese']
        response = self.client.patch(
            url_synthese,
            data=json.dumps(self._data_synthese),
            content_type="application/json",
        )
        assert(response.status_code == 200)
        self._data_synthese = json_of_response(response)
        assert(self._data_synthese['id_synthese'] == id_synthese)


    def _delete_synthese(self):
        url_synthese = '/exchanges/synthese/{}'.format(self._data_synthese['id_synthese'])
        response = self.client.delete(
            url_synthese
        )
        assert(response.status_code == 200)
        response = self.client.get(
            url_synthese
        )
        assert(response.status_code != 200)



    def _errors_synthese(self):
        # erreur pour les patch selon plusieurs config
        url_synthese = '/exchanges/synthese/'

        # cd_nomenclature mal renseigné
        data_synthese = self.data_synthese()
        data_synthese['cd_nomenclature_geo_object_nature'] = "Ceci n'est pas un cd_nomenclature"
        response = self.client.patch(
            url_synthese,
            data=json.dumps(data_synthese),
            content_type="application/json",
        )
        print(response.get_data())
        assert(response != 200)


        # source n'existe pas
        # cd_nomenclature mal renseigné
        data_synthese = self.data_synthese()
        del data_synthese['id_source']
        response = self.client.patch(
            url_synthese,
            data=json.dumps(data_synthese),
            content_type="application/json",
        )
        print(response.get_data())
        assert(response != 200)

        # jdd n'existe pas
        data_synthese = self.data_synthese()
        del data_synthese['id_dataset']
        response = self.client.patch(
            url_synthese,
            data=json.dumps(data_synthese),
            content_type="application/json",
        )
        print(response.get_data())
        assert(response != 200)




    def test_exchanges_action(self, config):
        token = get_token(self.client, login="admin", password="admin")
        self.client.set_cookie("/", "token", token)

        self._get_synthese_sample()
        self._post_synthese()
        self._patch_synthese()
        self._delete_synthese()
        self._errors_synthese()
