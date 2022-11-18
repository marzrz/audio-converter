from flask import Flask, jsonify, request
from flask_cors import CORS
import ffmpeg, base64, wave, os

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/', methods=['GET'])
def debug():
      return jsonify({ 'message': 'ok' })

@app.route('/', methods=['POST'])
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
      os.remove("temp.aac")
      os.remove("temp.wav")
      return jsonify(converted_audio)

if __name__ == '__main__':
      import ssl
      context = ssl.SSLContext()
      context.load_cert_chain("/etc/ssl/certs/conversational_ugr_es.pem","/etc/ssl/certs/conversational_ugr_es.key")
      CORS(app)
      app.run(host='0.0.0.0',port=5100,ssl_context=context,debug=False)