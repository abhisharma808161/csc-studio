import os, io, base64
from flask import Flask, render_template, request, jsonify
from rembg import remove, new_session
from PIL import Image
from pillow_heif import register_heif_opener

register_heif_opener()
app = Flask(__name__)
# 100MB limit for large photos
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024 

# Load AI Model once
session = new_session("u2netp-thumbnail")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_background():
    try:
        file = request.files['photo']
        img = Image.open(file.stream).convert("RGBA")
        no_bg_img = remove(img, session=session)
        buffered = io.BytesIO()
        no_bg_img.save(buffered, format="PNG")
        return jsonify({"image": f"data:image/png;base64,{base64.b64encode(buffered.getvalue()).decode()}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- PUBLIC DEPLOYMENT FIX START ---
if __name__ == '__main__':
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is required for public access
    app.run(host='0.0.0.0', port=port)
# --- PUBLIC DEPLOYMENT FIX END ---
