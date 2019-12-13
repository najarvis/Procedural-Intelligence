from flask import Blueprint, render_template, request, session, url_for, redirect, jsonify

BLUEPRINT_WHEEL = Blueprint('wheel', __name__, template_folder='templates')

@BLUEPRINT_WHEEL.route("/wheel")
def wheel():
    return render_template("wheel.html")