from flask import Flask, request, jsonify
from flask_cors import CORS

from dataManipulation import XMLDataframeParser
from normalize import Normalizer
from generateNetwork import NetworkGenerator as NG



app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    return "Hello"

# code need to be clean -> vectorizers need to be put into a separate class
# lemmatization by the normalize function need to be implemented using a url parameter
@app.route("/count/<int:edgeCount>")
def getNodesByCount(edgeCount):
    centrality = request.args.get("centrality")
    if centrality:
        if centrality=="d":
            data = NG().generate(edgeCount,False,0,True)
            return jsonify(data)
        elif centrality=="c":
            data = NG().generate(edgeCount,False,0,False,True)
            return jsonify(data)
    data = NG().generate(edgeCount)
    return jsonify(data)

@app.route("/tfidf/<int:edgeCount>")
def getNodesByTfidf(edgeCount):
    centrality = request.args.get("centrality")
    if centrality:
        if centrality=="d":
            data = NG().generate(edgeCount,True,0,True)
            return jsonify(data)
        elif centrality=="c":
            data = NG().generate(edgeCount,True,0,False,True)
            return jsonify(data)
    data = NG().generate(edgeCount,True)
    return jsonify(data)

@app.route("/count/skipgram/<int:edgeCount>")
def getSkipgramsByCount(edgeCount):
    centrality = request.args.get("centrality")
    window_size = request.args.get('window_size')
    degree = False
    closeness= False
    if centrality:
        if centrality=="d":
            degree=True
        elif centrality=="c":
            closeness= True
    if window_size:
        data = NG().generate(edgeCount,False,int(window_size),degree,closeness)
    else:
        data = NG().generate(edgeCount,False,1,degree,closeness)
    
    return jsonify(data)

@app.route("/tfidf/skipgram/<int:edgeCount>")
def getSkipgramsByTfidf(edgeCount):
    centrality = request.args.get("centrality")
    window_size = request.args.get('window_size')
    degree = False
    closeness= False
    if centrality:
        if centrality=="d":
            degree=True
        elif centrality=="c":
            closeness= True
    if window_size:
        data = NG().generate(edgeCount,True,int(window_size),degree,closeness)
    else:
        data = NG().generate(edgeCount,True,1,degree,closeness)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
