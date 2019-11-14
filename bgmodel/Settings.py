"""
Abstract data model class that serves as the base class for specific model instantiations
"""
class Settings():
    def select(self, key):
        """
        Gets all entries from the database
        :return: Tuple containing all rows of database
        """
        pass

    def insert(self, key, value):
        """
        Inserts entry into database
        :param name: String
        :param street: String
        :param city: String
        :param state: String
        :param zip: Integer
        :param open_hr: String
        :param close_hr: String
        :param phone: String
        :param drink: String
        :param rating: Integer
        :param website: String
        :return: none
        :raises: Database errors on connection and insertion
        """
        pass

    def delete(self, key):
        """
        Deletes an entry from the database
        :param name: String
        :return: none
        :raises: Database errors on connection and deletion
        """
        pass
