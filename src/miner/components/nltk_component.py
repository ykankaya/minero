import os
import traceback
import sys
import logging
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from miner.services.downloader import Downloader
from miner.services.models import Models
from miner.services.models import Model

logger = logging.getLogger(__name__)

class Nltk:

    def __init__(self):
        self.models = NltkModels()
        pass

    def vader_sentiment_analysis(self, document):
        sid = SentimentIntensityAnalyzer()
        result = sid.polarity_scores(document)
        return {"sentiment": {
                'compound': result['compound'],
                'negative': result['neg'],
                'neutral': result['neu'],
                'positive': result['pos'],
                }
            }


class NltkModels(Models):
   def __init__(self):
       Models.__init__(self);
       self.models_path = os.path.join(self.models_path, 'nltk')

       self.models = dict()
       self.add(Model(
           name = 'nltk',
           description = 'vader_lexicon',
           size = '1MB',
           downloader = NltkDownloader(
               'nltk',
               url='https://www.nltk.org/data.html',
               path=self.models_path)
           ))


class NltkDownloader(Downloader):
   def __init__(self, name, *args, **kwargs):
        Downloader.__init__(self, *args, **kwargs)
        self.name = name
        self.models_path = self.path
        self.ensure_models_path()
        nltk.data.path.append(self.models_path);

   def on_download(self):
        import nltk
        nltk.download('vader_lexicon', download_dir=self.models_path)

   def is_downloaded(self):
       downloaded_models = os.listdir(self.models_path)
       if 'sentiment' in downloaded_models:
           return True
       return False

   def ensure_models_path(self):
      if not os.path.exists(self.models_path):
         os.makedirs(self.models_path)