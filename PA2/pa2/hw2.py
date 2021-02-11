from pathlib import Path
from flask import Flask, render_template, request
from utils import title_match, load_wapo

app = Flask(__name__)

data_dir = Path("pa2_data")
wapo_path = data_dir.joinpath("wapo_pa2.jl")
wapo_docs_titles, wapo_docs = load_wapo(wapo_path)  # load and process WAPO documents


@app.route("/")
def home():
    """
    home page
    :return:
    """
    return render_template("home.html")


@app.route("/results", methods=["POST"])
def results():
    """
    result page
    :return:
    """
    query_text = request.form["query"]  # Get the raw user query from home page
    matches = [title for title in wapo_docs_titles if title_match(query_text,title)]
    print(matches)
    return render_template("results.html",matches=matches)  # add variables as you wish


@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    """
    "next page" to show more results
    :param page_id:
    :return:
    """
    return render_template("results.html")  # add variables as you wish


@app.route("/doc_data/<doc_id>")
def doc_data(doc_id):
    """
    document page
    :param doc_id:
    :return:
    """
    return render_template("doc.html")  # add variables as you wish


if __name__ == "__main__":
    app.run(debug=True, port=5000)