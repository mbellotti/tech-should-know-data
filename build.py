import os
import json

def count_tags(tags, article, name):
    found = False
    for a in article["tags"]:
        for t in tags:
            if t["text"] == a:
                t["value"] += 1
                t["items"].append({"title":article["title"], "uri": name})
                found = True
        if not found:
            tags.append({"text":a, "value":1, "items":[{"title":article["title"], "uri": name}]})
    return tags


template = open("index.temp")
ret = json.loads(template.read())

for root, dirs, files in os.walk("articles", topdown=False):
    for name in files:
        f = open(os.path.join(root, name))
        data = json.load(f)
        ret["articles"].append({"title":data["title"], "uri": name})
        ret["tags"] = count_tags(ret["tags"], data, name)

out = open("index.json", "w")
out.write(json.dumps(ret))