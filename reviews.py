from __future__ import print_function # In python 2.7

from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import bgmodel
import sys
import requests

class Reviews(MethodView):
    def get(self, shop_phone):
        """
        GET method for the reviews page
        :return: renders the reviews.html page on return
        """
        settings = bgmodel.get_settings()
        key_row = settings.select()[0]
        api_keys = dict(google=key_row[0], yelp=key_row[1])

        response = requests.get("https://api.yelp.com/v3/businesses/search/phone?phone=+1" + shop_phone, headers={"Authorization": "Bearer " + api_keys['yelp']})
        return render_template('reviews.html')

    def post(self):
        """
        POST method for the reviews page.
        :return: renders the reivews.html page on return
        """
        return redirect(url_for('reviews'))
