from google.cloud import language
from google.cloud.language import enums, types
from google.cloud import storage

# Instantiates a client
gcl = language.LanguageServiceClient()
gcs = storage.Client()



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


