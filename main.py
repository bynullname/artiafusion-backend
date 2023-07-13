from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import shopify
from shopify.resources import Metafield
import string
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
from ShopifyMetafieldManager import ShopifyMetafieldManager
from midjourney_api import TNL



# help(jwt)
load_dotenv()
SHOPIFY_API_KEY = os.getenv("API_KEY")
SHOPIFY_API_SECRET = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")  # JWT密钥
TNL_API_KEY = os.getenv("TNL_API_KEY")

JWT_EXPIRY = timedelta(minutes=60)  # JWT过期时间设置为1小时

tnl = TNL(TNL_API_KEY)

shop_url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{SHOP_NAME}.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)
app = Flask(__name__)
metaManager = ShopifyMetafieldManager("artiafusion", SHOPIFY_API_SECRET)
CORS(app)

@app.route('/api/requestVerification', methods=['POST'])
def request_verification():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        if not customer_id:
            return jsonify({'message': 'customer_id is required'}), 400
        customer = shopify.Customer.find(customer_id)
        if not customer:
            return jsonify({'message': 'customer_id is invalid'}), 400
        
        # 生成JWT Token
        token = jwt.encode({'customer_id': customer_id, 'exp': datetime.utcnow() + JWT_EXPIRY}, JWT_SECRET, algorithm='HS256')

        metaManager.update_kiss(customer_id,token)
        print(token)
        return jsonify({'message': 'Verification requested'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': f'{e}'}), 400


@app.route('/api/processData', methods=['POST'])
def process_data():
    try:
        data = request.get_json()
        customer_id = data.get('customer_id')
        token = data.get('token')

        if not all([customer_id, token]):
            return jsonify({'message': 'customer_id and token are required'}), 400

        # 验证JWT Token的有效性
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            if payload['customer_id'] == customer_id:
                # 检查token是否过期
                now = datetime.utcnow()
                expiration_time = datetime.fromtimestamp(payload['exp'])
                if expiration_time > now:
                    return jsonify({'message': 'Data processed successfully'}), 200
                else:
                    return jsonify({'message': 'Token has expired'}), 400
            else:
                return jsonify({'message': 'Identity not verified'}), 400
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 400
    except Exception as e:
        print(e)
        return jsonify({'message': f'{e}'}), 400

#读取请求的header
@app.route('/api/mj/image/', methods=['POST'])
def image():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'No input data provided'}), 400

        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'No Authorization header provided'}), 401

        prompt = data.get('prompt')
        customer_id = data.get('customer_id')
        if not prompt or not customer_id:
            return jsonify({'message': 'prompt or customer_id missing'}), 400

        print(auth_header,prompt,customer_id)
        response = tnl.imagine(prompt)
        if response['success'] != True:
            return jsonify({'message': 'imagine is runing failed,pls contact admin'},400)

        messageId = response['messageId']
        print(messageId)
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/webhook/mj', methods=['POST'])
def MjWebhook():
    try:
        data = request.get_json()
        print(data)
        return 'hello1'
    except Exception as e:
        print(e)
        return jsonify({'message': f'{e}'}), 400



if __name__ == '__main__':
    # 设置SSL上下文
    context = ('fullchain.pem', 'privkey.pem')
    # 运行Flask应用程序，启用HTTPS
    app.run(host='0.0.0.0', port=6090, ssl_context=context, debug=True)


