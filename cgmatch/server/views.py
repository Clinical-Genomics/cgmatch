# -*- coding: utf-8 -*-
import logging
import json
from flask import render_template, flash, current_app, request
from werkzeug.datastructures import Headers
from cgmatch import app
from . import controllers

LOG = logging.getLogger(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    data = {}
    test_patient_obj = None
    if request.method == 'POST':
        # create patient query
        patient_query = controllers.format_query(request.form)
        data['patient_query'] = json.dumps(patient_query)

        mme_servers_urls = [current_app.config.get('REFSERVER_URL'), current_app.config.get('MATCHBOX_URL')] # url to available mme servers
        mme_servers_tokens = [current_app.config.get('REFSERVER_TOKEN'), current_app.config.get('MATCHBOX_TOKEN')] # tokens to available mme servers
        mme_patients = [] #patients returned by querying different mme servers

        index = 0
        for url in mme_servers_urls:
            try:
                headers = Headers()
                content_type = None
                if index==0:
                    content_type = 'application/vnd.ga4gh.matchmaker.v1.0+json'
                else:
                    content_type = 'application/x-www-form-urlencoded'

                headers = {'Content-Type': content_type, 'Accept': 'application/vnd.ga4gh.matchmaker.v1.0+json', "X-Auth-Token": mme_servers_tokens[index]}
                server_response = controllers.post_request(server_url=url, headers=headers, query=patient_query)
                mme_patients.append(server_response)

            except Exception as err:
                flash('An exception has occurred while querying mme service: {}'.format(url), 'danger')

            index += 1

        if len(mme_servers_urls) == 2:
            data['refserver_response'] = mme_patients[0]
            data['matchbox_response'] = mme_patients[1]

        test_patient_obj = controllers.a_patient(patient_id=request.form.get('patients_id')) # get same patient as before the query

    # If connection to db is present get a test patient to populate the patient's form
    else:
        if current_app.config.get('MONGO_URI'):
            test_patient_obj = controllers.a_patient()

    if test_patient_obj:
        data['test_patient'] = test_patient_obj



    return render_template('search.html', **data)
