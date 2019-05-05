from dataManipulation import XMLDataframeParser
from normalize import Normalizer

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import networkx as nx
from networkx.readwrite import json_graph
import pandas as pd
from nltk.util import skipgrams
from toolz import itertoolz, compose
from toolz.curried import map as cmap, sliding_window, pluck
import community

class NetworkGenerator:

    def generate(self, edgeCount, tfidf = False, window_size = 0, degree = False, closeness = False, groups= False):
        parser = XMLDataframeParser()
        text = parser.getText("./data/smokingRecords.xml")
        parser.addFeatureFromText(text, "HISTORY OF PRESENT ILLNESS :", "", True, True, "illness")
        df = parser.getDataframe()
        df_xml = parser.removeEmptyEntries(df, "illness")
        normalizer = Normalizer()
        if tfidf:
            if window_size == 0:
                vectorizer = TfidfVectorizer(tokenizer = lambda text: normalizer.normalize(text, True, False), ngram_range = (2, 2))
                mostFreq2Grams = self.get_first_n_words(vectorizer, df_xml.illness, edgeCount)
            else:
                vectorizer = TfidfVectorizer(analyzer = lambda text: self.custom_analyser(text, 2, int(window_size)))
                mostFreq2Grams = self.get_first_n_words(vectorizer, normalizer.normalizeArray(df_xml.illness, True, False), edgeCount)
        else:
            if window_size == 0:
                vectorizer = CountVectorizer(tokenizer = lambda text: normalizer.normalize(text, True, False), ngram_range = (2, 2))
                mostFreq2Grams = self.get_first_n_words(vectorizer, df_xml.illness, edgeCount)
            else:
                vectorizer = CountVectorizer(analyzer = lambda text: self.custom_analyser(text, 2, int(window_size)))
                mostFreq2Grams = self.get_first_n_words(vectorizer, normalizer.normalizeArray(df_xml.illness, True, False), edgeCount)
        df_graph = self.create_dataframe(mostFreq2Grams)
        GF = nx.from_pandas_edgelist(df_graph, 'Node1', 'Node2', ["Weight"])
        

        if degree:
            # calculate degree centrality
            degree_centrality = nx.degree_centrality(GF)
            nx.set_node_attributes(GF, degree_centrality, "degree_centrality")
            
        if closeness:
            # calculate closeness centrality    
            closeness_centrality = nx.closeness_centrality(GF) 
            nx.set_node_attributes(GF, closeness_centrality, "closeness_centrality")

        if groups:
            # calculate partitions
            partition = community.best_partition(GF)
            nx.set_node_attributes(GF, partition, "group")

        payload = json_graph.node_link_data(GF)
        return payload

    def custom_analyser(self, token, n, k):
        return compose(cmap(' '.join), skipgrams)(token, n, k)

    def get_first_n_words(self, vec, data, n):
        bag_of_words = vec.fit_transform(data)
        sum_words = bag_of_words.sum(axis = 0)
        words_freq = [(word, sum_words[0, idx])
                    for word, idx in vec.vocabulary_.items()]
        words_freq_sorted = sorted(words_freq, key = lambda x: x[1], reverse = True)
        return words_freq_sorted[:n]


    def create_dataframe(self, data):
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