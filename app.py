from flask import Flask, render_template
import os, db
app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html', games = db.games.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)