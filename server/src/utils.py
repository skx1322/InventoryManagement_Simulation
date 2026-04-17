import os
import uuid

def generate_sku(brand, cateogry_name, product_name):
    b = str(brand).replace(" ", "")[:3].upper()
    c = str(cateogry_name).replace(" ", "")[:2].upper()
    n = str(product_name).replace(" ", "")[:3].upper()

    suffix = uuid.uuid4().hex[:4].upper()

    return f'{b}-{c}-{n}-{suffix}'
    