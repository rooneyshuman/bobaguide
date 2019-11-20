from .model_datastore import model
from .settings_datastore import settings


appmodel = model()
appsettings = settings()


def get_model():
    return appmodel

def get_settings():
    return appsettings
