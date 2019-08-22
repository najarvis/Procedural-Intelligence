"""This will be where I store the miscellaneous functionality of the website"""

from flask import Blueprint, render_template

BLUEPRINT_TOOLS = Blueprint('tools', __name__, template_folder='templates')

#TODO: Get the github project hooked up
#TODO: Register this blueprint in the main file.

@BLUEPRINT_TOOLS.route('/tools')
def tools_index():
    """Main tools route. Displays a listing of all tools hosted."""

    render_template("tools.html")

@BLUEPRINT_TOOLS.route('/tools/wfdata/<search>')
def wfdata_search(search=None):
    if search is None:
        render_template("wfsearch.html")

    else:
        result_str = wfsearch(search)
        render_template("wfsearch.html", result=result_str)

def wfsearch(search_string):
    """Will call github.com/lyneca/wfdata to search for the most common places
    to find the searched item, and return them in a string"""
    return ""
