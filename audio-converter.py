from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS
import ffmpeg
import base64
import wave
import json

def create_app():
    app = Flask(__name__)
    return app

app = create_app()
CORS(app)

@app.route('/converter', methods=['POST'])
def convert_audio():
      data = request.get_json()
      temp_file = open("temp.aac", "wb")
      decode_string = base64.b64decode(data['base64'])
      temp_file.write(decode_string)
      temp_file.close()

      audio = (
            ffmpeg
            .input("temp.aac")
            .output("temp.wav", acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run()
      )

      with open("temp.wav", "rb") as wav_file:
            wav_data = wave.open(wav_file)
            audio_data = wav_data.readframes(wav_data.getnframes())
      print(audio_data)
      converted_audio = {
            'base64': str(audio_data)
      }
      return jsonify(converted_audio)

if __name__ == '__main__':
    app.run(port=8000, debug=True)