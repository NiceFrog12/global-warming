from sqlalchemy import create_engine, func
import random #use random to get the random id number to get the query by
from main import db,Facts, app #to know which database im working with

#making the engine for pandas
engine = create_engine('sqlite:///instance/facts.db')

#allowing pandas read through the database


def random_fact_choice(language):
    with app.app_context():
        min_id = db.session.query(func.min(Facts.id)).filter(Facts.language == language).scalar()
        max_id = db.session.query(func.max(Facts.id)).filter(Facts.language == language).scalar()

        if min_id is None or max_id is None:
            return None

        random_id = random.randint(min_id, max_id)
        fact = db.session.query(Facts).filter(Facts.id == random_id, Facts.language == language).first()

        return fact
