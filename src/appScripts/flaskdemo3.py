from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

headline = "House to vote on $2,000 stimulus checks after Trump signs Covid relief and funding bill"
storyUrl = "https://www.cnbc.com/2020/12/28/house-votes-on-2000-stimulus-checks-after-trump-signs-relief-bill.html"
relatedArticles = [
    "https://www.cnbc.com/2020/12/28/house-votes-on-2000-stimulus-checks-after-trump-signs-relief-bill.html",
    "https://www.thedailybeast.com/kim-yo-jong-is-ready-to-become-the-first-woman-dictator-in-modern-history"
]
bias = "center"
sentiment = 1
coverage = [1, 0, 1, 1, 1]

@app.route("/<name>")
def home(name):
    return render_template( "newslist3.html", 
        headline=headline,
        storyUrl=storyUrl, 
        bias=bias,
        sentiment=sentiment,
        coverage=coverage,
        relatedArticles=relatedArticles
        )


if __name__ == "__main__":
    app.run()