from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import requests
import json


def random_quote(lang="en"):
    if not lang.startswith("en") and not lang.startswith("ru"):
        raise AttributeError("language not supported, only en and ru are "
                             "available")
    url = "http://api.forismatic.com/api/1.0/?method=getQuote&lang=" \
          + lang[:2] + "&format=json"
    response = requests.get(url)
    result = json.loads(response.text)
    author = result['quoteAuthor']
    quote = result['quoteText']
    if author == "":
        author = "Anonymous"
    return quote, author


def quote_of_the_day(lang="en"):
    if not lang.startswith("en"):
        raise AttributeError("language not supported, only english is "
                             "available")
    url = "http://quotes.rest/qod.json"
    response = requests.get(url)
    result = json.loads(response.text)["contents"]["quotes"][0]
    author = result['author']
    quote = result['quote']
    if author == "":
        author = "Anonymous"
    return quote, author


class QuotesSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder("random_quote").require(
        'Quotes').require("random"))
    def handle_random_quote(self, message):
        quote, author = random_quote(self.lang)
        self.speak(quote + ". " + author)

    @intent_handler(IntentBuilder("quote_of_the_day").require(
        'Quotes').require("day"))
    def handle_quote_of_the_day(self, message):
        quote, author = quote_of_the_day(self.lang)
        self.speak(quote + ". " + author)


def create_skill():
    return QuotesSkill()


