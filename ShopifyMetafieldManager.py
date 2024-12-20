import requests
import json
import os
from dotenv import load_dotenv
import random
import string
import shopify
import base64

load_dotenv()
SHOPIFY_API_KEY = os.getenv("API_KEY")
SHOPIFY_API_SECRET = os.getenv("PASSWORD")
SHOP_NAME = os.getenv("SHOP_NAME")

shop_url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{SHOP_NAME}.myshopify.com/admin/api/2023-07"
shopify.ShopifyResource.set_site(shop_url)

def generate_random_string(length=10):
    """生成一个指定长度的随机字符串"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class ShopifyMetafieldManager:
    def __init__(self, store_name, access_token):
        self.store_name = store_name
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": access_token
        }
        
    def get_metafield_value(self, customer_id, namespace, key):
        url = f"https://{self.store_name}.myshopify.com/admin/api/2023-07/customers/{customer_id}/metafields.json"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            metafields = response.json()["metafields"]
            for metafield in metafields:
                if metafield['key'] == key and metafield['namespace'] == namespace:
                    return metafield
        else:
            return f"Request failed with status code {response.status_code}"
    
    def set_metafield_to_customer(self, customer_id, namespace, key, value):
        try:
            url = f"https://{self.store_name}.myshopify.com/admin/api/2023-07/customers/{customer_id}/metafields.json"

            # Construct the metafield data
            metafield_data = {
                "metafield": {
                    "namespace": namespace,
                    "key": key,
                    "value": value,
                    "type": "single_line_text_field"  # Assume the value type is string, modify this if necessary
                }
            }

            response = requests.post(url, headers=self.headers, json=metafield_data)
            # print(response)
            if response.status_code == 201:
                id = response.json()["metafield"]['owner_id']
                kiss = response.json()["metafield"]['value']
                print(f'write {id} token to shopify metafield successfully! ----> {kiss}')
                return True  # Return the newly created metafield
            else:
                print(f"Request failed with status code {response.status_code}")
                raise Exception
        except Exception as e:
            print(f'{e}')
            raise Exception
    
    def update_metafield_value(self, customer_id, metafield_id, new_value, type):
        url = f"https://{self.store_name}.myshopify.com/admin/api/2023-07/customers/{customer_id}/metafields/{metafield_id}.json"
        data = {
            "metafield": {
                "id": metafield_id,
                "value": new_value,
                "type": type,
            }
        }
        response = requests.put(url, headers=self.headers, data=json.dumps(data))
        if response.status_code == 200:
            return "Metafield updated successfully"
        else:
            return f"Request failed with status code {response.status_code}"

    def update_kiss(self, customer_id, newToken):
        namespace = 'custom'
        key = 'kiss'
        try:
            self.set_metafield_to_customer(customer_id,namespace,key,newToken)
            return True
        except Exception as e:
            print(f'{e}')
            return False


    def get_orders(self, customer_id):
        url = f"https://{self.store_name}.myshopify.com/admin/api/2023-07/customers/7061354938648/orders.json?status=any"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return f"Request failed with status code {response.status_code}"

if __name__ == '__main__':
    metaManager = ShopifyMetafieldManager("artiafusion", SHOPIFY_API_SECRET)
    # result = metaManager.fill_random_number_to_kiss('7061354938648')
    # print(result)
    # 格式化 json result
    #debug this
    # metaManager.get_metafield_value('7086791196952','custom','kiss')
    metaManager.set_metafield_to_customer('7086791196952','custom','kiss','test123')
    

    # result = metaManager.get_orders(7061354938648)
    #['orders'][0]['fulfillments']['line_items']['name']
    
    #整理orders里fulfillments所有订单下的所有line_items的name（包含AI Design Credits）的各种类数量
    # for i in range(len(result['orders'])):
    #     for j in range(len(result['orders'][i]['fulfillments'])):
    #         for k in range(len(result['orders'][i]['fulfillments'][j]['line_items'])):
    #             if result
    #'list' object has no attribute 'items'
    # creditsProductList = [
    #     'AI Design Credits - Basic Pack (1 Use)',
    #     'AI Design Credits - Value Pack (5 Uses)',
    #     'AI Design Credits - Premium Pack (10 Uses)'
    # ]
    # for i, order in enumerate(result['orders']):
    #     customer_id = order['customer']['id']
    #     print(customer_id)
    #     for j, fulfillment in enumerate(order['fulfillments']):
    #         for k, line_item in enumerate(fulfillment['line_items']):
    #             print(f"Order index: {i}, Fulfillment index: {j}, Line item index: {k}")
    #             print(line_item['id'])
    #             print(line_item['name'])
    #             print(line_item['quantity'])

    
    # result = json.dumps(result, indent=4)

    # print(result)
    

# curl -X GET "https://artiafusion.myshopify.com/admin/api/2023-07/customers/7061354938648/orders.json?status=any" \
# -H "X-Shopify-Access-Token: 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"



        # metafield = self.get_metafield_value(customer_id, namespace, key)
        # if metafield:
        #     metafield_id = metafield['id']
        #     response = self.update_metafield_value(customer_id, metafield_id, newToken, "single_line_text_field")
        #     if response == "Metafield updated successfully":
        #         return True
        #     else:
        #         return False
        # else:
        #     return False
