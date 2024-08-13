from main import db,Facts, app #to know which database im working with
import random
from sqlalchemy import func

def random_fact_choice(language):
    with app.app_context():
        min_id = db.session.query(func.min(Facts.id)).filter(Facts.language == language).scalar()
        max_id = db.session.query(func.max(Facts.id)).filter(Facts.language == language).scalar()

        if min_id is None or max_id is None:
            return None

        attempts = 0
        max_attempts = 10  # Limit the number of attempts to avoid potential infinite loops

        while attempts < max_attempts:
            random_id = random.randint(min_id, max_id)
            fact = db.session.query(Facts).filter(Facts.id == random_id, Facts.language == language).first()

            if fact:
                return fact

            attempts += 1

        return None
