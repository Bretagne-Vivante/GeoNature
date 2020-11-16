'''
    Module pour l'api post synthese et pour les fonctionalité d'échanges de données plus général
'''
import requests
import time

from flask import Blueprint, request, current_app
from geonature.utils.env import DB, ROOT_DIR
from geonature.core.gn_permissions import decorators as permissions
from utils_flask_sqla.response import json_resp
from .models import Synthese

from .repository import (
    get_synthese,
    create_or_update_synthese,
    delete_synthese
)

from .util import (
    process_from_post_data,
    process_to_get_data
)


routes = Blueprint("gn_exchanges", __name__)

@routes.route("/synthese/<int:id_synthese>", methods=["GET"])
@routes.route("/synthese/<string:unique_id_sinp>", methods=["GET"])
@permissions.check_cruved_scope("R", module_code="SYNTHESE")
@json_resp
def get_exchanges_synthese(id_synthese=None, unique_id_sinp=None, id_source=None, entity_source_pk_value=None):
    '''
        get synthese for exchange
    '''

    try:
        synthese = get_synthese(id_synthese, unique_id_sinp, id_source, entity_source_pk_value)
        return (
            process_to_get_data(
                synthese.as_dict(True)
            )
        )

    except Exception as e:
        raise e


    return (
        process_to_get_data(
            synthese.as_dict(True)
        )
    )


def patch_or_post_exchange_synthese():
    '''
        post synthese for exchange

        post_data:
            nomenclature by code (code_type is supposed to be known)

    '''

    try:

        # check data
        # nomenclature code to synthese
        # etc...
        post_data = request.json
        synthese_data = process_from_post_data(post_data)

        synthese = create_or_update_synthese(synthese_data=synthese_data)

        return (
            process_to_get_data(
                synthese.as_dict(True)
            )
        )

    except Exception as e:
        raise e



@routes.route("/synthese/", methods=["POST"])
@permissions.check_cruved_scope("C", module_code="SYNTHESE")
@json_resp
def post_exchanges_synthese():
    '''
        post put synthese for exchange
    '''

    return patch_or_post_exchange_synthese()


@routes.route("/synthese/", methods=["PATCH", "PUT"])
@permissions.check_cruved_scope("U", module_code="SYNTHESE")
@json_resp
def patch_exchanges_synthese(id_synthese):
    '''
        patch put synthese for exchange
    '''

    return patch_or_post_exchange_synthese()


@routes.route("/synthese/<int:id_synthese>", methods=["DELETE"])
# @routes.route("/synthese/<int:id_synthese>", methods=["DELETE"])
@permissions.check_cruved_scope("D", module_code="SYNTHESE")
@json_resp
def delete_exchanges_synthese(id_synthese):
    '''
        patch put synthese for exchange
    '''
    try:
        delete_synthese(id_synthese)
    except Exception as e:
        raise e

    return id_synthese


def check_request(r):
    print(r)
    # if not r.status_code == 200:
        # raise Exception("{} {} {} {}".format(r.request.method, r.url, r.status_code, r.headers)) 


@routes.route("/test", methods=["GET"])
@permissions.check_cruved_scope("C", module_code="SYNTHESE")
@json_resp
def test_exchanges_synthese():
    '''
        test pour les routes get et post
    '''

    session = requests.Session()

    api_login = "{}/{}".format(
        current_app.config['API_ENDPOINT'],
        'auth/login'
    )


    api_synthese_url = "{}/{}".format(
        current_app.config['API_ENDPOINT'],
        'exchanges/synthese/',
    )

    # connexion
    r = session.post(api_login, json={"login":"admin", "password":"admin", "id_application":3})
    check_request(r)

    
    id_synthese = DB.session.query(Synthese.id_synthese).limit(1).one()[0]

    print(api_synthese_url + str(id_synthese))

    # get synthese
    r = session.get(api_synthese_url + str(id_synthese))
    check_request(r)

    post_data = r.json()

    # patch synthese
    r = session.patch(api_synthese_url + str(id_synthese), json=post_data)
    check_request(r)

    id_synthese = post_data['id_synthese']
    print(id_synthese)
    del post_data['unique_id_sinp']
    del post_data['id_synthese']

    # post synthese
    r = session.post(api_synthese_url, json=post_data)
    check_request(r)

    post_data['entity_source_pk_value'] = post_data['entity_source_pk_value'] + 1
    id_synthese = r.json()['id_synthese']
    print(id_synthese)


    check_request(r)

    r = session.delete(api_synthese_url + str(id_synthese))
    check_request(r)

    r = session.get(api_synthese_url + str(id_synthese))
    if r.status_code == 200:
        return 'error', 500

    return 'ok', 200
