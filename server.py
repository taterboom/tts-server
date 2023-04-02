# flask server for the web app

from flask import Flask, jsonify, request, send_file

from tts import tts, get_speaker_list

app = Flask(__name__)
app.config['USE_X_SENDFILE'] = True


@app.route('/')
def index():
    return 'home'


# @app.route('/tts/<text>/<speaker>')
# def tts_test(text, speaker):
#     b = tts(text, speaker)
#     return send_file(b, mimetype='audio/wav')

@app.route('/tts/speakers', methods=['GET'])
def route_tts_speakers():
    return jsonify(get_speaker_list())

# TODO remove
@app.route('/tts', methods=['POST'])
def route_tts():
    params = request.get_json()
    b = tts(params["text"], params["speaker"])
    if b:
        return send_file(b, mimetype='audio/wav')
    else:
        return "error", 500

@app.route('/tts-enc', methods=['POST'])
def route_tts_enc():
    params = request.get_json()
    b = tts(params["text"], params["speaker"])
    if b:
        return b.getvalue().hex()
    else:
        return "error", 500



if __name__ == '__main__':
    app.run()
