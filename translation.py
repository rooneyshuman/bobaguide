from __future__ import print_function  # In python 2.7

from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import bgmodel
import sys
import requests
import datetime
import six
import json
from google.cloud import translate_v2 as translate
from google.oauth2 import service_account
import os


class Translation(MethodView):
    """
    Translates text into the target language. Target must be an ISO 639-1 language code.
    Is # -*- coding: utf-8 -*- needed at top of page?
    """

    def get(self, shop_name, text, target):
        """
        GET method for the translation page
        :return: renders the translation.html page on return
        """
        key_path = "bobaguide-84a4975c26d7.json"
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

        translate_client = translate.Client()

        if isinstance(text, six.binary_type):
            text = text.decode("utf-8")

        result = translate_client.translate(text, target_language=target)
        translation = result["translatedText"]

        print(u"Text: {}".format(result["input"]))
        print(u"Translation: {}".format(result["translatedText"]))
        print(u"Detected source language: {}".format(result["detectedSourceLanguage"]))

        return render_template("translation.html", result=result, shop_name=shop_name)
