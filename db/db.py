from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
MONGO_URI = os.getenv("MONGO_URI")

class dbclass():
    def __init__(self, db, collection):
        self.cluster = MongoClient(MONGO_URI)
        self.db = self.cluster[db]
        self.collection = self.db[collection]
        self.points:dict = {}
    
    def add(self, post):
        print(post)
        self.collection.insert_one(post)

    def exist(self, id):
        try:
            value = self.collection.find({"$and":[{"_id":{"$exists": True}}, {"_id":{"$eq": id}}]})[0]
            return value
        except:
            self.create_new(id)
            return None
    
    def hour_reset(self):
        self.collection.update_many({}, {"$set":{"msg": 0, "voice": 0}})
    
    def post(self, post):
        self.collection.insert_one(post)

    def existpost(self, seri):
        try:
            value = self.collection.find({"$and":[{"Seri Adı":{"$exists": True}}, {"Seri Adı":{"$eq": seri}}]})[0]
            return value
        except:
            return None
    
    def exist_title(self, title):
        try:
            self.collection.find({"$and":[{"title":{"$exists": True}}, {"title":{"$eq": title}}]})[0]
            return True
        except:
            return False

    def update(self, multipost):
        for post in multipost:
            if self.existpost(post['Seri Adı']):
                self.collection.update_one({"Seri Adı": post['Seri Adı']}, {"$set":post})
            else:
                self.collection.insert_one(post)
        pass

    def chapterupdate(self, multipost):
        try:
            for post in multipost:
                self.collection.update_one({"title": post['title']}, {"$set":post})
            return True
        except:
            return False

    def ekipupdate(self, postlist):
        for rumuz in postlist:
            try:
                r = self.collection.find({"rumuz":rumuz['rumuz']})[0]
            except:
                rumuz['aktif'] = True
                self.collection.insert_one(rumuz)

    def data(self):
        data = self.collection.find({})
        try:
            if data[0]['aktif']:
                pass
            output = []
            for d in data:
                if d['aktif'] == True:
                    output.append(d)
            return output
        except:
            return data

    def chapters_seri(self, seri):
        try:
            value = self.collection.find({"seri":seri})
            return value
        except:
            return None
    
    def cuzdan(self, rumuz):
        try:
            return self.collection.find({"$and":[{"rumuz":{"$exists": True}}, {"rumuz":{"$eq": rumuz}}]})[0]
        except:
            return False

    def ekip_puan_update(self, post):
        try:
            self.collection.update_one({"rumuz": post['rumuz']}, {"$set": post})
            return "işlem tamam"
        except:
            print("update error")
            return "update error"
    
    def ekip_aktif(self, rumuz, aktif):
        try:
            self.collection.find_one_and_update({"rumuz": rumuz}, {"$set": {"aktif": aktif}})
            return "işlem tamam"
        except:
            print("update error")
            return "update error"