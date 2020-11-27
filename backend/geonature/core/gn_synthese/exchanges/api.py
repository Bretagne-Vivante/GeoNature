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
    delete_synthese,
    get_source,
    create_or_update_source,
    delete_source
)

from .util import (
    process_from_post_data,
    process_to_get_data,
    ApiSyntheseException
)


routes = Blueprint("gn_exchanges", __name__)

@routes.route("/synthese/<int:id_synthese>", methods=["GET"], defaults={'unique_id_sinp':None, 'id_source':None, 'entity_source_pk_value':None})
@routes.route("/synthese/<string:unique_id_sinp>", methods=["GET"], defaults={'id_synthese':None, 'id_source':None, 'entity_source_pk_value':None})
@routes.route("/synthese/<int:id_source>/<int:entity_source_pk_value>", methods=["GET"], defaults={'id_synthese':None, 'unique_id_sinp':None})
@permissions.check_cruved_scope("R", module_code="SYNTHESE")
@json_resp
def get_exchanges_synthese(id_synthese, unique_id_sinp, id_source, entity_source_pk_value):
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
        return None


    return (
        process_to_get_data(
            synthese.as_dict(True)
        )
    )


def patch_or_post_exchange_synthese():
    '''
        post or patch synthese for exchange

        post_data:
            nomenclature by code (code_type is supposed to be known)

    '''

    try:

        # check data
        # nomenclature code to synthese
        # etc...
        post_data = request.json
        synthese_data = process_from_post_data(post_data)

        synthese = create_or_update_synthese(synthese_data)

        return (
            process_to_get_data(
                synthese.as_dict(True)
            )
        )

    except ApiSyntheseException as e:
        return e.as_dict(), 500



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
def patch_exchanges_synthese():
    '''
        patch put synthese for exchange
    '''

    return patch_or_post_exchange_synthese()


@routes.route("/synthese/<int:id_synthese>", methods=["DELETE"])
@routes.route("/synthese/<string:unique_id_sinp>", methods=["DELETE"], defaults={'id_synthese':None, 'id_source':None, 'entity_source_pk_value':None})
@routes.route("/synthese/<int:id_source>/<int:entity_source_pk_value>", methods=["DELETE"], defaults={'id_synthese':None, 'unique_id_sinp':None})
@permissions.check_cruved_scope("D", module_code="SYNTHESE")
@json_resp
def delete_exchanges_synthese(id_synthese, unique_id_sinp, id_source, entity_source_pk_value):

    '''
        delete synthese for exchange
    '''


    try:
        synthese = get_synthese(id_synthese, unique_id_sinp, id_source, entity_source_pk_value)
        delete_synthese(synthese.id_synthese)
    except ApiSyntheseException as e:
        return e.as_dict(), 500

    return id_synthese


@routes.route("/source/<int:id_source>", methods=["GET"])
@permissions.check_cruved_scope("R", module_code="SYNTHESE")
@json_resp
def api_get_source(id_source):
    '''
        api get source
    '''
    try:
        source = get_source(id_source)
    except:
        return "Pas de source défine pour (id_source={})".format(id_source), 500

    return source.as_dict()



def patch_or_post_exchange_source():
    '''
        post or patchsource for exchange

    '''

    post_data = request.json

    source = create_or_update_source(post_data)

    return source.as_dict()


@routes.route("/source/", methods=["PATCH"])
@permissions.check_cruved_scope("U", module_code="SYNTHESE")
@json_resp
def api_patch_source():
    '''
        api patch source
    '''
    
    return patch_or_post_exchange_source()


@routes.route("/source/", methods=["POST"])
@permissions.check_cruved_scope("C", module_code="SYNTHESE")
@json_resp
def api_post_source():
    '''
        api post source
    '''

    return patch_or_post_exchange_source()


@routes.route("/source/<int:id_source>", methods=["DELETE"])
@permissions.check_cruved_scope("D", module_code="SYNTHESE")
@json_resp
def api_delete_source(id_source):
    '''
        api delete source
    '''

    return delete_source(id_source)
