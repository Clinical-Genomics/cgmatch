#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import click

from .load import load, load_demo

LOG = logging.getLogger(__name__)


@click.group()
def base():
    """entry point of the cli"""


base.add_command(load)
base.add_command(load_demo)
