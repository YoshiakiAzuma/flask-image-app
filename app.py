from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename
from PIL import Image
import math

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['THUMB_FOLDER'] = 'static/uploads/thumbs/'
PER_PAGE = 40

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['THUMB_FOLDER'], exist_ok=True)

def create_thumbnail(image_path, thumb_path):
    img = Image.open(image_path)
    img.thumbnail((200, 200))
    img.save(thumb_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(save_path)

            thumb_path = os.path.join(app.config['THUMB_FOLDER'], filename)
            create_thumbnail(save_path, thumb_path)

            return redirect(url_for('index'))

    page = int(request.args.get('page', 1))
    images = sorted(os.listdir(app.config['THUMB_FOLDER']))
    total_pages = math.ceil(len(images) / PER_PAGE)

    start = (page - 1) * PER_PAGE
    end = start + PER_PAGE
    images_paginated = images[start:end]

    return render_template('index.html', images=images_paginated, page=page, total_pages=total_pages)

@app.route('/image/<filename>')
def image_detail(filename):
    page = request.args.get('page', 1)
    return render_template('detail.html', filename=filename, page=page)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
