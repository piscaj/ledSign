from flask import Flask, render_template, request
from flask_assets import Environment, Bundle
from flask_fontawesome import FontAwesome
from celery import Celery
from threading import Thread
from sign import start, status, onOff

app = Flask(__name__)

# Start Celery client ###############
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)
#####################################

# Setup Flask to use scss ###########
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('scss/styleIndex.scss', 'scss/styleMatrix.scss', 'scss/styleStrip.scss',
              'scss/styleSetup.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)
#####################################

# Flask FontAwseome #################
fa = FontAwesome(app)
#####################################

# Flask Routes ######################
@app.route("/")
def index():
    mstate = status()
    print(status)
    if mstate == 1:
        matrixPowerState = 'checked'
    else:
        matrixPowerState = 'unchecked'
    neoPixlPowerState = 'unchecked'
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
    mstate = status()
    print(status)
    if mstate == 1:
        matrixPowerState = 'checked'
    else:
        onOff(1)
        m = Thread(target=start)
        m.start()
        matrixPowerState = 'unchecked'
    return render_template('index.html', matrixSwitchState=matrixPowerState)


@app.route('/MatrixOff')
def matrixOff():
    onOff(0)
    mstate = status()
    print(status)
    if mstate == 1:
        matrixPowerState = 'checked'
    else:
        matrixPowerState = 'unchecked'
    return render_template('index.html', matrixSwitchState=matrixPowerState)


@app.route('/NeoPixlOn')
def neoPixlOn():
    print('Powering NeoPixl Strip On...')
    return "Nothing"


@app.route('/NeoPixlOff')
def neoPixlOff():
    print('Powering NeoPixl Strip Off...')
    return "Nothing"
###########################################


def flaskThread():
    app.run(host='192.168.2.225', debug=False)


if __name__ == "__main__":
    # Run Flask in own thread
    tFlask = Thread(target=flaskThread).start()
