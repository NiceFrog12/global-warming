
from flask import Flask, render_template, url_for, request, redirect
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





def create_app():
    return app

def get_db():
    return db



@app.route('/')
def login():
    return render_template('login.html')
    
@app.route('/browse')
def browsing():
    facts = Facts.query.order_by(Facts.id).all()
    return render_template('index.html', facts=facts)


#Запуск страницы c картой
@app.route('/card/<int:id>')
def fact(id):
    fact = Facts.query.get(id)
    return render_template('card.html', fact=fact)


@app.route('/create')
def create():
    return render_template('create_card.html')

#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']
        #Создание объкта для передачи в дб

        fact = Facts(title=title, subtitle=subtitle, text=text)

        db.session.add(fact)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')






if __name__ == "__main__":
    app.run(debug=True)
