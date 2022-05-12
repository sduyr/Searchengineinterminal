import crawler as we
import interface as si
import pickle
from os.path import exists
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
import os
import math
from os.path import exists




class SearchEngine():
    def __init__(self, mode, verbosity, query, root, depth):
        self.mode = mode
        self.verbosity = verbosity
        self.query = query
        self.root = root
        self.depth = depth
        self.webcrawl = we.WebCrawler(self.root, self.verbosity)
        self.searchi = si.SearchInterface(self.mode, self, self.query)
        #self.collected_documents = None
        self.collected_links = None

    def train(self):
        '''This function saves cleaned documents or crawled links if the file does not exists otherwise load the cleaned documents'''
        if not os.path.exists("./links.pickle"):
            #pass the depth value here.
            self.webcrawl.collect(self.root, self.depth)
            scraped_links = self.webcrawl.get_links()
            file_name_2 = "links.pickle"
            open_file_2 = open(file_name_2, "wb")
            pickle.dump(scraped_links, open_file_2)
            open_file_2.close()
            #self.compute_tf_idf()
        else:
            open_links = open(os.path.join(os.path.dirname(__file__),"links.pickle"),'rb')
            loaded_links = pickle.load(open_links)
            open_links.close()



        if not os.path.exists("./docs.pickle"):
            self.webcrawl.crawl()
            self.webcrawl.clean()
            cleaned_documents = self.webcrawl.get_documents()
            file_name_1 = "docs.pickle"
            open_file_1 = open(file_name_1, "wb")
            pickle.dump(cleaned_documents, open_file_1)
            open_file_1.close()
            #self.compute_tf_idf()
        '''
        else:
            open_documents = open(os.path.join(os.path.dirname(__file__),"docs.pickle"),'rb')
            loaded_docs = pickle.load(open_documents)
            open_documents.close()
        '''



        #print("def")



        #self.compute_tf_idf()






        return self.compute_tf_idf()



    def delete(self):
        ''' This function deletes the pickle files '''
        if os.path.exists("/Users/Senjuti/AI/project4/docs.pickle"):
            print("Deleting docs.pickle file")
            os.remove("docs.pickle")
            print("docs.pickle file deleted")
        if os.path.exists("/Users/Senjuti/AI/project4/links.pickle"):
            print("Deleting links.pickle file")
            os.remove("links.pickle")
            print("links.pickle file deleted")




    def compute_tf_idf(self):
        ''' This function vectorizes the cleaned documents using Scikit-Learn’s TfidfVectorizor'''

        open_documents = open(os.path.join(os.path.dirname(__file__),"docs.pickle"),'rb')
        #print("ee")
        loaded_docs = pickle.load(open_documents)
        open_documents.close()
        '''
        open_links = open("links.pickle", "rb")
        loaded_links = pickle.load(open_docs)
        open_links.close()
        '''



        tfidf_vectorizer=TfidfVectorizer()

        # Send our docs into the Vectorizer
        tfidf_vectorizer_documents_vectors=tfidf_vectorizer.fit_transform(loaded_docs)
        #tfidf_vectorizer_links_vectors=tfidf_vectorizer.fit_transform(loaded_links)

        # Transpose the result into a more traditional TF-IDF matrix, and convert it to an array.
        X1 = tfidf_vectorizer_documents_vectors.T.toarray()
        #print(X1)
        #X2 = tfidf_vectorizer_links_vectors.T.toarray()

        # Convert the matrix into a dataframe using feature names as the dataframe index.
        df = pd.DataFrame(X1, index=tfidf_vectorizer.get_feature_names_out())
        #self.collected_links = pd.DataFrame(X2, index=tfidf_vectorizer.get_feature_names())
        #print(df)
        return df , tfidf_vectorizer
    def handle_query(self):
        ''' This function vectorize the query, calculate cosine similarity to the texts extracted from the web'''
        dataframe, tfidf_vectorizer = self.train()
        q_vec = tfidf_vectorizer.transform([self.query]).toarray().reshape(dataframe.shape[0],)

        # Calculate cosine similarity.
        sim = {}
        for i in range(len(dataframe.columns)-1):
            sim[i] = np.dot(dataframe.loc[:, i].values, q_vec) / np.linalg.norm(dataframe.loc[:, i]) * np.linalg.norm(q_vec)

            #print("Collected documents analog norm",np.linalg.norm(collected_documents.loc[:, i]))
            #print("Q vector analog norm",np.linalg.norm(q_vec))
            #print("Dot Product",np.dot(collected_documents.loc[:, i].values, q_vec))
            #if np.dot(np.dot(collected_documents.loc[:, i].values, q_vec)) ==0:


        #print(sim.keys())
        #print(sim.values())
        #print(sim.items())

        count = 0
        for x in sim.values():
            count += 1
            if (math.isnan(x)):
                #print(count)
                sim[count -1 ] = 0.0
            #print(x)
        #print(sim.values())






        #print(sim.keys())
        #print(sim.values())





        # Sort the values
        sim_sorted = sorted(sim.items(), key=lambda x: x[1], reverse=True)
        print(sim_sorted)

        # Print the articles and their similarity values
        for k, v in sim_sorted:
            if v != 0.0 :
                open_links = open(os.path.join(os.path.dirname(__file__),"links.pickle"),'rb')
                loaded_links = pickle.load(open_links)
                open_links.close()
                #print("abc")
                print("["+str(k)+"]" + loaded_links[k] +"- (" + str("{:.2f}".format(v)) + ')')
            else:
                print("Your search did not match any documents. Try again.")
    def listen(self):
        ''' This function call the listen() method of the SearchInterface created in the constructor'''
        self.searchi.listen()
