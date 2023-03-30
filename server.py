# flask server for the web app

from flask import Flask, request, send_file

from tts import tts

app = Flask(__name__)
app.config['USE_X_SENDFILE'] = True


@app.route('/')
def index():
    return 'home'


@app.route('/tts/<text>/<speaker>')
def tts_test(text, speaker):
    b = tts()
    return send_file(b, mimetype='audio/wav')


@app.route('/tts', methods=['POST'])
def tts_route():
    params = request.get_json()
    b = tts(params["text"], params["speaker"])
    return send_file(b, mimetype='audio/wav')


if __name__ == '__main__':
    app.run()
