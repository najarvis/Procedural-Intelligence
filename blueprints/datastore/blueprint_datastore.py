"""Handles the basic file storage capabilities needed for M3 for the time being."""

from tinydb import TinyDB, Query
from flask import Blueprint, render_template, request, session, url_for, redirect, jsonify, send_from_directory
import json
import os.path
import time

BLUEPRINT_DATA = Blueprint('data', __name__, template_folder='templates')

@BLUEPRINT_DATA.route('/upload_data', methods=['POST'])
def upload_data():
    data = request.get_json(force=True)

    db_name = data['device']
    db = TinyDB('capture_dbs/{}.json'.format(db_name))
    probe_captures = db.table('pcaps')

    device = data["device"]
    for scan in data['scans']:
        new_scan = scan.copy()
        new_scan["device"] = device
        probe_captures.insert(new_scan)

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

@BLUEPRINT_DATA.route('/upload_ip', methods=['POST'])
def upload_ip():
    data = request.get_json(force=True)
    if "ip" not in data or "name" not in data:
        return jsonify({"status": "error", "reason": "payload should have the fields 'ip' and 'name.'"})

    ip = data["ip"]
    name = data["name"]
    t = time.time()

    db = TinyDB('ips.json')
    Device = Query()

    if db.search(Device.name == name):
        db.update({'ip': ip, 'last_seen': t}, Device.name == name)
    else:
        db.insert({'ip': ip, 'name': name, 'last_seen': t})

    return jsonify({"status": "success"})

@BLUEPRINT_DATA.route('/get_ips', methods=['GET'])
def get_ips():
    if 'user' not in session:
        return redirect(url_for('login.view_login', route='data.get_ips'))

    db = TinyDB('ips.json')
    payload = [{"last_seen": "{} seconds ago".format(time.time() - dev["last_seen"]), "ip": dev["ip"], "name": dev["name"]} for dev in db.all()]
    return jsonify(payload)

@BLUEPRINT_DATA.route('/reset_ips', methods=['GET'])
def reset_ips():
    if 'user' not in session:
        return redirect(url_for('login.view_login', route='data.get_ips'))

    db = TinyDB('ips.json')
    db.purge_table('_default')
    return jsonify({"status": "success"})

@BLUEPRINT_DATA.route('/upload-plant-data', methods=['POST'])
def upload_plant_data():
    data = request.get_json(force=True)
    if 'test' not in data:
        return jsonify({"status": "error", "reason": "Payload must have the field: 'test'"})

    with open('data/test_data.txt', 'a') as f:
        f.write("{}\n".format(data['test']))

    return jsonify({"status": "success"})

@BLUEPRINT_DATA.route('/get-plant-data-raw', methods=['GET'])
def get_raw_plant_data():
    with open('data/test_data.txt') as f:
        data = f.read()
        to_send = [[i, float(v)] for i, v in enumerate(data.split('\n')[-25:]) if v != ""]

    # Return the last 100 lines
    return jsonify({"status": "success", "data": to_send})

@BLUEPRINT_DATA.route('/get-plant-data', methods=['GET'])
def get_plant_data():
    return render_template("plant_data.html")