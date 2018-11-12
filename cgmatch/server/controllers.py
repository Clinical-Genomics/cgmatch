import logging
from flask import current_app
from flask_pymongo import PyMongo

LOG = logging.getLogger(__name__)


def a_patient(patient_id=None):
    """ Gets a specific patient when an id is provided,
        otherwise returns a random patient from the 50 benchmark patients

        Args:
            patient_id(str) : the _id of the patient in matchmaker mongodb database

        Returns:
            patient_obj(dic) : a matchmaker patient object
    """
    LOG.info("retrieving a random patient from db")

    mongo = PyMongo(current_app)
    patient_obj = None
    if patient_id == None: # this function should return a test patient
        patient_obj = mongo.db.patient.find_one( {'contact.institution' : "Children's Hospital of Eastern Ontario"} )
    else:
        patient_obj = mongo.db.patient.find_one( {'_id': patient_id} )

    return patient_obj
