import barcode
import os
from barcode.writer import ImageWriter

BARCODE_DIR = 'static/barcodes'

def generate_barcode(prod_sku):
    try:
        CODING = barcode.get_barcode_class('code128')
        
        my_code = CODING(prod_sku, writer=ImageWriter())
        
        filename = f"barcode_{prod_sku}"
        full_path = os.path.join(BARCODE_DIR, filename)
        
        my_code.save(full_path)
        
        return f"{BARCODE_DIR}/{filename}.png"
    
    except Exception as e:
        print(f"Barcode Error: {e}")
        return None

# path = generate_barcode('HI3-PL-FUH-AE3E')
# print(f"Saved to: {path}")