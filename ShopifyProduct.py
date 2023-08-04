import os
from dotenv import load_dotenv
import shopify
from shopify import Metafield
import json
from PIL import Image
import io


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
            selectedSize, # add a new parameter to accept the selected size
            title='AIGC Phone Case', 
            body_html='AIGC Phone Case', 
            vendor='Artia Fusion', 
            product_type='AIGC Phone Case', 
            tags='AIGC Phone Case', 
            serielsName='AIGC Phone Case', 
            productName='Phone Case', 
            image_data_list=[], 
            seo_title=None, 
            seo_description=None):

        new_product = shopify.Product()
        sizes = [   
                    'iphone-11',
                    'iphone-11-pro-max',
                    'iphone-12-mini',
                    'iphone-12-12-pro',
                    'iphone-12-pro-max',
                    'iphone-13-mini',
                    'iphone-13',
                    'iphone-13-pro',
                    'iphone-13-pro-max',
                    'iphone-14',
                    'iphone-14-plus',
                    'iphone-14-pro',
                    'iphone-14-pro-max'
                ]
        abbreviations = [s.replace(' ', '').replace('iPhone','IP').upper() for s in sizes]

        new_product.title = title
        new_product.body_html = body_html
        new_product.vendor = vendor
        new_product.product_type = product_type
        new_product.tags = tags
        new_product.metafields_global_title_tag = seo_title
        new_product.metafields_global_description_tag = seo_description

        variants = [shopify.Variant({'price': '25.00', 
                                    'compare_at_price': '30.00', 
                                    'option1': size,
                                    'sku': (serielsName + productName+'#'+abbreviations[index]+'#'+str(index+1)).replace(' ','').upper(),
                                    'inventory_management': 'shopify', 
                                    'inventory_policy': 'continue'}) 
                    for index, size in enumerate(sizes)]
        new_product.variants = variants

        images = []
        for imgdata in image_data_list:  
            image = shopify.Image()
            filename = 'some_filename.png' 
            image.attach_image(imgdata, filename=filename)  
            images.append(image)
        new_product.images = images

        success = new_product.save()  

        if success:
            selected_variant_id = None  # to store the id of the selected variant
            for variant in new_product.variants:  # iterate through all the variants
                if variant.option1 == selectedSize:  # find the variant with the selected size
                    selected_variant_id = variant.id
                    break
            if selected_variant_id is not None:
                print(f"Successfully added product {new_product.id}, selected variant id: {selected_variant_id}")
            else:
                print(f"Selected size: {selectedSize} is not a valid size.")
            return selected_variant_id
        else:
            print(f"Failed to add product: {new_product.errors}")
            return None

def image_to_byte_array(image:Image):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format='PNG')  # Change the format to 'PNG'
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

if __name__ == '__main__':
    # Open an image file
    with Image.open('image1.png') as img:  # Change the filename to 'image1.png'
        # Convert image data to byte array
        image_data = image_to_byte_array(img)
        
    ps = ProductSolver()
    ps.create_product(selectedSize='iphone-14-pro', image_data_list=[image_data])  # Call the create_product method with the image data
