# from faker import Faker

# fake = Faker()

# def mock_payment():
#     return {
#         'payment_id': fake.uuid4(),
#         'amount': fake.random_number(digits=5),
#         'currency': 'hjbvdsbdbh',
#         'status': fake.random_element(elements=('created', 'completed', 'failed')),
#         'transaction_date': fake.date_time_this_year()
#     }

# # Generate mock payment data
# payment = mock_payment()
# print(payment)

# import stripe
# stripe.api_key = ""

# payment_intent = stripe.PaymentIntent.create(
#   amount=500,
#   currency="gbp",
#   payment_method="pm_card_visa",
# )

# print(payment_intent)

import pymongo

connection = pymongo.MongoClient("mongodb://localhost:27017")


db = connection["auth_using_flask"]

customer_support_collection = db['customer_support']


email = "nandhakumar2000@gmail.com"


# email = "nandhakumarselva2000@gmail.com"

'''
# add 
check_user_existance = customer_support_collection.find_one({"email":email})
# print(check_user_existance)
if  check_user_existance == None :
    new_data = {"email":email, "support_request":[{"support_id":"1234", "category":"order","date_of_generation":"01-10-2024","message":"why my order is not placed?", "status":"support_submitted"}]}
    ins = customer_support_collection.insert_one(new_data)
    if ins.inserted_id:
        print("support request has been send to the admin")
else:
    updation_data = customer_support_collection.update_one({"email":email},{"$push":{"support_request":{"support_id":"000", "category":"order","date_of_generation":"01-10-2024","message":"why my order is not placed?", "status":"support_submitted"}}})
    if updation_data.matched_count ==1 :
        print("data has been updated in old document")
'''

'''
# view 
check_user_existance = customer_support_collection.find_one({"email":email})
if check_user_existance==None :
    print("this user has not send any support request")
else :
    print(check_user_existance['support_request'])
'''

# # update_response_status and message 
'''

search_qwery={"email":email,"support_request.support_id":"00"}
update_qwery = {"$set":{"support_request.$.status":"admin_received","support_request.$.admin_message":"enquiring about issue"}}
print(search_qwery,update_qwery)
upd_cus_support = customer_support_collection.update_one(search_qwery ,update_qwery)
print(email)
if upd_cus_support.modified_count ==1:
    print("status has been updated")
else :
    print("status not updated")
'''

'''
# update the message that user send 

new_message="new_message"
support_id="00"


search_qwery={"email":email,"support_request.support_id":support_id}
update_qwery = {"$set":{"support_request.$.message":new_message}}

upd_cus_support = customer_support_collection.update_one(search_qwery ,update_qwery)
print(email)
if upd_cus_support.modified_count ==1:
    print("status has been updated")
else :
    print("status not updated")
'''

'''
# delete_specific_message 
search_qwery = {"email":email}

del_doc = customer_support_collection.update_one({"email":email,"support_request.support_id":"00"},{"$pull":{"support_request":{"support_id":"00"}}})
if del_doc.modified_count==1:
    print("qwery has been deleted")
else:
    print("please try again later")
'''

#delete complete_ reply

del_doc = customer_support_collection.delete_one({"email":email})
if del_doc.deleted_count ==1:
  print("all reviews deleted")
else:
  print("please try again later")
  