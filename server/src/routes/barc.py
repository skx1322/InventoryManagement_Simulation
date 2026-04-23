from flask import Blueprint, jsonify, request, send_file
from session import token_required
import uuid
from models import Product, Barcode, db
from barcode_utils import generate_barcode

barcode_bp = Blueprint('barcode_bp', __name__)

@barcode_bp.route("/barcode", methods=['POST'])
@token_required
def create_barcode():
    product_id = request.form.get('product_id')
    product = Product.query.filter(Product.product_id == product_id).first()
    if not product:
        return jsonify({
            "success": False,
            "message": f"Not Found: Category {product_id} does not exist",
        }), 404
    
    save_path = generate_barcode(product.product_sku)
    new_barcode = Barcode(
        barcode_id=str(uuid.uuid4()),
        product_sku=product.product_sku,
        barcode_image=save_path.replace("\\", "/")
    )

    db.session.add(new_barcode)
    db.session.commit()
    
    return jsonify({}), 201

@barcode_bp.route("/barcode", methods=['GET'])
@token_required
def read_barcode():

    return jsonify({}), 200

@barcode_bp.route("/barcode", methods=['PUT'])
@token_required
def update_barcode():

    return jsonify({}), 200

@barcode_bp.route("/barcode", methods=['DELETE'])
@token_required
def delete_barcode():

    return jsonify({}), 200

@barcode_bp.route('/static/barcodes/<barcode_id>', methods=['GET'])
def return_image(barcode_id):
    image_path = f'../static/barcodes/{barcode_id}'
    return send_file(image_path, mimetype="image/png")