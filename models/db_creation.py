import pymongo 

connection = pymongo.MongoClient("mongodb://localhost:27017")


db = connection["auth_using_flask"]

new_user_collection = db["newly_registered_user"]

product_collection = db ['product_details']
