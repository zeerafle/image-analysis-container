from flask import Flask, request, jsonify
from modules.image_analysis import analyze_image
from modules.blob_storage import upload_image_to_blob
from modules.translation import translate_text

app = Flask(__name__)


@app.route('/', methods=['POST'])
def image_analysis():
    file = request.files['image']
    image_url = upload_image_to_blob(file)
    caption = analyze_image(image_url)
    if caption:
        print("Image analysis results:")
        print(" Caption:")
        return jsonify({
            'description': caption,
            'translated_text': translate_text(caption)
        })


if __name__ == '__main__':
    app.run()
