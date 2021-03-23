import os, time
from os.path import join, dirname, realpath
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_assets import Environment, Bundle
from flask_fontawesome import FontAwesome
from celery import Celery
from threading import Thread
from mysign import mySign
from werkzeug.utils import secure_filename
from PIL import Image
from resizeimage import resizeimage

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'ppm'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOADS_PATH

sign = mySign()

text = "It's time for dinner..."
textColor = 0x00a0b0
strokeColor = (255, 255, 255)


# Start Celery client ###############
#app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
#app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
#celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)
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

def resize_image(file):
    with Image.open(file) as image:
        print(image)
        img = resizeimage.resize_contain(image, [64, 32])
        img.save(file, image.format)
        
    #fd_img = open(file, 'r')
    #img = Image.open(file)
    #img = resizeimage.resize_contain(img, [32, 64])
    #img.save(file, img.format)
    #img.save(file,"PNG")
    #fd_img.close()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    if sign.isRunning:
        matrixPowerState = 'checked'
    else:
        matrixPowerState = 'unchecked'

    neoPixlPowerState = 'unchecked'
    return render_template('index.html', matrixSwitchState=matrixPowerState,
                           neoPixlSwitchState=neoPixlPowerState)

@app.route("/matrix")
def matrix():
    lastMessage = sign.myText
    lastTextColor = sign.myTextColor
    lastStrokeColor = sign.myStrokeColor
    lastBgColor = sign.myBackgroundColor
    lastImagePath = sign.myImagePath
    print(lastImagePath)
    if sign.showScrollLeft:
         sLeftState = 'checked'
    else:
        sLeftState = 'unchecked'
    if sign.showScrollRight:
         sRightState = 'checked'
    else:
        sRightState = 'unchecked'
    if sign.showFade:
         sFadeState = 'checked'
    else:
        sFadeState = 'unchecked'
    if sign.showSplit:
         sSplitState = 'checked'
    else:
        sSplitState = 'unchecked'
    if sign.showImage:
         sImageState = 'checked'
    else:
        sImageState = 'unchecked'
    return render_template('matrix.html', lastMessage=lastMessage, lastTextColor=lastTextColor, lastBgColor=lastBgColor,
                           sLeftState=sLeftState, sRightState=sRightState,sFadeState=sFadeState,
                           sSplitState=sSplitState, sImageState=sImageState, lastImagePath=lastImagePath )

@app.route("/strip")
def strip():
    return render_template('strip.html')


@app.route("/setup")
def setup():
    return render_template('setup.html')


@app.route('/MatrixOn')
def matrixOn():
    if not sign.isRunning:
        matrixPowerState = 'checked'
        busyMessageHeader = "Matrix LED Starting"
        sign.startSign()
    return "Nothing"


@app.route('/MatrixOff')
def matrixOff():
    if sign.isRunning:
        sign.stopSign()
        matrixPowerState = 'unchecked'
        busyMessageHeader = "Matrix LED Stopping"
    return "Nothing"


@app.route('/NeoPixlOn')
def neoPixlOn():
    print('Powering NeoPixl Strip On...')
    return "Nothing"


@app.route('/NeoPixlOff')
def neoPixlOff():
    print('Powering NeoPixl Strip Off...')
    return "Nothing"


@app.route('/updateMatrix', methods=["POST"])
def updateMatrix():
    sLeft, sRight, sFade, sSplit, sImage = False, False, False, False, False
    text = request.form['msgtext']
    textColor = request.form['msgcolor']
    strokeColor = request.form['msgstroke']
    bgColor = request.form['msgbg'] 
    if request.form.get('scroll-left'):
        sign.showScrollLeft = True
    else:sign.showScrollLeft = False
    if request.form.get('scroll-right'):
        sign.showScrollRight = True
    else:sign.showScrollRight = False
    if request.form.get('fade'):
        sign.showFade = True
    else:sign.showFade = False    
    if request.form.get('split'):
        sign.showSplit = True
    else:sign.showSplit = False
    if request.form.get('show-image'):
        sign.showImage = True
    else:sign.showImage = False
    sign.makeNewMessage(text,textColor,strokeColor,bgColor)
    return "Nothing"

@app.route('/upload', methods=["POST"])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'msgimage' not in request.files:
            render_template('matrix.html')
        file = request.files['msgimage']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            render_template('matrix.html')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            mySign.myImagePath = "static/uploads/"+filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            resize_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return  redirect(url_for('matrix'))

###########################################


def flaskThread():
    app.run(host='192.168.2.225')


if __name__ == "__main__":
    # Run Flask in own thread
    tFlask = Thread(target=flaskThread).start()
