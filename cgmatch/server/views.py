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
    if request.method == 'POST':
        # create patient query
        patient_query = controllers.format_query(request.form)
        data['patient_query'] = patient_query

        # query reference server, if available
        refserver_url = current_app.config.get('REFSERVER_URL')
        if refserver_url:

            headers = Headers()
            headers = {'Content-Type': 'application/vnd.ga4gh.matchmaker.v1.0+json', 'Accept': 'application/vnd.ga4gh.matchmaker.v1.0+json', 'X-Auth-Token': request.form.get("token")}
            refserver_response = controllers.post_request(refserver_url, headers, patient_query)
            data['refserver_response']=refserver_response



    # If connection to db is present get a test patient to populate the patient's form
    if current_app.config.get('MONGO_URI'):
        test_patient_obj = controllers.a_patient()

        if test_patient_obj:
            data['test_patient'] = test_patient_obj



    return render_template('search.html', **data)
