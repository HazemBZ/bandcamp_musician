import pymongo as PM


### Maybe change the design to be more application specific

class MongoHandler():
    def __init__(self):
        self.client = None
        self.db = None
        self.last_collection = None
        self.last_inserts = [None].append
        self.connect()
        self.get_database()
        self.get_collection()

    def connect(self, host="localhost", port=27017):
        self.client = PM.MongoClient(fr"mongodb://{host}:{port}")
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
        collection = self.get_collection() if not col else self.get_collection(col)
        self.last_inserts = collection.insert_many(docs_list)

    ## no connection closure    
    # def close(self):
    #     self.db.close()

    ###