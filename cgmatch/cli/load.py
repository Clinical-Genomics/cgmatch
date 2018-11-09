#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from pprint import pprint as pp
import coloredlogs
import click
import json
from pymongo import MongoClient


coloredlogs.install(level='INFO')
LOG = logging.getLogger(__name__)


@click.option('--json_file', type=click.Path(exists=True), nargs=1, required=True, help='A json file containing data from one or more patients' )
@click.option('--db_uri', type=click.STRING, nargs=1, required=False, help='mongodb database connection string: mongodb://db_user:db_password@db_host:db_port/db_name', default='mongodb://mboxuser:mboxpassword@127.0.0.1:27017/cgmatchbox')
@click.command()
def load(json_file, db_uri=None):
    """load one of more samples to matchbox db

        Args:
            json(Path) : path the the json file containing one or more samples to add to matchbox database
             db_uri(str) : optional, database connection string, if it's not already specified in the config.cfg file

        Returns:
            BAH!
    """
    LOG.info("uploading samples from json file: {}".format(json))



@click.command()
@click.option('--db_uri', type=click.STRING, nargs=1, required=False, help='mongodb database connection string: mongodb://db_user:db_password@db_host:db_port/db_name', default='mongodb://mboxuser:mboxpassword@127.0.0.1:27017/cgmatchbox')
def load_demo(db_uri=None):
    """ Load demo patient data into to matchbox db
        Benchmarking patients from paper: http://onlinelibrary.wiley.com/doi/10.1002/humu.22850
    """

    LOG.info("Loading 50 test patients into to matchbox database")

    demo_patients_path = os.path.abspath(os.path.join(os.getcwd(), 'cgmatch', 'demo', 'resources', 'benchmark_patients.json'))

    patients_collection = patients_connect(db_uri)

    patients = [] # a list of dictionaries

    try:
        with open(demo_patients_path) as json_data:
            patients = json.load(json_data)
            counter = 1
            inserted_patients = []
            for patient in patients:

                # convert patient in matchbox patient
                matchbox_patient = matchbox_patient_obj(patient) # convert json patient to matchbox patient object
                # save patient to database:
                if counter <= 2:
                    LOG.info("\n-------> patient n. "+str(counter)+'\n')
                    inserted_patients.append(add_patient(patients_collection, matchbox_patient))
                counter += 1


    except Exception as err:
        LOG.fatal("An error occurred while importing benchmarking patients: {}".format(err))
        sys.exit()


def add_patient(patients_collection, matchbox_patient):
    """
        Insert a patient into matchbox database

        Args:
            matchbox_patient(dict) : a matchbox patient entity (org.broadinstitute.macarthurlab.matchbox.entities.Patient)

        Returns:
            result.inserted_id(str) : the if of the inserted patient or None if patient couldn't be saved
    """

    LOG.info("Adding patient with ID {} to matchbox database".format(matchbox_patient.get('_id')))
    inserted_id = None
    try:
        inserted_id = patients_collection.insert_one(matchbox_patient).inserted_id
    except Exception as err:
        LOG.fatal("Error while inserting a patient into db: {}".format(err))

    return inserted_id


def matchbox_patient_obj(patient_obj):
    """
        Accepts a json patient and converts it to a matchbox patient

        Args:
            patient_obj(dict): a patient object as in https://github.com/ga4gh/mme-apis

        Returns:
            matchbox_patient(dict) : a matchbox patient entity (org.broadinstitute.macarthurlab.matchbox.entities.Patient)
    """
    # fix patient's features:
    for feature in patient_obj.get('features'):
        feature['_id'] = feature.get('id')
        feature.pop('id')

    matchbox_patient = {
        '_id' : patient_obj['id'],
        '_class' : 'org.broadinstitute.macarthurlab.matchbox.entities.Patient',
        'label' : patient_obj.get('label'),
        'contact' : patient_obj['contact'],
        'features' : patient_obj['features'],
        'genomicFeatures' : patient_obj.get('genomicFeatures'),
        'disorders' : patient_obj.get('disorders'),
        'species' : patient_obj.get('species'),
        'ageOfOnset' : patient_obj.get('ageOfOnset'),
        'inheritanceMode' : patient_obj.get('inheritanceMode')
    }

    return matchbox_patient



def patients_connect(db_uri):
    """connect to matchbox database"""

    LOG.info("Establishing connection with matchbox db..")

    collection = None
    try:
        client = MongoClient(db_uri)
        db_name = db_uri.split('/')[-1]
        db = client[db_name]
        collection = db.patient

    except Exception as err:
        LOG.fatal("Couldn't establish connection to database: {}".format(err))
        sys.exit()

    LOG.info("Connected!")
    return collection
