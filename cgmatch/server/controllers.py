import logging
import json
from flask import current_app
from flask_pymongo import PyMongo
from werkzeug.datastructures import Headers
import requests

LOG = logging.getLogger(__name__)

def a_patient(patient_id=None):
    """ Gets a specific patient when an id is provided,
        otherwise returns a random patient from the 50 benchmark patients

        Args:
            patient_id(str) : the _id of the patient in matchmaker mongodb database

        Returns:
            patient_obj(dic) : a matchmaker patient object
    """

    mongo = PyMongo(current_app)
    patient_obj = None
    if patient_id == None: # this function should return a random test patient
        LOG.info("retrieving a random patient from db")
        query_result = mongo.db.patient.aggregate([
                { '$match' : {'contact.institution' : "Children's Hospital of Eastern Ontario"} },
                { '$sample' : { 'size' : 1 } }]
            )
        patient_obj = dict(list(query_result)[0])
    else:
        LOG.info("retrieving patient {} from db".format(patient_id))
        patient_obj = mongo.db.patient.find_one( {'_id': patient_id} )

    # if a patient is retrieved than parse its features (used downstream for patient query)
    if patient_obj:
        for feature in patient_obj.get('features'):
            feature['id'] = feature.get('_id')
            feature.pop('_id')

        LOG.info("Patient with ID {} was retrieved".format(patient_obj['_id']))
    return patient_obj

def patient_matches():
    """ Retrieve external matching queries and respective matching results, group by patient matched

        Returns:
            patient_matches(obj): keys are database patients and values a list of external patients matching them
    """

    LOG.info("collecting patient matches from matchbox database")
    mongo = PyMongo(current_app)

    patient_matches = {}

    patients = mongo.db.patient.find()
    for patient in patients:
        matches = mongo.db.externalMatchQuery.find({ 'results.patient._id' : patient['_id']})
        patient_matches[patient['_id']] = list(matches)

    return patient_matches

def format_query(form_fields):
    """ Create a patient query from the fields returned from a patient search form

        Args:
            form_fields(dict): form fields dictionary

        Returns:
            patient_query(dict) : a patient query object
    """
    LOG.info("formatting patient query")

    patient_query= {
        "patient": {
            "id": 'test_patient_id',
            "contact" : {
                "name": form_fields.get("contact_name"),
                "href": "mailto:"+form_fields.get("contact_email")
            },
            "features": eval(form_fields.get("features")),
            "genomicFeatures": eval(form_fields.get("genomic_features"))
        }
    }
    return patient_query

def post_request(server_url,headers,query):
    """ Posts a HTTP request to a server and returns its response

    Args:
        headers (werkzeug.datastructures.Headers)
        server_url(str): url of the server

    Returns:
        json_response: a json-formatted server response
    """
    json_response = None
    try:
        LOG.info('sending HTTP request to server:{}'.format(server_url))
        server_return = requests.request(
            method = 'POST',
            url = server_url,
            headers = headers,
            data = json.dumps(query)
        )
        # get json response:
        try:
            json_response = server_return.json()
        except Exception as json_exp:
            json_response_string = server_return.text.replace('""','","') # fixing json file in the string representation of it
            json_response = eval(json_response_string)
            LOG.info('------->'+str(json_response.keys()))

        LOG.info('server returns the following response: {}'.format(json_response))

    except Exception as err:
        LOG.info('An error occurred while sending HTTP request to server ({})'.format(err))

    return json_response
