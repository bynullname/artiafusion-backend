import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# JWT密钥
JWT_SECRET = os.getenv("JWT_SECRET")  # JWT密钥

# JWT过期时间设置为10年
JWT_EXPIRY = timedelta(days=365 * 10)  

# customer_id for the token
customer_id = "3782739991"  # replace with your customer id

# 生成JWT Token
token = jwt.encode({'customer_id': customer_id, 'exp': datetime.utcnow() + JWT_EXPIRY}, JWT_SECRET, algorithm='HS256')

print(token)
