from flask import Blueprint, render_template, request, url_for, send_from_directory, jsonify
import json

blueprint_game = Blueprint('game', __name__, template_folder='pacmanjs-e', static_url_path='')

@blueprint_game.route('/game')
def view_game():
    return render_template("pages/index.html")

@blueprint_game.route('/<path:file>')
def get_file(file):
	if file is not None:
		return send_from_directory(blueprint_game.root_path+'/pacmanjs-e', file)

@blueprint_game.route('/get_high_scores')
def get_high_scores():
    data = json.load(open(blueprint_game.root_path+'/pacmanjs-e/high_scores.json'))
    return jsonify(data)

@blueprint_game.route('/update_high_scores', methods=['POST'])
def update_high_scores():
    data = request.get_json()
    with open(blueprint_game.root_path+'/pacmanjs-e/high_scores.json', 'w') as f:
        json.dump(data, f)
    return jsonify(data)

# @blueprint_game.route('/grab_script/<script>')
# def get_script(script=None):
#     if script is None:
#         return

#     return render_template('scripts/'+script)
