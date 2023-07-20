from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

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
from functools import wraps
from flask import make_response
from CaseGenerator import CaseGenerator
from models import db, Mj


load_dotenv()
SHOPIFY_API_KEY = os.getenv("API_KEY")
SHOPIFY_API_SECRET = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")  # JWT密钥
TNL_API_KEY = os.getenv("TNL_API_KEY")
db_name = os.getenv("db_name")
db_psw = os.getenv("db_psw")
PORT = os.getenv("PORT")


JWT_EXPIRY = timedelta(minutes=60)  # JWT过期时间设置为1小时

tnl = TNL(TNL_API_KEY)
cg =CaseGenerator()
shop_url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{SHOP_NAME}.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)

metaManager = ShopifyMetafieldManager("artiafusion", SHOPIFY_API_SECRET)


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{db_psw}@localhost:5432/{db_name}'

db.init_app(app)
migrate = Migrate(app, db)

CORS(app)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('token')
        if not auth_header:
            return jsonify({'message': 'No token header provided'}), 401

        try:
            payload = jwt.decode(auth_header, JWT_SECRET, algorithms='HS256')
            jwt_customer_id = payload['customer_id']
            print(payload)
            # 获取请求数据
            data = request.get_json()
            if not data:
                return jsonify({'message': 'No input data provided'}), 400
            
            request_customer_id = data.get('customer_id')
            print(request_customer_id)
            # 检查请求体中的 customer_id 是否与 token 中的一致
            if request_customer_id != jwt_customer_id:
                return jsonify({'message': 'Customer id does not match'}), 401
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Signature expired. Please log in again.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token. Please log in again.'}), 401
        except Exception as e:
            return jsonify({'message': f'Jwt : {e}'}), 401
        return f(*args, **kwargs)
    return decorated



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
        return jsonify({'message': 'Verification requested'}), 200
    except Exception as e:
        print(e)
        return jsonify({'message': f'{e}'}), 400


@app.route('/api/mj/imagine/', methods=['POST'])
# @token_required
def imagine():
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        customer_id = data.get('customer_id')

        if not prompt or not customer_id:
            return jsonify({'message': 'prompt or customer_id missing'}), 400

        print(customer_id,prompt)
        response = tnl.imagine(prompt)
        if response['success'] != True:
            return jsonify({'message': 'imagine is running failed, please contact admin'}), 400

        messageId = response['messageId']

        # Insert data into the database
        mj = Mj(customer_id=customer_id, prompt=prompt, messageId=messageId)
        db.session.add(mj)
        db.session.commit()

        return jsonify({'message': 'Success', 'messageId': messageId}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/api/mj/query/', methods=['POST'])
def queryMj():
    try:
        data = request.get_json()
        messageId = data.get('messageId')
        if not messageId:
            return jsonify({'message': 'messageId missing'}), 400

        mj = Mj.query.filter_by(messageId=messageId).first()
        if mj:
            if mj.imageUrls:
                return jsonify({'message': 'Success', 'imageUrls': mj.imageUrls}), 200
            else:
                return jsonify({'message': 'Work in progres,pls wait moment.'}), 200
        else:
            return jsonify({'message': 'Not found'}), 404
    except Exception as e:
        print(e)
        return jsonify({'message': str(e)}), 400


@app.route('/webhook/mj', methods=['POST'])
def MjWebhook():
    try:
        data = request.get_json()
        print(data)

        originatingMessageId = data.get('originatingMessageId')
        if originatingMessageId:
            mj = Mj.query.filter_by(messageId=originatingMessageId).first()
            if mj:
                # Update relevant fields based on data
                mj.content = data.get('content')
                mj.imageUrl = data.get('imageUrl')
                mj.imageUrls = data.get('imageUrls')
                mj.type = data.get('type')
                mj.createdAt = data.get('createdAt')
                mj.responseAt = data.get('responseAt')

                db.session.commit()

        return jsonify(data), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400



if __name__ == '__main__':
    # 设置SSL上下文
    context = ('fullchain.pem', 'privkey.pem')
    # 运行Flask应用程序，启用HTTPS
    app.run(host='0.0.0.0', port=PORT, ssl_context=context, debug=True)


