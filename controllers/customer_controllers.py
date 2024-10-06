
from flask import session , request 
from models import db_creation

def customer_support():


    find_email_existance = db_creation.customer_support_collection.find_one({"email":session['email']})
    if find_email_existance :
        new_data= {"email":session['email'], }