"""This will be where I store the miscellaneous functionality of the website"""

from flask import Blueprint, render_template

BLUEPRINT_TOOLS = Blueprint('tools', __name__, template_folder='templates')

#Original TODO: Get the github project hooked up
# Edit: Looks like the project hasn't been updated in a while and the 
# structure of the page it reads from is very different. I'll have to
# write my own.

@BLUEPRINT_TOOLS.route('/tools')
def tools_index():
    """Main tools route. Displays a listing of all tools hosted."""

    return render_template("tools.html")

@BLUEPRINT_TOOLS.route('/tools/wfdata/<search>')
def wfdata_search(search=None):
    if search is None:
        return render_template("wfsearch.html")

    else:
        result_str = wfsearch(search)
        return render_template("wfsearch.html", result=result_str)

@BLUEPRINT_TOOLS.route('/tomato')
def tomato_timer():
    """A pomodoro timer to help me focus"""

    return render_template("pomodoro.html")

def wfsearch(search_string):
    """Will call github.com/lyneca/wfdata to search for the most common places
    to find the searched item, and return them in a string"""
    return ""
