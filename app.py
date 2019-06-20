from flask import Flask, request, jsonify
from flask_cors import CORS

from dataManipulation import XMLDataframeParser
from normalize import Normalizer
from generateNetwork import NetworkGenerator as NG



app = Flask(__name__)
CORS(app)


# returns graph data where the edge weights are equal to the 2-grams count
@app.route("/count/<int:edgeCount>")
def getNodesByCount(edgeCount):
    centrality = request.args.get("centrality")
    groups = request.args.get("groups")
    degree = False
    closeness= False
    getGroups = False
    if centrality:
        if centrality=="d":
            degree=True
        elif centrality=="c":
            closeness= True
    if groups=="y":
        getGroups = True
    data = NG().generate(edgeCount,False,0,degree,closeness,getGroups)
    return jsonify(data)

# returns graph data where the edge weights are equal to the 2-grams tfidf
@app.route("/tfidf/<int:edgeCount>")
def getNodesByTfidf(edgeCount):
    centrality = request.args.get("centrality")
    groups = request.args.get("groups")
    degree = False
    closeness= False
    getGroups = False
    if centrality:
        if centrality=="d":
            degree=True
        elif centrality=="c":
            closeness= True
    if groups=="y":
        getGroups = True
    data = NG().generate(edgeCount,True,0,degree,closeness,getGroups)
    return jsonify(data)

# returns graph data where the edge weights are equal to the skipgrams count
@app.route("/count/skipgram/<int:edgeCount>")
def getSkipgramsByCount(edgeCount):
    centrality = request.args.get("centrality")
    groups = request.args.get("groups")
    window_size = request.args.get('window_size')
    degree = False
    closeness= False
    getGroups = False
    if centrality:
        if centrality=="d":
            degree=True
        elif centrality=="c":
            closeness= True
    
    if groups=="y":
        getGroups = True

    if window_size:
        data = NG().generate(edgeCount,False,int(window_size),degree,closeness,getGroups)
    else:
        data = NG().generate(edgeCount,False,1,degree,closeness,getGroups)
    
    return jsonify(data)

# returns graph data where the edge weights are equal to the skipgrams tfidf
@app.route("/tfidf/skipgram/<int:edgeCount>")
def getSkipgramsByTfidf(edgeCount):
    centrality = request.args.get("centrality")
    groups = request.args.get("groups")
    window_size = request.args.get('window_size')
    degree = False
    closeness= False
    getGroups = False
    if centrality:
        if centrality=="d":
            degree=True
        elif centrality=="c":
            closeness= True
    
    if groups=="y":
        getGroups = True

    if window_size:
        data = NG().generate(edgeCount,True,int(window_size),degree,closeness,getGroups)
    else:
        data = NG().generate(edgeCount,True,1,degree,closeness,getGroups)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
