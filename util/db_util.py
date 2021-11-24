"""
Handles all database interactions
"""
import logging
import os

from pymongo import MongoClient

LOGGER = logging.getLogger()


class DBUtil:
    """
    Handles all database interactions
    """
    db_host = os.environ.get('DB_HOST', 'localhost')
    db_user = os.environ.get('DB_USER', 'root')
    db_password = os.environ.get('DB_PASSWORD', 'password')
    db_port = 27017
    db_auth_mech = 'SCRAM-SHA-1'

    def __init__(self, db_name='meeting'):
        self.client = MongoClient(
            self.db_host,
            port=self.db_port,
            username=self.db_user,
            password=self.db_password,
            authMechanism=self.db_auth_mech
        )
        self.db_name = db_name
        self.db_client = self.client[db_name]

    def get_db(self):
        """
        Returns a database client
        """
        try:
            LOGGER.info("Fetching %s client", self.db_name)
            response = self.db_client
        except Exception as ex:  # pylint: disable=broad-except
            LOGGER.error(
                "Error occured in fetching"
                " database %s client..Error: %s", self.db_name, ex)
            response = "Failed to fetch database client"
        return response

    def get_collection(self, collection_name):
        """ Returns database collection """
        try:
            LOGGER.debug("Fetching %s collection", collection_name)
            response = self.db_client[collection_name]
        except Exception as ex:  # pylint: disable=broad-except
            LOGGER.error(
                "Error occured in fetching"
                " %s collection.Error: %s", self.db_name, ex)
            response = "Failed to fetch database collection"
        return response
