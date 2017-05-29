import os
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask import current_app as app
from werkzeug.utils import secure_filename
from PIL import Image

blueprint_gallery = Blueprint('gallery', __name__, template_folder='templates')

@blueprint_gallery.route('/gallery')
@blueprint_gallery.route('/gallery/<picture_id>')
def view_gallery(picture_id=None):
    user = None
    if 'user' in session:
        user = session['user']

    if picture_id is None:
        pictures = os.listdir('static/images')
        return render_template("gallery.html", user=user, pictures=pictures)

    if picture_id is not None:
        return render_template("view_image.html", picture_id=picture_id)

@blueprint_gallery.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if 'user' not in session:
        return redirect(url_for('login.view_login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            print('No file part')
            return redirect(request.url)

        uploaded_file = request.files['file']

        if uploaded_file.filename == '':
            flash('No file selected')
            print('No file selected')
            return redirect(request.url)

        if uploaded_file:
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # Resize all images to an acceptable size.
            basewidth = 1600
            im = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            wpercent = (basewidth / im.size[0])
            hsize = int(im.size[1] * wpercent)

            im = im.resize((basewidth, hsize), Image.ANTIALIAS)
            im.save(os.path.join(app.config['UPLOAD_FOLDER'], filename), optimize=True, quality=85)

            return redirect(url_for('gallery.view_gallery'))

    return render_template('upload_file.html')
