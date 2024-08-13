

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
    language = db.Column(db.String(2), nullable=False)

    def __repr__(self):
        return f'<Fact {self.id}>'





def create_app():
    return app

def get_db():
    return db



@app.route('/')
def language_choosing():
    return render_template('language.html')
    
@app.route('/login/eng')
def login():
    return render_template("login.html") 

@app.route('/login/ru')
def login_ru():
    return render_template("login_ru.html")

@app.route('/browse/ru')
def browsing():
    facts = Facts.query.filter_by(language='ru').order_by(Facts.id).all()
    return render_template('index.html', facts=facts)

@app.route('/browse/eng')
def browsing_eng():
    facts = Facts.query.filter_by(language='eng').order_by(Facts.id).all()
    return render_template('index_eng.html', facts=facts)

#Запуск страницы c картой
@app.route('/card/ru/<int:id>')
def fact(id):
    fact = Facts.query.get(id)
    return render_template('card.html', fact=fact)

@app.route('/card/eng/<int:id>')
def fact_eng(id):
    fact = Facts.query.get(id)
    return render_template('card_eng.html', fact=fact)

@app.route('/create/ru')
def create():
    return render_template('create_card.html')

@app.route('/create/eng')
def create_eng():
    return render_template('create_card_eng.html')


#Форма карты
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']
        language = request.form['language']
        #Создание объкта для передачи в дб

        fact = Facts(title=title, subtitle=subtitle, text=text, language=language)

        db.session.add(fact)
        db.session.commit()
        return redirect('/')
    else:
        return render_template('create_card.html')






if __name__ == "__main__":
    app.run(debug=True)
