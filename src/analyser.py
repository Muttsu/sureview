from google.cloud import language
from google.cloud.language import enums, types
from google.cloud import storage
import os
import numpy as np
from scipy.spatial.distance import cosine
from aylienapiclient import textapi

# Instantiates a client
aylien = textapi.Client("981ee42b", "afcc086b9a3d6392d060b2ed87df8261")
gcl = language.LanguageServiceClient()
gcs = storage.Client()

wordvectors = {}
key_cost = ["cost","price","cheap"]
key_food = ["food","meat","vegetable","fish","egg","desert","sushi","kebab"]
key_service = ["service","waiter","tips","taxes"]

def analyse( text ):
    document = types.Document( #pylint: disable=E1101
        content=text,
        type=enums.Document.Type.PLAIN_TEXT,
    )
    response = gcl.analyze_entity_sentiment(
        document=document,
        encoding_type='UTF32',
    )
    entities = sorted([{"name": entity.name, "score": entity.sentiment.score*5/2+2.5}for entity in response.entities if entity.sentiment.magnitude != 0],
        key = lambda e: str.lower(e['name'])
    )
    rcost = [e['score'] for e in entities if related(e['name'],key_cost)]
    rfood = [e['score'] for e in entities if related(e['name'],key_food)]
    rservice = [e['score'] for e in entities if related(e['name'],key_service)]
    s = aylien.Summarize({"text": text, "language": "en", "sentences_number": 1,"title": "review"})['sentences']
    s = s[0] if len(s) else ""
    return {
        "summary": s,
        "cost": sum(rcost)/len(rcost) if len(rcost) else 0,
        "food": sum(rfood)/len(rfood) if len(rfood) else 0,
        "service": sum(rservice)/len(rservice) if len(rservice) else 0
    }


def init():
    if os.path.isfile('./wordveccommon.txt'):
        print("using local copy of wordvec")
        with open('./wordveccommon.txt', encoding="utf8") as f:
            for line in f:
                l = line.split()
                wordvectors[" ".join(l[:-300])] = np. array([float(x) for x in l[-300:]])
    else:
        bucket = gcs.get_bucket('third-wharf-229116.appspot.com')
        blob = storage.Blob('wordveccommon.txt', bucket)
        raw = blob.download_as_string()

        for line in raw:
            l = line.split()
            wordvectors[l[0]] = np.array([float(x) for x in l[1:]])

    print('hi')


def related(a, b):
    if a not in wordvectors:
        return False
    for k in b:
        if k in wordvectors and cosine(wordvectors[a],wordvectors[k]) < 0.5:
            return True
    return False

