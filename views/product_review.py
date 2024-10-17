from flask import Blueprint, request
from controllers import review_controller


review  = Blueprint('review', __name__)



@review.route('/add_review',methods=['POST'])

def add_review():
    
    review_message = request.json.get('review')
    product_id = request.json.get('product_id')
    rating = request.json.get('rating')


    return review_controller.add_review(review_message,product_id,rating)

@review.route('/add_reply_message',methods =['POST'])
def add_reply_message():
    reply_message = request.json.get('message')
    product_id = request.json.get('product_id')
    repling_person= request.json.get('repling_person')
    return review_controller.add_reply_message(product_id, reply_message, repling_person)



@review.route('/update_review', methods=['PUT'])
def update_review():
    product_id = request.json.get('product_id')
    updated_message = request.json.get('updated_review')
    print(updated_message)
    return review_controller.update_review(product_id, updated_message)


@review.route('/update_reply_review', methods=['PUT'])
def update_reply_review():
    product_id = request.json.get('product_id')
    target_email= request.json.get('target_email')
    updated_message = request.json.get('updated_review')
    print(updated_message)
    return review_controller.update_reply_review(product_id,target_email, updated_message)



@review.route('/view_all_review_user', methods=['GET'])
def view_all_review_user():
    user_email = request.args.get("email")
    return review_controller.view_all_review_user(user_email)


@review.route('/view_all_review_product', methods=['GET'])
def view_all_review_product():
    product_id = request.args.get('product_id')
    return  review_controller.view_all_review_product(product_id)


@review.route('/view_specific_review', methods=['GET'])
def view_specific_review():
    review_id=request.args.get('review_id')
    return review_controller.view_specific_review(review_id)


@review.route('/edit_review', methods=['PUT'])
def edit_review():
    review_id = request.args.get('review_id')
    return review_controller.edit_review(review_id)


@review.route('/delete_specific_review', methods=['DELETE'])
def delete_specific_review():
    review_id = request.args.get('review_id')
    email = request.args.get('email')
    return review_controller.delete_specific_review(review_id,email)



@review.route('/delete_all_review_user', methods=['DELETE'])
def delete_all_review_user():
    user_email = request.args.get('user_email')
    
    return review_controller.delete_all_review_user(user_email)



@review.route('/delete_all_review_product', methods=['DELETE'])
def delete_all_review_product():
    product_id = request.args.get('product_id')
    return review_controller.delete_all_review_product(product_id)


@review.route('/like_an_review', methods=['POST'])
def like_an_review():
    review_id = request.args.get('review_id')
    return review_controller.like_an_review(review_id)



@review.route('/like_an_nested_review', methods=['POST'])
def like_an_nested_review():
    replied_email = request.json.get('replied_email')
    review_id = request.json.get('review_id')

    return review_controller.like_an_nested_review(review_id,replied_email)

