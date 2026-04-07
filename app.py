import os, io, base64
from flask import Flask, render_template, request, jsonify
from rembg import remove, new_session
from PIL import Image

app = Flask(__name__)

# Sirf smallest model use karenge memory bachane ke liye
session = new_session("u2netp")

@app.route('/')
def home():
    # Ab design yahan nahi, Hostinger par rahega
    return "CSC Studio AI Engine is Running!"

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    try:
        if 'photo' not in request.files: return jsonify({'error': 'No file'}), 400
        file = request.files['photo']
        
        input_image = Image.open(file.stream)
        
        # Professional cutting yahan ho rahi hai
        output_image = remove(input_image, session=session)
        
        # Result ko wapas bhejne ke liye convert karna
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        return jsonify({'image': f'data:image/png;base64,{img_base64}'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
