from flask import render_template
from flask.views import MethodView
from settings_datastore import Settings

class Index(MethodView):
    def get(self):
        """
        GET method for the main landing page
        :return: renders the index.html page on return
        """
        return render_template('index.html')
