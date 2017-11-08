import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 \
  as Features

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username="677f3028-23f0-46eb-9ab9-36c7b5934e4e",
  password="aXjQMxHcf7qB",
  version="2017-02-27")


def get_sentiment(txt):
    response = natural_language_understanding.analyze(
      text=txt,
      features=[
        Features.Entities(
          emotion=True,
          sentiment=True,
          limit=2
        ),
        Features.Keywords(
          emotion=True,
          sentiment=True,
          limit=2
        )
      ]
    )

    print(json.dumps(response, indent=2))

def get_nlu(data):
    response = natural_language_understanding.analyze(
      text = data,
      features=[
        Features.Entities(
        emotion=True,
        sentiment=True,
        limit=2),

        Features.Keywords(
        emotion=True,
        sentiment=True,
        limit=2),

        Features.Emotion(),
      ]
    )
    info = json.dumps(response, indent=2)
    return response
