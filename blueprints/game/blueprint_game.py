"""This blueprint handles the running of the PacMan-JS game."""

import json
from flask import Blueprint, render_template, request, send_from_directory, jsonify

BLUEPRINT_GAME = Blueprint('game', __name__, template_folder='pacmanjs-e', static_url_path='')

@BLUEPRINT_GAME.route('/game')
def view_game():
    """Basic route for PacMan-JS. Simply opens a page with the game on it."""

    return render_template("pages/index.html")

@BLUEPRINT_GAME.route('/<path:requested_file>')
def get_file(requested_file):
    """Handles when the page requests js or css files"""

    if requested_file is not None:
        return send_from_directory(BLUEPRINT_GAME.root_path+'/pacmanjs-e', requested_file)
    return ""

@BLUEPRINT_GAME.route('/get_high_scores')
def get_high_scores():
    """Simply returns the json data of the high score table."""

    data = json.load(open(BLUEPRINT_GAME.root_path+'/pacmanjs-e/high_scores.json'))
    return jsonify(data)

@BLUEPRINT_GAME.route('/update_high_scores', methods=['POST'])
def update_high_scores():
    """Updates the high score table based on json request POST data."""

    data = request.get_json()
    with open(BLUEPRINT_GAME.root_path+'/pacmanjs-e/high_scores.json', 'w') as f:
        json.dump(data, f)
    return jsonify(data)
