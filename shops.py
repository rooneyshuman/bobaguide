from __future__ import print_function  # In python 2.7

from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import bgmodel
import sys
import requests


class Shops(MethodView):
    def get(self):
        """
        GET method for the shops page
        :return: renders the shops.html page on return
        """
        model = bgmodel.get_model()
        settings = bgmodel.get_settings()
        shops = [
            dict(
                name=row[0],
                street=row[1],
                city=row[2],
                state=row[3],
                zip=row[4],
                open_hr=row[5],
                close_hr=row[6],
                phone=row[7],
                drink=row[8],
                rating=row[9],
                website=row[10],
            )
            for row in model.select()
        ]
        key_row = settings.select()[0]
        api_keys = dict(google=key_row[0])
        shop_locations = []
        for shop in shops:
            address = shop["street"] + "+" + shop["city"] + "+" + shop["state"]
            response = requests.get(
                (
                    "https://maps.googleapis.com/maps/api/geocode/json?address={}&key={}"
                ).format(address, api_keys["google"])
            )
            geocode_result = response.json()["results"][0]["geometry"]["location"]
            shop_locations.append(geocode_result)
        return render_template(
            "shops.html", shops=shops, api_keys=api_keys, shop_locations=shop_locations
        )

    def post(self):
        """
        POST method for the shops page. Deletes an entry from the db when called.
        :return: renders the shops.html page on return
        """
        model = bgmodel.get_model()
        model.delete(request.form["name"])
        return redirect(url_for("shops"))
