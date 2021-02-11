import os,json
from typing import Dict, Union


def title_match(query: str, title: str) -> bool:
    for word in query.split(" "):
        if word in title:
            return True        #if a match between a search term and the title is found return true


def load_wapo(wapo_jl_path: Union[str, os.PathLike]) -> Dict[str, Dict]:
    """
    output dictionary should be of the following format:
    {
      "2ee2b1ca-33d9-11e1-a274-61fcdeecc5f5": {
        "id": "2ee2b1ca-33d9-11e1-a274-61fcdeecc5f5",
        "title": "Many Iowans still don't know who they will caucus for",
        "author": "Jason Horowitz",
        "published_date": 1325380672000,
        "content_str": "Iran announced a nuclear fuel breakthrough and test-fired ..."
      },
      "another id": {...}
    }

    "content_str" is a new field that you need to generate. The value of "content_str" is the concatenation of
    content values that are typed as "sanitized_html" from "contents" field.

    """
    output = {}
    titles = {}
    with open(wapo_jl_path,"r") as wapo:                             # open file
        for line in wapo.read().splitlines():                        #read line by line
            doc = json.loads(line)                                   #unpack json
            content = ""
            for cont in doc["contents"]:
                if "subtype" in cont and cont["subtype"] == "paragraph":
                    content = content +" "+ cont["content"]         #build text content from paragraphs
            output[doc["id"]] ={                                    #build dictionary for document
                "id":doc["id"],
                "title":doc["title"],
                "author":doc["author"],
                "published_date":doc["published_date"],
                "content_str": content
            }
            titles[doc["title"]] = doc["id"]
    return titles,output
