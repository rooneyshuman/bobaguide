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
    """
    def get(self, shop_name, shop_phone, text, target):
        """
        GET method for the translation page
        :return: renders the translation.html page on return
        """
        # Get Yelp reviews to translate
        yelp_reviews = Translation().get_yelp_reviews(shop_name, shop_phone)
        
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

        return render_template("translate_reviews.html", result=result, shop_name=shop_name, shop_phone=shop_phone, yelp_reviews=yelp_reviews)


    def get_yelp_reviews(self, shop_name, shop_phone):
        """
        GET method for the reviews page
        :return: renders the reviews.html page on return
        """
        settings = bgmodel.get_settings()
        key_row = settings.select()[0]
        api_keys = dict(google=key_row[0], yelp=key_row[1])

        # Retrieve yelp id through phone search
        response = requests.get(
            "https://api.yelp.com/v3/businesses/search/phone?phone=+1"
            + shop_phone.replace("-", ""),
            headers={"Authorization": "Bearer " + api_keys["yelp"]},
        )

        # Check for status code of HTTP request to yelp API
        if response.status_code == 200 and response.json()["total"] > 0:
            yelp_id = response.json()["businesses"][0]["id"]

            # Retrieve yelp reviews through yelp id and passes them to reviews template
            response = requests.get(
                "https://api.yelp.com/v3/businesses/" + yelp_id + "/reviews",
                headers={"Authorization": "Bearer " + api_keys["yelp"]},
            )
            if response.status_code == 200:
                raw_reviews = response.json()["reviews"]

                # Format datetime string to mm/dd/yyyy
                for review in raw_reviews:
                    date_time_str = review["time_created"]
                    date_str = datetime.datetime.strptime(
                        date_time_str, "%Y-%m-%d %H:%M:%S"
                    ).date()
                    formatted_date = (
                        str(date_str.month)
                        + "/"
                        + str(date_str.day)
                        + "/"
                        + str(date_str.year)
                    )
                    review["time_created"] = formatted_date

                # Build dictionary of yelp reviews
                yelp_reviews = [
                    dict(
                        id=review["id"],
                        text=review["text"],
                        date=review["time_created"],
                        url=review["url"],
                        user_name=review["user"]["name"],
                        user_img=review["user"]["image_url"],
                    )
                    for review in raw_reviews
                ]
                return yelp_reviews
            else:
                return render_template("404.html", shop_name=shop_name)
        else:
            return render_template("404.html", shop_name=shop_name)