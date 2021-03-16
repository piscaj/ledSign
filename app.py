from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
from flask_fontawesome import FontAwesome

app = Flask(__name__)

# Setup Flask to use scss
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/styleIndex.scss', 'scss/styleMatrix.scss', 'scss/styleStrip.scss',
              'scss/styleSetup.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)

fa = FontAwesome(app)


@app.route("/")
def index():
    matrixPowerState = 'checked'
    neoPixlPowerState = 'checked'
    return render_template('index.html', matrixSwitchState=matrixPowerState,
                           neoPixlSwitchState=neoPixlPowerState)


@app.route("/matrix")
def matrix():
    return render_template('matrix.html')


@app.route("/strip")
def strip():
    return render_template('strip.html')


@app.route("/setup")
def setup():
    return render_template('setup.html')


@app.route('/MatrixOn')
def matrixOn():
    print('Powering Matrix Led On...')
    return "Nothing"


@app.route('/MatrixOff')
def matrixOff():
    print('Powering Matrix Led Off...')
    return "Nothing"


@app.route('/NeoPixlOn')
def neoPixlOn():
    print('Powering NeoPixl Strip On...')
    return "Nothing"


@app.route('/NeoPixlOff')
def neoPixlOff():
    print('Powering NeoPixl Strip Off...')
    return "Nothing"


if __name__ == "__main__":
    app.run(host='192.168.2.225')
