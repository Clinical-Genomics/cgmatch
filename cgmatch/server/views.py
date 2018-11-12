# -*- coding: utf-8 -*-
import logging
from flask import render_template, flash, current_app, request

from cgmatch import app
from . import controllers

LOG = logging.getLogger(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    data = {}
    if request.method == 'POST':
        flash("POST!")
        # create patient query

    # If connection to db is present get a test patient to populate the patient's form
    if current_app.config.get('MONGO_URI'):
        test_patient_obj = controllers.a_patient()

        if test_patient_obj:
            data['test_patient'] = test_patient_obj



    return render_template('search.html', **data)
