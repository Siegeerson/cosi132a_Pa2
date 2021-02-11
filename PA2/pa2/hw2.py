from pathlib import Path
from flask import Flask, render_template, request, Markup
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
    if not query_text:
    	matches =[]
    else:
    	matches = []
    	for title in wapo_docs_titles:
    		if title_match(query_text,title):
    			doc_id = wapo_docs_titles[title]
    			doc = wapo_docs[doc_id]
                # NOTE: I dont escape the snipit because it causes issues with unfinished html tags
    			snipit = doc["content_str"][:150]
    			matches.append((title,doc_id,snipit))
    return render_template("results.html",matches=matches[:min(8,len(matches))],page=1,query=query_text,maxpages=len(matches)//8)  # add variables as you wish

# Current iteration of next page--> re-does search with a different page #
@app.route("/results/<int:page_id>", methods=["POST"])
def next_page(page_id):
    """
    "next page" to show more results
    :param page_id:
    :return:
    """
    query_text = request.form["query"]
    if not query_text:
    	matches =[]
    else:
    	matches = []
    	for title in wapo_docs_titles:
    		if title_match(query_text,title):
    			doc_id = wapo_docs_titles[title]
    			doc = wapo_docs[doc_id]
    			snipit = doc["content_str"][:150]
    			matches.append((title,doc_id,snipit))
    return render_template("results.html",matches=matches[8*page_id:min(len(matches),8*(page_id+1))],page=page_id+1,query=query_text,maxpages=len(matches)//8)  # add variables as you wish


@app.route("/doc_data/<doc_id>")
def doc_data(doc_id):
    """
    document page
    :param doc_id:
    :return:
    """
    print("DOC ID",doc_id)
    return render_template("doc.html",doc=wapo_docs[doc_id],text=Markup(wapo_docs[doc_id]["content_str"]))  # add variables as you wish


if __name__ == "__main__":
    app.run(debug=True, port=5000)
