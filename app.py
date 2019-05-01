from flask import Flask, request, jsonify

from dataManipulation import XMLDataframeParser
from normalize import Normalizer
from generateNetwork import NetworkGenerator as NG



app = Flask(__name__)
app.config["DEBUG"] = True


@app.route("/")
def hello():
    return "Hello"

# code need to be clean -> vectorizers need to be put into a separate class
# lemmatization by the normalize function need to be implemented using a url parameter
@app.route("/count/<int:edgeCount>")
def getNodesByCount(edgeCount):
    data = NG().generate(edgeCount)
    return jsonify(data)

@app.route("/tfidf/<int:edgeCount>")
def getNodesByTfidf(edgeCount):
    data = NG().generate(edgeCount,True)
    return jsonify(data)

@app.route("/count/skipgram/<int:edgeCount>")
def getSkipgramsByCount(edgeCount):
    window_size = request.args.get('window_size')
    if window_size:
        data = NG().generate(edgeCount,False,int(window_size))
    else:
        data = NG().generate(edgeCount,False,2)
    return jsonify(data)

@app.route("/tfidf/skipgram/<int:edgeCount>")
def getSkipgramsByTfidf(edgeCount):
    window_size = request.args.get('window_size')
    if window_size:
        data = NG().generate(edgeCount,True,int(window_size))
    else:
        data = NG().generate(edgeCount,True,3)
    return jsonify(data)

if __name__ == "__main__":
    app.run()
