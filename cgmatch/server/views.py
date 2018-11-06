# -*- coding: utf-8 -*-
import logging
from flask import render_template, flash

from cgmatch import app
from . import controllers

LOG = logging.getLogger(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():

    data = {}
    return render_template('search.html', **data)
