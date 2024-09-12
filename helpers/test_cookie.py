from flask import Flask, request, make_response, jsonify
import json

app = Flask(__name__)

@app.route('/set_cookie', methods=['POST'])
def update_data_into_cookie():
    data = {"sample_key": "sample_value"}  # Example data
    data_str = json.dumps(data)
    
    # Create response with a JSON message
    resp = make_response(jsonify({"message": "Login successful"}))
    
    # Set the cookie
    resp.set_cookie('token', data_str, httponly=True, samesite='Strict', secure=True)
    print("Cookie has been updated.")
    print(request.cookies.get('token'))
    
    return resp

@app.route('/get_cookie', methods=['GET'])
def get_cookie():
    # Attempt to retrieve the 'token' cookie
    token_cookie = request.cookies.get('token')
    if token_cookie:
        print(f"Cookie value: {token_cookie}")
        return jsonify({"cookie_value": token_cookie})
    else:
        return jsonify({"message": "No cookie found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
