

import flask


app = flask.Flask(__name__)

@app.route("/")
def home():
    return "<h1>messi mide 10 cm</h1> <h2>tu vieja</h2> <b>esto es unn parrafo</b> <href>https://gopaapp.com</href>"

app.run(debug=True)
