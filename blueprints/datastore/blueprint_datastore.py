"""Handles the basic file storage capabilities needed for M3 for the time being."""

from tinydb import TinyDB, Query
from flask import Blueprint, render_template, request, session, url_for, redirect, jsonify, send_from_directory
import json
import os.path

BLUEPRINT_DATA = Blueprint('data', __name__, template_folder='templates')

@BLUEPRINT_DATA.route('/upload_data', methods=['POST'])
def upload_data():
    data = request.get_json(force=True)

    db = TinyDB('db.json')
    probe_captures = db.table('pcaps')

    device = data["device"]
    for scan in data['scans']:
        new_scan = scan.copy()
        new_scan["device"] = device
        probe_captures.insert(new_scan)

    return jsonify({"status": "success"})

@BLUEPRINT_DATA.route('/download_data', methods=['GET'])
def download_data():
    db = TinyDB('db.json')
    probe_captures = db.table('pcaps')

    if os.path.isfile('data/tmp.json'):
        os.remove('data/tmp.json')

    with open("data/tmp.json", "w") as f:
        f.write(json.dumps(probe_captures.all(), indent=2))

    return send_from_directory('data', "tmp.json")

@BLUEPRINT_DATA.route('/purge_scans', methods=['GET'])
def purge_scans():
    """Empty the probe captures database. Cannot be undone."""

    if 'user' not in session:
        return redirect('/login')

    db = TinyDB('db.json')
    db.purge_table('pcaps')
    print(db.tables)

    return jsonify({"status": "success"})
