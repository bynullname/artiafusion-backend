import os
from dotenv import load_dotenv
import shopify
from shopify import Metafield
import json

class ProductSolver:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        SHOPIFY_API_KEY = os.getenv("API_KEY")
        SHOPIFY_API_SECRET = os.getenv("PASSWORD")
        SHOP_NAME = os.getenv("SHOP_NAME")

        shop_url = f"https://{SHOPIFY_API_KEY}:{SHOPIFY_API_SECRET}@{SHOP_NAME}.myshopify.com/admin/api/2023-07"
        shopify.ShopifyResource.set_site(shop_url)

    def create_product(self, 
        title='AIGC Phone Case', 
        body_html='AIGC Phone Case', 
        vendor='Artia Fusion', 
        product_type='AIGC Phone Case', 
        tags='AIGC Phone Case', 
        serielsName='AIGC Phone Case', 
        productName='Phone Case', 
        image_data_list=[],  # modify this parameter to accept a list of image data
        seo_title=None, 
        seo_description=None):
        
        new_product = shopify.Product()
        sizes = ["iPhone 14 Pro", 
                "iPhone 14 Pro Max", 
                "iPhone 14 Pro Plus", 
                "iPhone 14",
                "iPhone 13 Pro Max", 
                "iPhone 13 Pro", 
                "iPhone 13 min", 
                "iPhone 13"]
        abbreviations = [s.replace(' ', '').replace('iPhone','IP').upper() for s in sizes]
        
        new_product.title = title
        new_product.body_html = body_html
        new_product.vendor = vendor
        new_product.product_type = product_type
        new_product.tags = tags
        # new_product.seo_title = seo_title  # set SEO title
        # new_product.seo_description = seo_description  # set SEO description
        new_product.metafields_global_title_tag = seo_title
        new_product.metafields_global_description_tag = seo_description

        variants = [shopify.Variant({'price': '20.00', 
                                    'compare_at_price': '25.00', 
                                    'option1': size,
                                    'sku': (serielsName + productName+'#'+abbreviations[index]+'#'+str(index+1)).replace(' ','').upper(),
                                    'inventory_management': 'shopify', 
                                    'inventory_policy': 'continue'}) 
                    for index, size in enumerate(sizes)]
        new_product.variants = variants

        images = []
        for imgdata in image_data_list:  # modify this line to iterate through the image data list
            image = shopify.Image()
            filename = 'some_filename.png'  # you might want to generate or pass filename for each image data
            image.attach_image(imgdata, filename=filename)  # directly use image data to attach image
            images.append(image)
        new_product.images = images


        success = new_product.save()  # returns True if the product was saved successfully, the product data gets updated if it was saved

        if success:
            print(f"Successfully added product {new_product.id} {new_product.variants[0].id}")
            return new_product.variants[0].id
        else:
            print(f"Failed to add product: {new_product.errors}")
            return None

if __name__ == '__main__':
    ps = ProductSolver()
    # product = ps.create_product(paths=['0_2.png'])
    # print(product)
