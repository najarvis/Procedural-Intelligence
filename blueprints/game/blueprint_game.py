from flask import Blueprint, render_template, request, url_for

blueprint_game = Blueprint('game', __name__, template_folder='templates', static_folder='static')

@blueprint_game.route('/game')
def view_game():
    return render_template("game.html")

@blueprint_game.route('/grab_script/<script>')
def get_script(script=None):
    if script is None:
        return

    return render_template('scripts/'+script)
