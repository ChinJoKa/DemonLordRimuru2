import pymongo
from db import dbclass

class roldb():
    def __init__(self):
        self.dbclass = dbclass("Rol", "Roller")
        self.db = self.dbclass.collection
    
    def ekle(self, post):
        self.db.insert_one(post)
    
    def bul(self, name:str = None, roleID:int = None):
        if name:
            rol = self.db.find_one({"name":name})
        elif id:
            rol = self.db.find_one({"rolID":roleID})
        return rol

    def sil(self, post):
        self.db.delete_one(post)
    
    def edit(self, post):
        ...
    
    def getAll(self):
        cursor = self.db.find({})
        data = []
        for d in cursor:
            data.append(d)
        data.sort(key=lambda x: x['name'].lower())
        return data