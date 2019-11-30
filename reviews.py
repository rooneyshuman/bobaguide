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

        # Retrieves yelp id through phone search
        response = requests.get("https://api.yelp.com/v3/businesses/search/phone?phone=+1" + shop_phone, headers={"Authorization": "Bearer " + api_keys['yelp']}).json()
        yelp_id = response['businesses'][0]['id']
        
        # Retrieves yelp reviews through yelp id and passes them to reviews template
        raw_reviews = requests.get("https://api.yelp.com/v3/businesses/" + yelp_id + "/reviews", headers={"Authorization": "Bearer " + api_keys['yelp']}).json()['reviews']
        yelp_reviews = [dict(id=review['id'], text=review['text'], date=review['time_created'], url=review['url'], 
            user_name=review['user']['name'], user_img=review['user']['image_url']) for review in raw_reviews]
        return render_template('reviews.html', yelp_reviews=yelp_reviews)

    def post(self):
        """
        POST method for the reviews page.
        :return: renders the reivews.html page on return
        """
        return redirect(url_for('reviews'))
