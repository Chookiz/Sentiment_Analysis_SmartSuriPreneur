import pandas as pd
import numpy as py
import joblib
import psycopg2
import nltk
from nltk.tokenize import word_tokenize
from deep_translator import GoogleTranslator
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from pydantic import BaseModel
from typing import Annotated

nltk.download('punkt')
nltk.download('stopwords')

# Creating a base model using pydantic for the Reviews
class ReviewBase(BaseModel):
    name: str
    sold: float | None = None
    price: float | None = None
    stock: float | None = None
    comment: str
    sentiment: int | None = None
    kategori: str | None = None

class Sentiment:
    
    # Load models and vectorizer
    vectorizer = joblib.load('vectorizer.pkl')
    nb_model = joblib.load('nb_model.pkl')
    svm_model = joblib.load('svm_model.pkl')
    lr_model = joblib.load('lr_model.pkl')

    def __init__(self, comment, name):
        self.comment = comment # Extract the review text from the tuple
        self.name = name
        # Tokenization
        tokens = word_tokenize(self.comment)

        # Lowercasing
        tokens = [word.lower() for word in tokens]

        # Removing Punctuation
        tokens = [word for word in tokens if word.isalnum()]

        self.text = ' '.join(tokens)

        short_form_dict = {
        'x': 'tak',
        'tk': 'tak',
        'dlm': 'dalam',
        'd': 'di',
        'utk': 'untuk',
        'd': 'di',
        'ap': 'apa',
        'nk': 'nak',
        'tp': 'tapi',
        'tpi': 'tapi',
        'dgn': 'dengan',
        'sgt': 'sangat',
        'brg': 'barang',
        'shj': 'sahaja',
        'kpd': 'kepada',
        'mkn': 'makan',
        'dri': 'dari',
        'yg': 'yang',
        'mmg': 'memang',
        'sy': 'saya',
        'blh': 'boleh',
        'dh': 'dah',
        'lmbt': 'lambat',
        'nk': 'nak',
        'sbb': 'sebab',
        'lpas': 'lepas',
        'plak': 'pulak',
        'cri': 'cari',
        'dpat': 'dapat',
        'dpt':'dapat',
        'dtg': 'datang',
        'bg': 'bagi',
        'mcm': 'macam',
        'klo': 'kalau',
        'klu': 'kalau',
        'btg': 'batang',
        'smpai': 'sampai',
        'jg': 'juga',
        'bnyk': 'banyak',
        'sket': 'sikit',
        'ckp': 'cakap',
        'knape': 'kenapa',
        'knpe': 'kenapa',
        'sdp': 'sedap',
        'pkai': 'pakai',
        'skt': 'sikit',
        'wt': 'buat',
        'thu': 'tahu',
        'blas': 'balas',
        'dr': 'dari',
        'pnh': 'pernah',
        'fham': 'faham',
        'rse': 'rasa',
        'dlm': 'dalam',
        'hbis': 'habis',
        'bnyk': 'banyak',
        'mkn': 'makan',
        'cpt': 'cepat',
        'sni': 'sini',
        'dkt': 'dekat',
        'msh': 'masih',
        'byk': 'banyak',
        'bli': 'beli',
        'amik':'ambik',
        'selmt':'selamat',
        'org':'orang',
        'bkn': 'bukan',
        'pn': 'pun',
        'tq': 'terima kasih',
        'lg': 'lagi',
        'amk': 'ambik',
        'trus': 'terus',
        'bpe': 'berapa',
        'plg': 'paling',
        'g':'pergi'

        }

        # Tokenize the text
        tokens = word_tokenize(self.text)

        # Expand short-form words using the custom dictionary
        expanded_tokens = [short_form_dict.get(token.lower(), token) for token in tokens]

        # Join the tokens back into a single string
        self.expanded_text = ' '.join(expanded_tokens)

        self.translated = GoogleTranslator(source='auto', target='ms').translate(self.expanded_text)

        text = self.translated
        text = "".join(token.lower() for token in text) #Lowercasing
        text = re.sub(r"\d", " ", text) #Remove numbers
        text = re.sub(r"[,-/<>?;''=""\|*!\_&^%#+`~]\{\}\[\]\(\)", " ", text, flags = re.I) #Remove multiple punctuations
        text = re.sub(r"[^\w]", " ", text) #Remove non-alphanumeric symbols whitespaces
        text = re.sub(r"(\w*)(hah|gag)(\w*)", "haha", text) #Convert variation of 'haha'
        text = re.sub(r"\b(ahakz|ahsbahaba|ha+ha|shsjsjs)\b", "haha", text) #Convert variation of 'haha'
        text = re.sub(r"(\w*)(huh)(\w*)", "huhu", text) #Convert variation of 'huhu'
        text = re.sub(r"(\w*)(heh)(\w*)", "hehe", text) #Convert variation of 'hehe'
        text = re.sub(r"(\w*)(hoh)(\w*)", "hoho", text) #Convert variation of 'hoho'
        text = re.sub(r"(\w*)(hih|hikh|sksksksksks)(\w*)", "hihi", text) #Convert variation of 'hihi'
        text = re.sub(r"(\w*)(kahk|kakaka)(\w*)", "kahkah", text) #Convert variation of 'kahkah'
        text = re.sub(r"(\w*)(keke)(\w*)", "keke", text) #Convert variation of 'keke'
        text = re.sub(r"(\w*)(kihk)(\w*)", "kihkih", text) #Convert variation of 'kihkih'
        text = re.sub(r"\b(eleh)(\w*)", "eleh", text) #Convert variation of 'eleh'
        text = re.sub(r"(\w*)(wkwk)(\w*)", "wakawaka", text) #Convert variation of 'wakawaka'
        text = re.sub(r"(alolo)(\w*)", "alolo", text) #Convert variation of 'alolo'
        text = re.sub(r"\b(aish+|ish+|eish)\b", "cis ", text) #Convert variation of 'cis'
        text = re.sub(r"\b(arg+h|argh+|a+rgh|arh+|urgh)\b", "ah", text) #Convert variation of 'ah'
        text = re.sub(r"\b(pew|pfts|prft)\b", "ah", text) #Convert variation of 'fuh'
        text = re.sub(r"\b(ddk)\b", "duduk", text) #Convert variation of 'duduk'

        text = re.sub(r"a+\b", "a", text) #Remove multiple 'a' to a single 'a'
        text = re.sub(r"\ba+", "a", text) #Remove multiple 'a' to a single 'a'
        text = re.sub(r"b+", "b", text) #Remove multiple 'b' to a single 'b'
        text = re.sub(r"c+", "c", text) #Remove multiple 'c' to a single 'c'
        text = re.sub(r"d+", "d", text) #Remove multiple 'd' to a single 'd'
        text = re.sub(r"e+\b", "e", text) #Remove multiple 'e' to a single 'e'
        text = re.sub(r"f+\b", "f", text) #Remove multiple 'f' to a single 'f'
        text = re.sub(r"g+\b", "g", text) #Remove multiple 'g' to a single 'g'
        text = re.sub(r"h+", "h", text) #Remove multiple 'h' to a single 'h'
        text = re.sub(r"i+", "i", text) #Remove multiple 'i' to a single 'i'
        text = re.sub(r"j+", "j", text) #Remove multiple 'j' to a single 'j'
        text = re.sub(r"k+", "k", text) #Remove multiple 'k' to a single 'k'
        text = re.sub(r"ll*\b", "l", text) #Remove multiple 'l' to a single 'l'
        text = re.sub(r"m+", "m", text) #Remove multiple 'm' to a single 'm'
        text = re.sub(r"n+", "n", text) #Remove multiple 'n' to a single 'n'
        text = re.sub(r"o+\b", "o", text) #Remove multiple 'o' to a single 'o'
        text = re.sub(r"p+", "p", text) #Remove multiple 'p' to a single 'p'
        text = re.sub(r"q+", "q", text) #Remove multiple 'q' to a single 'q'
        text = re.sub(r"r+", "r", text) #Remove multiple 'r' to a single 'r'
        text = re.sub(r"s+", "s", text) #Remove multiple 's' to a single 's'
        text = re.sub(r"t+", "t", text) #Remove multiple 't' to a single 't'
        text = re.sub(r"u+\b", "u", text) #Remove multiple 'u' to a single 'u'
        text = re.sub(r"v+", "v", text) #Remove multiple 'v' to a single 'v'
        text = re.sub(r"w+", "w", text) #Remove multiple 'w' to a single 'w'
        text = re.sub(r"x+", "x", text) #Remove multiple 'x' to a single 'x'
        text = re.sub(r"y+", "y", text) #Remove multiple 'y' to a single 'y'
        text = re.sub(r"z+", "z", text) #Remove multiple 'z' to a single 'z'

        text = re.sub(r"(?<!a)(?<!e)(?<!i)(?<!o)(?<!u)(?<!l)(?<!g)(lah|la|le|lo|lar|ler|lor|lh)\b", "la", text) #Normalizing 'la'
        text = re.sub(r"(?<!ta)(?<!ha)(?<!pu)(?<!dit)(nya|nye|nyo|nyer)\b", "nya", text) #Normalizing 'nya'
        text = re.sub(r"(?<!ta)(?<!ha)(?<!pu)(?<!dit)nya\b", "", text) #Remove 'nya'
        text = re.sub(r"\b(tny|tnyk|taye|taya|tanya|tanye|tanyo|tanyer)\b", " tanya ", text) #Convert variation of 'tanya'
        text = re.sub(r"\b(ditnya)\b", "ditanya", text) #Convert variation of 'ditanya'
        text = re.sub(r"\b(pny|punya|punye|punyo|punyer)\b", " punya ", text) #Convert variation of 'punya'
        text = re.sub(r"\b(x)", "tak", text) #Replace 'x' with 'tak'
        text = re.sub(r"\b(tk)\b", "tak", text) #Convert variation of 'tak'
        text = re.sub(r"\b(tk)(?!a)(?!e)(?!at)(?!jut)", "tak", text) #Convert variation of 'tak'
        text = re.sub(r"\b(tak)(?!ut)(?!jut)(?!ejut)(?!ot)(?!raw)(?!at)(?!sub)(?!tik)", "tak", text) #Convert variation of 'tak'
        text = re.sub(r"\b(eluar)\b", "keluar", text) #Convert variation of 'keluar'
        text = re.sub(r"\b(k|okay|okei|oke|kei|okeh)\b", "ok", text) #Convert variation of 'ok'
        text = re.sub(r"\b(hei|hey)\b", "hai", text) #Convert variation of 'hai'
        text = re.sub(r"\b(eyh|ey|ei|e+h)\b", "eh", text) #Conveelokrt variation of 'eh'
        text = re.sub(r"\b(wey|weyh|we+i)\b", "weh", text) #Convert variation of 'weh'
        text = re.sub(r"\b(weiaku)\b", "weh aku", text) #Convert variation of 'weh aku'
        text = re.sub(r"\b(wow|woah)\b", "wah", text) #Convert variation of 'wah'
        text = re.sub(r"\b(wo+i|woit|woy)\b", "woi", text) #Convert variation of 'woi'
        text = re.sub(r"\b(hk|huk|ho)\b", "hok", text) #Convert variation of 'hok'
        
        self.cleaned_text=text

    def view(self):
        return self.main()

    def main(self):

        text_as_list = [self.cleaned_text]

        # Process the review
        X_vec = self.vectorizer.transform(text_as_list)

        # Make predictions
        nb_preds = self.nb_model.predict(X_vec).astype(float)
        svm_preds = self.svm_model.predict(X_vec).astype(float)
        lr_preds = self.lr_model.predict(X_vec).astype(float)

        weights = [0.35, 0.33, 0.34]

        # Calculate weighted sum of predictions
        weighted_sum = weights[0] * nb_preds + weights[1] * svm_preds + weights[2] * lr_preds
        self.weighted_prediction = sum(weighted_sum)

        # Extract the sentiment value from the list based on the index
        selected_sentiment = int(self.weighted_prediction)

        return selected_sentiment
