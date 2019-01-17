"""Handles the basic file storage capabilities needed for M3 for the time being."""

from tinydb import TinyDB, Query
from flask import Blueprint, render_template, request, session, url_for, redirect

BLUEPRINT_DATA = Blueprint('data', __name__, template_folder='templates')

@BLUEPRINT_DATA.route('/upload_data', methods=['POST'])
def upload_data():
    data = get_json()

    db = TinyDB('db.json')
    probe_captures = db.table('probe_captures')

    for scan in data:
        probe_captures.insert(scan)
