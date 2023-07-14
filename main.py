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
from functools import wraps
from flask import make_response
from CaseGenerator import CaseGenerator
load_dotenv()
SHOPIFY_API_KEY = os.getenv("API_KEY")
SHOPIFY_API_SECRET = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")
JWT_SECRET = os.getenv("JWT_SECRET")  # JWT密钥
TNL_API_KEY = os.getenv("TNL_API_KEY")

JWT_EXPIRY = timedelta(minutes=60)  # JWT过期时间设置为1小时

tnl = TNL(TNL_API_KEY)
cg =CaseGenerator()
shop_url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{SHOP_NAME}.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)
app = Flask(__name__)
metaManager = ShopifyMetafieldManager("artiafusion", SHOPIFY_API_SECRET)
CORS(app)



def token_required(f):
    """
    token_required 是一个装饰器函数，它用于验证 JWT token 的有效性和过期情况。
    
    这个装饰器首先从请求的 headers 中获取 JWT token。如果没有找到 JWT token，它会返回一个错误消息。
    如果找到了 JWT token，装饰器将尝试解析 JWT token。如果 JWT token 已经过期或无效，装饰器会返回相应的错误消息。
    
    然后，装饰器将从请求体中获取 'customer_id'。如果找不到 'customer_id'，它会返回一个错误消息。
    如果找到了 'customer_id'，装饰器将检查它是否与 JWT token 中的 'customer_id' 一致。如果不一致，它会返回一个错误消息。
    
    如果所有的检查都通过，装饰器将调用原始的路由函数，并将所有的参数传递给它。
    
    你可以将这个装饰器应用到任何需要 JWT token 验证的 Flask 路由上。
    """
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

        return f(*args, **kwargs)
    return decorated



@app.route('/api/requestVerification', methods=['POST'])
def request_verification():
    """
    该接口用于请求验证。当客户提交请求时，将生成一个 JWT token，其中包含客户 ID 和 token 的过期时间。
    该 token 然后将与客户 ID 关联，并存储在 Shopify Metafield 中。
    """
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
@token_required
def imagine():
    """
    该接口用于处理 "Imagine" 请求。首先，它会验证 JWT token 的有效性和过期情况。
    然后，如果 JWT token 有效且未过期，该接口将从请求体中提取 'prompt' 和 'customer_id'，并将 'prompt' 提交给 TNL API。
    如果 TNL API 响应表示操作成功，则返回成功消息。否则，返回错误消息。
    """
    try:
        data = request.get_json()
        prompt = data.get('prompt')
        customer_id = data.get('customer_id')

        if not prompt or not customer_id:
            return jsonify({'message': 'prompt or customer_id missing'}), 400

        response = tnl.imagine(prompt)
        if response['success'] != True:
            return jsonify({'message': 'imagine is running failed, pls contact admin'}), 400

        messageId = response['messageId']
        return jsonify({'message': 'Success','messageId':messageId}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/webhook/mj', methods=['POST'])
def MjWebhook():
    """
    该接口用于处理来自 MJ Webhook 的 POST 请求。在接收到请求后，它将打印并返回请求的 JSON 数据。
    """
    try:
        data = request.get_json()
        print(data)
        # cg.do(data.get('imageUrls')[0])
        # data demo
        # {
        #   'content': 'high texture quality portrait of a young woman with freckles and crystal blue eyes with wreath in her hair, 4k', 
        #   'imageUrl': 'https://cdn.discordapp.com/attachments/1128685518339710976/1129075874763903098/AjKaBaL_high_texture_quality_portrait_of_a_young_woman_with_fre_3d049b25-3b7a-4ad1-a50c-88b23fc51f27.png', 
        #   'imageUrls': ['https://cdn.midjourney.com/3d049b25-3b7a-4ad1-a50c-88b23fc51f27/0_0.png', 
        #   'https://cdn.midjourney.com/3d049b25-3b7a-4ad1-a50c-88b23fc51f27/0_1.png',
        #   'https://cdn.midjourney.com/3d049b25-3b7a-4ad1-a50c-88b23fc51f27/0_2.png', 
        #   'https://cdn.midjourney.com/3d049b25-3b7a-4ad1-a50c-88b23fc51f27/0_3.png'], 
        #   'buttons': ['U1', 'U2', 'U3', 'U4', '🔄', 'V1', 'V2', 'V3', 'V4'], 
        #   'createdAt': '2023-07-13T15:44:25.909Z', 
        #   'responseAt': '2023-07-13T15:44:26.741Z', 
        #   'ref': '', 
        #   'description': '', 
        #   'type': 'imagine', 
        #   'originatingMessageId': 
        #   '1pckDYipUHe4wPvQZbnp', 
        #   'buttonMessageId': 'PgPGNfV1NGvXkCkKhWtO'
        # }
        # 107.178.200.219 - - [13/Jul/2023 23:44:27] "POST /webhook/mj HTTP/1.1" 200 -

        return 'hello'
    except Exception as e:
        print(e)
        return jsonify({'message': f'{e}'}), 400






if __name__ == '__main__':
    # 设置SSL上下文
    context = ('fullchain.pem', 'privkey.pem')
    # 运行Flask应用程序，启用HTTPS
    app.run(host='0.0.0.0', port=6090, ssl_context=context, debug=True)


