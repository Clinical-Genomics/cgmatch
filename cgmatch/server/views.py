# -*- coding: utf-8 -*-
import logging
from flask import render_template, flash, request

from cgmatch import app
from . import controllers

LOG = logging.getLogger(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    data = {}

    if request.method == 'POST':

        flash("POST!")
        # create patient query

        #patient_query = controllers.create_query(request.form)
    else:
        benchmark_patients =  controllers.benchmark_patients()
        data['benchmark_patients'] = benchmark_patients

    return render_template('search.html', **data)
