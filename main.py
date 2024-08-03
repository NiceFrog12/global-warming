################
#
# THIS SHALL BE THE START OF MY BEST WORK!!!
#
# THE WORLD IS NOT READY FOR WHAT I HAVE PLANNED!!!
#
################


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///facts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "akdqwenqknlnlcashodonasdlkaksd"

db = SQLAlchemy(app)

class Facts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Fact {self.id}>'

if __name__ == "__main__":
    app.run(debug=True)



def create_app():
    return app

def get_db():
    return db