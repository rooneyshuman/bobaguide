from __future__ import print_function # In python 2.7

from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import bgmodel
import sys
import requests

class Reviews(MethodView):
    def get(self, shop_phone):
        """
        GET method for the shops page
        :return: renders the shops.html page on return
        """
        settings = bgmodel.get_settings()
        key_row = settings.select()[0]
        api_keys = dict(google=key_row[0], yelp=key_row[1])

        r = requests.get("https://api.yelp.com/v3/businesses/search/phone?phone=+19712291617", headers={"Authorization": "Bearer " + api_keys.yelp})
        print(r.text)
        return render_template('index.html', api_keys=api_keys)

    def post(self):
        """
        POST method for the shops page. Deletes an entry from the db when called.
        :return: renders the shops.html page on return
        """
        return redirect(url_for('shops'))
