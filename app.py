from flask import Flask, request, send_file, jsonify, render_template, redirect
from PIL import Image, ImageDraw, ImageChops
import requests
from io import BytesIO

app = Flask(__name__)

MAX_IMAGE_SIZE = (8192, 8192)

def check_image_size(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    width, height = img.size
    if width > MAX_IMAGE_SIZE[0] or height > MAX_IMAGE_SIZE[1]:
        return False
    return True

def crop_image_to_circle(image_url):
    if not check_image_size(image_url):
        return jsonify({"error": "This image is too large! Maximum allowed size is 8K x 8K."}), 413

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    width, height = img.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    circle_radius = min(width, height) // 2
    center_x, center_y = width // 2, height // 2
    bounding_box = (
        center_x - circle_radius,
        center_y - circle_radius,
        center_x + circle_radius,
        center_y + circle_radius,
    )
    draw.ellipse(bounding_box, fill=255)
    original_alpha = img.getchannel('A')
    new_alpha = ImageChops.multiply(original_alpha, mask)
    img.putalpha(new_alpha)
    img = img.crop((bounding_box[0], bounding_box[1], bounding_box[2], bounding_box[3]))

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

def crop_image_to_ellipse(image_url):
    if not check_image_size(image_url):
        return jsonify({"error": "This image is too large! Maximum allowed size is 8K x 8K."}), 413

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    width, height = img.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    original_alpha = img.getchannel('A')
    new_alpha = ImageChops.multiply(original_alpha, mask)
    img.putalpha(new_alpha)

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

def crop_image_to_square(image_url):
    if not check_image_size(image_url):
        return jsonify({"error": "This image is too large! Maximum allowed size is 8K x 8K."}), 413

    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    width, height = img.size
    square_size = min(width, height)
    left = (width - square_size) // 2
    top = (height - square_size) // 2
    right = left + square_size
    bottom = top + square_size
    img = img.crop((left, top, right, bottom))

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

@app.route('/circle', methods=['GET'])
def CIRCLE_crop_image():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        cropped_image = crop_image_to_circle(image_url)
        if isinstance(cropped_image, tuple):
            return cropped_image
        return send_file(cropped_image, mimetype='image/png')
    except Exception as e:
        return render_template('500.html'), 500

@app.route('/ellipse', methods=['GET'])
def ELLIPSE_crop_image():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        cropped_image = crop_image_to_ellipse(image_url)
        if isinstance(cropped_image, tuple):
            return cropped_image
        return send_file(cropped_image, mimetype='image/png')
    except Exception as e:
        return render_template('500.html'), 500
    
@app.route('/square', methods=['GET'])
def SQUARE_crop_image():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        cropped_image = crop_image_to_square(image_url)
        if isinstance(cropped_image, tuple):
            return cropped_image
        return send_file(cropped_image, mimetype='image/png')
    except Exception as e:
        return render_template('500.html'), 500

@app.route("/home")
def home():
    return render_template("home.html"), 200

@app.errorhandler(404)
def err_404(error):
    return render_template('404.html'), 404

@app.errorhandler(403)
def err_403(error):
    return render_template('403.html'), 403

@app.errorhandler(502)
def err_502(error):
    return render_template('502.html'), 502

@app.errorhandler(503)
def err_503(error):
    return render_template('503.html'), 503

@app.errorhandler(500)
def err_500(error):
    return render_template('500.html'), 500

@app.route("/repo")
def repo():
    return redirect("https://github.com/pytmg/cropper")

@app.route("/index")
def index():
    return render_template("index.html"), 200

@app.route("/")
def ROOT():
    return redirect("/home")

if __name__ == "__main__":
    app.run(debug=False)