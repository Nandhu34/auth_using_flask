import pymongo 

connection = pymongo.MongoClient("mongodb://localhost:27017")


db = connection["auth_using_flask"]

new_user_collection = db["newly_registered_user"]

product_collection = db ['product_details']

wishlist_collection = db['wishlist']

cart_collection = db['cart']

secondary_cart_collection = db['secondary_cart']

confirm_order_collection = db['confirm_order_collection']

customer_support_collection = db['customer_support']

product_review_collection = db['review_collection']
