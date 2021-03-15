from flask import Flask, render_template
from flask_assets import Environment, Bundle

app = Flask(__name__)

#Setup Flask to use scss
assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('styleIndex.scss','styleMatrix.scss','styleStrip.scss','styleSetup.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/matrix")
def matrix():
    return render_template('matrix.html')

@app.route("/strip")
def strip():
    return render_template('strip.html')

@app.route("/setup")
def setup():
    return render_template('setup.html')


if __name__ == "__main__":
    app.run(host='192.168.2.225')
    