from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from actionserver.controllers.faqs.filter import Filter

class BestMatch:
    def __init__(self, list):
        self.list = list
        self.fuzz = fuzz
    
    def getBestMatch(word, threshold = 0.6):
        max_score = 0
        word_idx = 0
        for word in self.list:
            filteredText = Filter(text).filterWords().lower()
            s = self.fuzz.partial_ratio(filteredText ,word)
            if s > max_score:
                max_score = s
                word_idx = i
        
        thresholdReq = threshold*100
        if max_score > thresholdReq:
            return self.list[word_idx]
        else:
            return None

