from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw
import requests
from io import BytesIO

app = Flask(__name__)

def crop_image_to_circle(image_url):
    # Fetch the image from the URL
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Ensure the image is in RGBA mode for transparency
    img = img.convert("RGBA")

    # Create a circular mask
    width, height = img.size
    mask = Image.new('L', (width, height), 0)  # 'L' mode for single-channel image (grayscale)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, width, height), fill=255)  # Draw a white circle

    # Apply the mask to the image
    img.putalpha(mask)  # Applying the alpha channel (transparency)

    # Save the image to a BytesIO object and return it
    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)  # Move back to the start of the BytesIO object
    return output

@app.route('/circle', methods=['GET'])
def crop_image():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "URL parameter is required"}), 400

    try:
        # Crop the image and get the output
        cropped_image = crop_image_to_circle(image_url)
        return send_file(cropped_image, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
