import os
import json

def count_tags(tags, article, name):
    for a in article["tags"]:
        try:
            tags[a]["value"] += 1
            tags[a]["items"].append({"title":article["title"], "uri": name})
        except KeyError:
            tags[a] = {"text":a, "value":1, "items":[{"title":article["title"], "uri": name}]}
    return tags

def unpack_tags(tags):
    # dict to list
    tlist = []
    for t in tags:
        tlist.append(tags[t])
    return tlist


template = open("index.temp")
ret = json.loads(template.read())
tags = {}

for root, dirs, files in os.walk("articles", topdown=False):
    for name in files:
        f = open(os.path.join(root, name))
        uri = name.split(".") # Don't want the .json part
        data = json.load(f)
        ret["articles"].append({"title":data["title"], "uri": uri[0]})
        tags = count_tags(tags, data, name)

ret["tags"] = unpack_tags(tags)
out = open("index.json", "w")
out.write(json.dumps(ret))