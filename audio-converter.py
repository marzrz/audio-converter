from flask import Flask, jsonify, request
from flask_cors import CORS
import ffmpeg, base64, wave, os
import librosa
import soundfile as sf

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

@app.route('/', methods=['GET'])
def debug():
      return jsonify({ 'message': 'ok' })

@app.route('/', methods=['POST'])
def convert_audio():
      print ('Iniciando')
      data = request.get_json()
      temp_file = open("temp.aac", "wb")
      decode_string = base64.b64decode(data['base64'])
      temp_file.write(decode_string)
      temp_file.close()
      print (decode_string)
      audio = (
            ffmpeg
            .input("temp.aac")
            .output("temp.wav", f='wav', )
            .overwrite_output()
            .run()
      )
      # data = open("temp.webm", "r")
      # encoded = base64.b64encode(data)

      # data, samplerate = sf.read("temp.wav")
      # sf.write("temp.wav", data, samplerate)
      # with open("temp.wav", "rb") as wav_file:
      #       wav_data = wave.open(wav_file)
      #       audio_data = wav_data.readframes(wav_data.getnframes())
      with open("temp.wav", 'rb') as f:
            contents = f.read()
            audio_data = base64.standard_b64encode(contents)
      audio_data = audio_data.replace("b'", "")
      audio_data = audio_data.replace("'", "")
      print(audio_data)
      converted_audio = {
            'base64': str(audio_data)
      }
      os.remove("temp.aac")
      os.remove("temp.wav")
      print (converted_audio)
      return jsonify(converted_audio)

if __name__ == '__main__':
      import ssl
      context = ssl.SSLContext()
      context.load_cert_chain("/etc/ssl/certs/conversational_ugr_es.pem","/etc/ssl/certs/conversational_ugr_es.key")
      CORS(app)
      app.run(host='0.0.0.0',port=5100,ssl_context=context,debug=False)
      # CORS(app)
      # app.run(port=5100, debug=False)