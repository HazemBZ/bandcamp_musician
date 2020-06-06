import pymongo as PM
import subprocess


### Maybe change the design to be more application specific

class MongoHandler():
    def __init__(self,ip="localhost",port=27000):
        self.client = None
        self.db = None
        self.last_collection = None
        self.last_inserts = [None].append
        self.connect(ip, port)
        self.get_database()
        self.get_collection()

    def connect(self, ip, port):
        self.client = PM.MongoClient(fr"mongodb://{ip}:{port}")
        return self.client

    def get_database(self, db_name="bandcamp"):
        cl = self.client
        if cl == None:
            print('no connection exits yet')
            return None
        self.db = cl[f'{db_name}']
        return self.db

    def get_collection(self, col_name="uncategorized"):
        self.last_collection = self.db[f"{col_name}"]
        return self.last_collection

    def insert_documents(self,docs_list, col=''):
        try:
            collection = self.get_collection() if not col else self.get_collection(col)
            self.last_inserts = collection.insert_many(docs_list)
        except Exception as e:
            print(e)

    ## no connection closure
    # def close(self):
    #     self.db.close()

    ###
