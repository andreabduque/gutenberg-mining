import pandas as pd
import textmining as tm
import os.path
from nltk.corpus import stopwords
import motif
import numpy as np

class View:
    def __init__(self, corpusMeta, corpusFiles):
        #A list of path files of the corpus
        self.corpus = corpusFiles
        self.stop = stopwords.words('english')

        # self.tdm = self.createTDM()
        # self.fdm = self.createFDM()
        #Many more
        # self.whatever = self.whatever()

    #Types available: lemma or standard
    #With or without stopwords
    def createTDM(self, featureType='lemma', stopWords=True):
        tdm = tm.TermDocumentMatrix()
        print('corpus size is ' + str(len(self.corpus)) + ' files')
        for i, file in enumerate(self.corpus):
            if(os.path.isfile(file)):

                tokens = pd.read_csv(file, sep=',')[featureType].dropna(axis=0).tolist()
                #convert to lower case
                tokens = [item.lower() for item in tokens]
                #remove stop words if desired
                if(not stopWords):
                    tokens = [item for item in tokens if item not in self.stop]

                tdm.add_doc(' '.join(tokens))
                print('file ' + str(i))
            else:
                print('error with ' + file)

        if(stopWords):
            tdmFile = featureType +'TDM.csv'
        else:
            tdmFile = featureType + 'NotStopwords' + 'TDM.csv'

        tdm.write_csv(tdmFile, cutoff=1)
        print('tdm finished.')


    def createFDM(self, featureType='lemma', stopWords=True):
        fdm = np.empty((len(self.corpus), 13))
        for i, file in enumerate(self.corpus):
            if(os.path.isfile(file)):

                tokens = pd.read_csv(file, sep=',')[featureType].tolist()
                #convert to lower case, keep nan untouched
                tokens = [x.lower() if not isinstance(x, float) else x for x in tokens]

                fdm[i,:] = np.array(motif.getBookMotifFrequency(tokens))

                # remove stop words if desired
                if(not stopWords):
                    tokens = [item for item in tokens if item not in self.stop]

                print('file ' + str(i))
            else:
                print('error with ' + file)



        if(stopWords):
            fdmFile = featureType +'FDM.csv'
        else:
            fdmFile = featureType + 'NotStopwords' + 'FDM.csv'

        np.savetxt(fdmFile, fdm, delimiter=",")
        print('fdm finished.')


    def getTDM(self):
        return []

    def getFDM(self):
        pass
