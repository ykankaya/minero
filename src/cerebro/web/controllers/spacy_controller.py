from datetime import datetime
from flask import render_template, redirect, request, jsonify
import json
import os
import traceback
import sys
import datetime
import logging;
from cerebro.web.server import app
from cerebro.components import Spacy

logger = logging.getLogger(__name__)
spacy = Spacy()

@app.route('/spacy')
def spacy_index():
   return render_template(
      'spacy/index.html',
      title='Spacy',
   )

@app.route('/spacy/nlp')
def spacy_index_nlp():
   return render_template(
      'spacy/nlp.html',
      title='Spacy',
   )

@app.route('/api/spacy/nlp')
def api_spacy():
    try:
        model = request.args.get('model') if 'model' in request.args else ''
        document = request.args.get('document') if 'document' in request.args else ''
        result = spacy.nlp(model, document)
        return jsonify(result)
    except Exception as e:
        logger.error("\n". join(traceback.format_exception(*sys.exc_info())))
        response = jsonify({"error": str(e)})
        response.status_code = 400
        return response
   
@app.route('/spacy/similarity')
def spacy_index_similarity():
   return render_template(
      'spacy/similarity.html',
      title='Spacy',
   )

@app.route('/api/spacy/similarity')
def api_spacy_similarity():
   model = request.args.get('model') if 'model' in request.args else ''
   document = request.args.get('document') if 'document' in request.args else ''
   similarTo = request.args.get('similarTo') if 'similarTo' in request.args else ''
   result = spacy.similarity(model, document, similarTo)
   return jsonify(result)
    
@app.route('/api/spacy/models/download/<name>')
def api_spacy_models_download(name):
    try:
        spacy.models.download(name)
        return jsonify(spacy.models.get_status())
    except Exception as e:
        logger.error("\n". join(traceback.format_exception(*sys.exc_info())))
        response = jsonify({"error": str(e)})
        response.status_code = 400
        return response

@app.route('/api/spacy/models/load/<name>')
def api_spacy_models_load(name):
    try:
        spacy.models.load(name)
        return jsonify(spacy.models.get_status())
    except Exception as e:
        logger.error("\n". join(traceback.format_exception(*sys.exc_info())))
        response = jsonify({"error": str(e)})
        response.status_code = 400
        return response

@app.route('/api/spacy/models/unload/<name>')
def api_spacy_models_unload(name):
    try:
        spacy.models.unload(name)
        return jsonify(spacy.models.get_status())
    except Exception as e:
        logger.error("\n". join(traceback.format_exception(*sys.exc_info())))
        response = jsonify({"error": str(e)})
        response.status_code = 400
        return response

@app.route('/api/spacy/models/status')
def api_spacy_models_status():
    try:
        return jsonify(spacy.models.get_status())
    except Exception as e:
        logger.error("\n". join(traceback.format_exception(*sys.exc_info())))
        response = jsonify({"error": str(e)})
        response.status_code = 400
        return response