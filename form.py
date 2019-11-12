from flask import redirect, request, url_for, render_template
from flask.views import MethodView
import gbmodel

class Form(MethodView):
    def get(self):
        """
        GET method for the form page
        :return: renders the form.html page on return
        """
        return render_template('form.html')

    def post(self):
        """
        Accepts POST requests, and processes the form;
        Redirect to index when completed.
        """
        model = gbmodel.get_model()
        website = request.form['website']
        if not ("http" in website):
            website = "http://" + website
        model.insert(request.form['name'], request.form['street'], request.form['city'], request.form['state'],
                     request.form['zip'], request.form['open_hr'], request.form['close_hr'], request.form['phone'],
                     request.form['drink'], request.form['rating'], website)
        return redirect(url_for('shops'))
