from sqlalchemy import create_engine, func
import random #use random to get the random id number to get the query by
from main import db,Facts, app #to know which database im working with

#making the engine for pandas
engine = create_engine('sqlite:///instance/facts.db')

#allowing pandas read through the database


def random_fact_choice():
    with app.app_context():
        # Get min and max ID from the database
        min_id = db.session.query(func.min(Facts.id)).scalar()
        max_id = db.session.query(func.max(Facts.id)).scalar()

        if min_id is None or max_id is None:
            return None  # Return None if no rows are found

        # Generate a random ID
        random_id = random.randint(min_id, max_id)

        # Get the fact with the random ID
        fact = db.session.query(Facts).filter(Facts.id == random_id).first()

        return fact