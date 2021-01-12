from flask import Flask, redirect, url_for, render_template, request
from compute import get_bias, get_sentiment, get_related, get_coverage
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("homepage.html")

@app.route("/search", methods=["POST", "GET"])
def form():
    headline = "None found :/"
    bias = "None found"
    sentiment = "None found"
    related = ["None found"]
    coverage = "None found"
    url1 = "None found"

    if request.method == "POST":
        headline = request.form["hd"]
        url1 = request.form["url"]

        bias = get_bias(url1)
        sentiment = get_sentiment(headline)
        related = get_related(headline)
        coverage = get_coverage(related)

        return render_template("search.html", result=headline, resultURL=url1, headline=headline, bias=bias, sentiment=sentiment, related=related, coverage=coverage, storyURL=url1)
    else:
        return render_template("search.html", result=headline, resultURL=url1, headline=headline, bias=bias, sentiment=sentiment, related=related, coverage=coverage)

@app.route("/documentation")
def documentation():
    return render_template("docs.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug = True)