from google.appengine.ext import ndb


class Settings(ndb.Model):
    key = nbd.StringProperty()
    value = ndb.StringProperty()

    def get(key):
        """
        Given a key, retrieves the secret configuration variable from Datastore
        :return: Value associated with the configuration variable key 
        :raises: Exception if value is not found in the database for a given key
        """
        VALUE_NOT_SET = "NOT SET"
        result = Settings.query(Settings.key == key).get()
        if not value:
            result = Settings()
            result.value = VALUE_NOT_SET
            result.put()
        if result.value == VALUE_NOT_SET:
            raise Exception("The given key %s was not found in the database.", key)
        return result.value
