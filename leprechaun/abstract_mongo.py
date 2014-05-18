# -*- coding: utf-8 -*-
import pymongo


class Mongo(object):
    """
    Free abstraction of mongo access.
    Unifies code and helps for tests.
    """

    def __init__(self, name):
        self.name = name
        self.connection = pymongo.Connection()
        self.mongo = self.connection[self.name]

    def _retrieve_collection_by_name(self, collection_name):
        return self.mongo[collection_name]

    def create_index(self, collection_name, string):
        return self._retrieve_collection_by_name(collection_name).create_index(string)

    def insert(self, collection_name, dico):
        return self._retrieve_collection_by_name(collection_name).insert(dico)

    def find(self, collection_name, filtering_criteria=dict()):
        """
        @param filtering_criteria : must be typed as dictionnary
        """
        return self._retrieve_collection_by_name(collection_name).find(filtering_criteria)

    def update(self, collection_name, dico1, dico2, multi=False):
        return self._retrieve_collection_by_name(collection_name).update(dico1, dico2, multi=multi)

    def find_one(self, collection_name, dico=None):
        return self._retrieve_collection_by_name(collection_name).find_one(dico)

    def count(self, collection_name):
        return self._retrieve_collection_by_name(collection_name).count()

    def remove(self, collection_name, dico=None):
        return self._retrieve_collection_by_name(collection_name).remove(dico)

    def exists(self, collection_name, dico):
        result = self._retrieve_collection_by_name(collection_name).find_one(dico)
        return (result != None)

    def create_indexes(self, collection_name, *field_names):
        collection = self._retrieve_collection_by_name(collection_name)
        for field in field_names:
            collection.create_index(field)
        return len(field_names)
