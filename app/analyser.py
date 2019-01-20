from google.cloud import language
from google.cloud.language import enums, types
from google.cloud import storage
import os
import numpy as np
from scipy.spatial.distance import cosine
from math import sqrt

# Instantiates a client
gcl = language.LanguageServiceClient()
gcs = storage.Client()

wordvectors = {}

def analyse( text ):
    document = types.Document( #pylint: disable=E1101
        content=text,
        type=enums.Document.Type.PLAIN_TEXT,
    )
    response = gcl.analyze_entity_sentiment(
        document=document,
        encoding_type='UTF32',
    )
    entities = response.entities
    return sorted([{"name": entity.name, "score": entity.sentiment.score*5/2+2.5}for entity in entities],
        key = lambda e: str.lower(e['name'])
    )

if os.path.isfile('./wordvec.txt'):
    with open('./wordvec.txt') as f:
        raw = f.readlines()
else:
    bucket = gcs.get_bucket('third-wharf-229116.appspot.com')
    blob = storage.Blob('wordvec.txt', bucket)
    raw = blob.download_as_string()

for line in raw:
    l = line.split()
    wordvectors[l[0]] = np.array([float(x) for x in l[1:]])

def related(a, b):
    return cosine(wordvectors[a],wordvectors[b]) < 0.36

