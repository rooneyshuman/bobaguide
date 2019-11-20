from .model_datastore import model
from .settings_datastore import settings


appmodel = model()	appmodel = model()
appsettings = settings()


def get_model():	def get_model():
    return appmodel 	    return appmodel

def get_settings():
    return appsettings
