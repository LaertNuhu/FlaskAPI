from flask import Flask, request, jsonify
from dataManipulation import XMLDataframeParser
from normalize import Normalizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd

app = Flask(__name__)
app.config["DEBUG"] = True

parser = XMLDataframeParser()
text = parser.getText("./data/smokingRecords.xml")
parser.addFeatureFromText(text, "HISTORY OF PRESENT ILLNESS :", "", True, True, "illness")
df = parser.getDataframe()
df_xml = parser.removeEmptyEntries(df, "illness")


def getFirstNWords(vec, data, n):
    bag_of_words = vec.fit_transform(data)
    sum_words = bag_of_words.sum(axis=0)
    words_freq = [(word, sum_words[0, idx])
                  for word, idx in vec.vocabulary_.items()]
    words_freq_sorted = sorted(words_freq, key=lambda x: x[1], reverse=True)
    return words_freq_sorted[:n]


def createDataframe(data):
    node1 = []
    node2 = []
    weight = []
    for entry in data:
        nodes = entry[0].split()
        node1.append(nodes[0])
        node2.append(nodes[1])
        weight.append(entry[1])
    df = pd.DataFrame()
    df['Node1'] = node1
    df['Node2'] = node2
    df['Weight'] = weight
    return df


normalizer = Normalizer()
vec2Gram = CountVectorizer(tokenizer=lambda text: normalizer.normalize(text, True, False),ngram_range=(2, 2))

@app.route("/")
def hello():
    return "Hello"

@app.route("/<int:edgeCount>")
def main(edgeCount):
    mostFreq2Grams = getFirstNWords(vec2Gram, df_xml.illness, edgeCount)
    df_graph = createDataframe(mostFreq2Grams)
    GF = nx.from_pandas_edgelist(df_graph, 'Node1', 'Node2', ["Weight"])
    d = json_graph.node_link_data(GF)  # node-link format to serialize
    return jsonify(d)

# code need to be clean -> vectorizers need to be put into a separate class
# lemmatization by the normalize function need to be implemented using a url parameter
@app.route("/count/<int:edgeCount>")
def getNodesByCount(edgeCount):
    return "Not ready"

@app.route("/tfidf/<int:edgeCount>")
def getNodesByTfidf(edgeCount):
    return "Not ready"

@app.route("/count/skipgram/<int:edgeCount>")
def getSkipgramsByCount(edgeCount):
    return "Not ready"

@app.route("/tfidf/skipgram/<int:edgeCount>")
def getSkipgramsByTfidf(edgeCount):
    return "Not ready"

if __name__ == "__main__":
    app.run()
