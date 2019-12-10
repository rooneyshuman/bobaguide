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
from reviews import Reviews


class Translation(MethodView):
    """
    Translates the Reviews page into the target language selected from a menu by the user.
    """

    def get(self, shop_name, shop_phone, target):
        """
        GET method for the translation page
        :return: renders the translation.html page on return
        """
        settings = bgmodel.get_settings()
        key_row = settings.select()[0]
        api_keys = dict(google=key_row[0], yelp=key_row[1])

        # Prevent application from attempting retry (likely due to missing Yelp user image)
        if target == "None":
            return "Target must contain a value"

        # Collect page components to translate
        text_to_translate = [
            "Home",
            "Add Tea Shop",
            "View Tea Shops",
            shop_name,
            "Translate Reviews",
            "View on Yelp",
            "Copyright 2019 Boba Guide",
        ]
        # Get Yelp reviews to translate
        yelp_reviews = Reviews().get_yelp_reviews(shop_name, shop_phone)
        # Extract the username, date, and text to translate for each Yelp review
        for idx, review in enumerate(yelp_reviews):
            text_to_translate.append(yelp_reviews[idx]["user_name"])
            text_to_translate.append(yelp_reviews[idx]["date"])
            text_to_translate.append(yelp_reviews[idx]["text"])

        # Perform POST request to Google Translation API to translate page
        headers = {"content-type": "application/json; charset=utf-8"}
        params = {"q": text_to_translate, "target": target}
        response = requests.post(
            "https://translation.googleapis.com/language/translate/v2?key="
            + api_keys["google"],
            headers=headers,
            params=params,
        )

        # Return JSON-encoded content of the response
        result = response.json()
        translation = result["data"]
        return render_template(
            "translation.html",
            translation=translation,
            shop_name=shop_name,
            shop_phone=shop_phone,
            yelp_reviews=yelp_reviews,
        )
