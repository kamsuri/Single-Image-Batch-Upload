# coding=UTF-8
# References: https://thetokenizer.com/2013/05/09/efficient-way-to-extract-the-main-topics-of-a-sentence/
import nltk
from nltk.corpus import brown


# Using brown corpus news categories to train data 
brown_train = brown.tagged_sents(categories='news')
# Regex Expression for comparing the given sentence with the below format and finding tags accordingly
regexp_tagger = nltk.RegexpTagger(
    [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
     (r'(-|:|;)$', ':'),
     (r'\'*$', 'MD'),
     (r'(The|the|A|a|An|an)$', 'AT'),
     (r'.*able$', 'JJ'),
     (r'^[A-Z].*$', 'NNP'),
     (r'.*ness$', 'NN'),
     (r'.*ly$', 'RB'),
     (r'.*s$', 'NNS'),
     (r'.*ing$', 'VBG'),
     (r'.*ed$', 'VBD'),
     (r'.*es$', 'VBZ'),
     (r'.*', 'NN')
     ])
# NLTK tagger classes to define my tagger, trained via Brown Corpus
unigram_tagger = nltk.UnigramTagger(brown_train, backoff=regexp_tagger)
bigram_tagger = nltk.BigramTagger(brown_train, backoff=unigram_tagger)


# semi-CFG
cfg = {}
cfg["NNP+NNP"] = "NNP"  # Concatinating two consecutive Proper Nouns into a phrase   
cfg["NN+NN"] = "NNI"    # Concatinating two consecutive Nouns into a phrase and assigning tag NNI
cfg["NNI+NN"] = "NNI"   # Concatinating a noun with any of the prebuilt phrase and assigning tag NNI
cfg["JJ+JJ"] = "JJ"     # Concatinating two consecutive Adjectives into a phrase
cfg["JJ+NN"] = "NNI"    # Concatinating an adjective and noun into a phrase and assigning tag NNI
cfg["VBG+NNP"] = "NNI"  # Concatinating a proper noun and verb into a phrase and assigning tag NNI
cfg["VBG+NN"] = "NNI"   # Concatinating a noun and verb into a phrase and assigning tag NNI
cfg["VBD+NNP"] = "NNI"  # Concatinating a proper noun and verb(past tense) into a phrase and assigning tag NNI
cfg["VBD+NN"] = "NNI"   # Concatinating a noun and verb(past tense) into a phrase and assigning tag NNI
cfg["VBZ+NNP"] = "NNI"  # Concatinating a proper noun and verb(present tense, 3rd person singular) into a phrase and assigning tag NNI
cfg["VBZ+NN"] = "NNI"   # Concatinating a noun and verb(present tense, 3rd person singular) into a phrase and assigning tag NNI


class NPExtractor(object):

    def __init__(self, sentence):
        self.sentence = sentence
    
    # This function breaks a sentence into individual words
    def tokenize_sentence(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        return tokens
    
    # In this function tags are renamed 
    def normalize_tags(self, tagged):
        n_tagged = []
        for t in tagged:
            if t[1] == "NP-TL" or t[1] == "NP":   # replacing a NP or NP-TL tag with NNP
                n_tagged.append((t[0], "NNP"))
                continue
            if t[1].endswith("-TL"):              # -TL(title) tag is removed
                n_tagged.append((t[0], t[1][:-3]))
                continue
            if t[1].endswith("S"):                # Removing the plural form
                n_tagged.append((t[0], t[1][:-1]))
                continue
            n_tagged.append((t[0], t[1]))
        return n_tagged

    def extract(self):

        tokens = self.tokenize_sentence(self.sentence)
        tags = self.normalize_tags(bigram_tagger.tag(tokens))
        #print tags
        merge = True
        # while loop to merge the words according to the semi-CFG mentioned above
        while merge:
            merge = False
            for x in range(0, len(tags) - 1):
                t1 = tags[x]
                t2 = tags[x + 1]
                key = "%s+%s" % (t1[1], t2[1])
                value = cfg.get(key, '')
                if value:
                    merge = True
                    tags.pop(x)
                    tags.pop(x)
                    match = "%s %s" % (t1[0], t2[0])
                    pos = value
                    tags.insert(x, (match, pos))
                    break

        noun = []
        # for loop for extracting the phrases/words with tags NNP or NNI
        for t in tags:
            if t[1] == "NNP" or t[1] == "NNI":
                noun.append(t[0])
        return noun


def main(sentence):

    np_extractor = NPExtractor(sentence)
    noun = np_extractor.extract()
    return noun
