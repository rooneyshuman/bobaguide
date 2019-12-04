"""
A Flask application for viewing and submitting bubble tea store locations
"""
import flask
from flask.views import MethodView
from index import Index
from form import Form
from shops import Shops
from reviews import Reviews
from translation import Translation

app = flask.Flask(__name__)  # our Flask app

"""
Route for main landing page. Accepts GET method
"""
app.add_url_rule("/", view_func=Index.as_view("index"), methods=["GET"])

"""
Route for form page. Accepts GET and POST methods
"""
app.add_url_rule("/form/", view_func=Form.as_view("form"), methods=["GET", "POST"])

"""
Route for shops (display) page. Accepts GET and POST methods
"""
app.add_url_rule("/shops/", view_func=Shops.as_view("shops"), methods=["GET", "POST"])

"""
Route for reviews (display) page. Accepts GET and POST methods
"""
app.add_url_rule(
    "/reviews/<shop_name>/<shop_phone>",
    view_func=Reviews.as_view("reviews"),
    methods=["GET", "POST"],
)

"""
Route for translation (display) page. Accepts GET methods
"""
app.add_url_rule(
    "/translation/<shop_name>/<text>/<target>",
    view_func=Translation.as_view("translation"),
    methods=["GET"],
)

"""
Application access point. Specifies host and port to run on
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
