"""Handles the basic file storage capabilities needed for M3 for the time being."""

from tinydb import TinyDB, Query
from flask import Blueprint, render_template, request, session, url_for, redirect, jsonify, send_from_directory
import json
import os.path

BLUEPRINT_DATA = Blueprint('data', __name__, template_folder='templates')

@BLUEPRINT_DATA.route('/upload_data', methods=['POST'])
def upload_data():
    data = request.get_json(force=True)

    db_name = data['device']
    db = TinyDB('capture_dbs/{}.json'.format(db_name))
    probe_captures = db.table('pcaps')

    for scan in data['scans']:
        probe_captures.insert(scan)

    return jsonify({"status": "success"})

@BLUEPRINT_DATA.route('/download_data', methods=['GET'])
@BLUEPRINT_DATA.route('/download_data/<machine>', methods=['GET'])
def download_data(machine=None):
    if machine is None:
        machine = "ACM-Blue"

    db = TinyDB('capture_dbs/{}.json'.format(machine))
    probe_captures = db.table('pcaps')

    fname = 'data/tmp_{}.json'.format(machine)
    if os.path.isfile(fname):
        os.remove(fname)

    with open(fname, "w") as f:
        f.write(json.dumps(probe_captures.all(), indent=2))

    return send_from_directory('data', "tmp_{}.json".format(machine))

@BLUEPRINT_DATA.route('/purge_scans', methods=['GET'])
def purge_scans():
    """Empty the probe captures database. Cannot be undone."""

    return jsonify({"status": "Currently under constructions."})

    
    if 'user' not in session:
        return redirect('/login')

    db = TinyDB('db.json')
    db.purge_table('pcaps')
    print(db.tables)

    return jsonify({"status": "success"})
