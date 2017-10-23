from flask import Blueprint, render_template, request, url_for, send_from_directory

blueprint_game = Blueprint('game', __name__, template_folder='pacmanjs-e', static_url_path='')

@blueprint_game.route('/game')
def view_game():
    return render_template("pages/index.html")

@blueprint_game.route('/<path:file>')
def get_file(file):
	if file is not None:
		return send_from_directory(blueprint_game.root_path+'/pacmanjs-e', file)


# @blueprint_game.route('/grab_script/<script>')
# def get_script(script=None):
#     if script is None:
#         return

#     return render_template('scripts/'+script)
