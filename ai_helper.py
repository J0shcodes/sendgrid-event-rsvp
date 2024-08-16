import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from datetime import datetime

nltk.download("punkt")
nltk.download("averaged_perceptron_tagger")


def generate_description(event_name, event_date):
    tokens = word_tokenize(event_name.lower())

    # Get the part of speech tags
    tagged = pos_tag(tokens)

    # Extract nouns and verbs
    nouns = [word for word, pos in tagged if pos.startswith("NN")]
    verbs = [word for word, pos in tagged if pos.startswith("VB")]

    date_obj = datetime.strptime(event_date, "%Y-%m-%d")
    date_str = date_obj.strftime("%B-%d-%Y")

    if nouns and verbs:
        return f"Join us for a {nouns[0]} {verbs[0]} event on {date_str}. This {' '.join(nouns)} promises to be an exciting occasion for all attendees."
    elif nouns:
        return f"You're invited to our {' '.join(nouns)} event on {date_str}. Don't miss this special occasion!"
    else:
        return f"Mark your calendars for our event on {date_str}. We look forward to seeing you there!"
