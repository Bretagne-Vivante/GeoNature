from .models import Synthese, TSources

from geonature.utils.env import DB


def request_synthese(id_synthese=None, unique_id_sinp=None, id_source=None, entity_source_pk_value=None):
    filter_params={}

    if id_synthese:
        filter_params = {
            'id_synthese': id_synthese
        }

    elif unique_id_sinp:
        filter_params = {
            'unique_id_sinp': unique_id_sinp
        }

    elif id_source and entity_source_pk_value:
        filter_params = {
            'id_source': id_source,
            'entity_source_pk_value': str(entity_source_pk_value)
        }

    return  (
        DB.session.query(Synthese)
        .filter_by(**filter_params)
        if filter_params else None
    )


def get_synthese(id_synthese=None, unique_id_sinp=None, id_source=None, entity_source_pk_value=None):
    '''
        get synthese for exchange

        soit par:
        - id_synthese

        - uuid_sinp

        - id_source et entity_source_pk_value
    '''

    req_synthese = (
        request_synthese(id_synthese, unique_id_sinp, id_source, entity_source_pk_value)
    )
    

    return req_synthese.one() if req_synthese else Synthese()


def create_or_update_synthese(synthese_data):
    '''
        post or patch synthese for exchange
    '''

    DB.session.commit()
    
    synthese_data_for_get = {
        key : synthese_data.get(key)
        for key in ['id_synthese', 'unique_id_sinp', 'id_source', 'entity_source_pk_value']
    }

    try: 
        synthese = get_synthese(**synthese_data_for_get)
    except Exception as e:
        synthese = Synthese()

    if not synthese.id_synthese:
        DB.session.add(synthese)

    # synthese from dict -> marshmallow
    synthese.from_dict(synthese_data, True)

    DB.session.commit()

    return synthese


def delete_synthese(id_synthese=None, unique_id_sinp=None, id_source=None, entity_source_pk_value=None):
    '''
        delete synthese
    '''

    synthese = request_synthese(id_synthese, unique_id_sinp, id_synthese, entity_source_pk_value)

    if not synthese:
        return 0

    res = synthese.delete()
    DB.session.commit()

    return res 


def get_source(id_source):
    '''
        get source
    '''

    return (
        DB.session.query(TSources)
        .filter_by(id_source=id_source)
        .one()
    )


def create_or_update_source(source_data):
    '''
        create or update source
    '''

    id_source = source_data.get('id_source')

    source = (
        get_source(id_source)
        if id_source
        else TSources()
    )

    if not id_source: 
        DB.session.add(source)

    # passer en marshmallow
    source.from_dict(source_data, True)

    DB.session.commit()

    return source


def delete_source(id_source):
    '''
    '''

    res = (
        DB.session.query(TSources)
        .filter_by(id_source=id_source)
        .delete()
    )
    DB.session.commit()

    return res 
