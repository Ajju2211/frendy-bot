import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()
class Filter:
    def __init__(self,sentence): 
        self.nlp = en_core_web_sm.load()
        self.doc = nlp(sentence)
    def filterWords(self):
        filtered_sentence =([x for x in self.doc if not x.is_stop])
        filtered_sentence = ' '.join(map(str, filtered_sentence))
        return (filtered_sentence)


if __name__ == "__main__":
	fs = Filter("Where can I find fee structure of Semister")
	print(fs.filterWords())