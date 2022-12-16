import math
import re
from tarfile import BLOCKSIZE

class Bayes_Classifier:

    # goal is to classify a given review as positive or negative
    # dataset contains 1-star and 5-star movie reviews (neg and pos)
    #  train takes a list of lines from the dataset
    # classify takes a list of lines from the dataset, and returns list of strings '1' or '5'

    # a line takes the following form: number of stars | id | text
        # text ends at a \n (newline)
        # can use split('|') to tell when things end

    def __init__(self):
        self.words =  {} 
        self.positivewords = {}
        self.negativewords = {}
        self.numpos = 0
        self.numneg = 0
        self.totalnumpos = 0
        self.totalnumneg = 0
        self.numposrevs = 0
        self.numnegrevs = 0
        self.totalnumrevs = 0
    
    def parse(self, line):
        # parsing the review -- split, remove capitilization, punctuation, and stop words
        line = line.replace('\n', '')
        fields = line.split('|')
        fields[2] = fields[2].lower()
        fields[2] = re.sub('[., !, ?]', ' ', fields[2])
        fields[2] = re.sub('ing', ' ', fields[2])
        fields[2] = re.sub('(\s+)(about|an|and|around|as|at|by|each|i|is|it|my|our|that|the|this|to|we|you|yours)(\s+)', ' ', fields[2])
        return (fields[0], fields[1], fields[2])

    def train(self, lines):
        negatives = []
        positives = []

        for line in lines:
            reviewdata = self.parse(line)
            # if we have a 5-star review, add it text to the list of positives
            # otherwise, add to list of negatives
            if reviewdata[0] == '5':
                positives.append(reviewdata[2]) 
            elif reviewdata[0] == '1':
                negatives.append(reviewdata[2])

        # update fields
        self.numposrevs = len(positives)
        self.numnegrevs = len(negatives)
        self.totalnumrevs = self.numposrevs + self.numnegrevs

        # update positivewords dictionary so that each word in a positive review adds to the count of positives 
        for line in positives:
            textwords = line.split(' ')
            for word in textwords:
                self.numpos += 1
                if word not in self.words:
                    self.words[word] = None 
                    self.positivewords[word] = 1
                    self.negativewords[word] = 0
                else:
                    self.positivewords[word] += 1

        for line in negatives:     
            textwords = line.split(' ')
            for word in textwords:
                self.numneg += 1
                if word not in self.words:
                    self.words[word] = None 
                    self.positivewords[word] = 0
                    self.negativewords[word] = 1
                else:
                    self.negativewords[word] += 1
        
        for word in self.words:
            if self.positivewords[word] > 0:
                self.totalnumpos += 1
            if self.negativewords[word] > 0:
                self.totalnumneg += 1

    def classify(self, lines):
        # initialize list of resulting predictions
        predictions = []

        reviewtexts  = []
        for line in lines:
            reviewdata = self.parse(line)
            reviewtexts.append(reviewdata[2])

        for text in reviewtexts:
            textwords = text.split(' ')
            posprob = math.log(self.numposrevs / self.totalnumrevs)
            negprob = math.log(self.numnegrevs / self.totalnumrevs)
            for word in textwords:
                if word in self.words:
                    # sums instead of products because we used log probabilities to get around underflow problems
                    # implement 1 smoothing
                    posprob += math.log((self.positivewords[word] + 1) / (self.numpos + self.totalnumpos))
                    negprob += math.log((self.negativewords[word] + 1) / (self.numneg + self.totalnumneg))
            if posprob >= negprob:
                predictions.append('5')
            else:
                predictions.append('1')

        return predictions