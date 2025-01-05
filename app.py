from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw
import requests
from io import BytesIO

app = Flask(__name__)

def crop_image_to_circle(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGBA")
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
    img.putalpha(mask)
    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

def crop_image_to_ellipse(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGBA")
    width, height = img.size
    mask = Image.new('L', (width, height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)
    img.putalpha(mask)
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
        return send_file(cropped_image, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ellipse', methods=['GET'])
def ELLIPSE_crop_image():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "URL parameter is required"}), 400
    try:
        cropped_image = crop_image_to_ellipse(image_url)
        return send_file(cropped_image, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
