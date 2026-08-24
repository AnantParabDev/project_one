from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from dao.category_dao import CategoryDAO
from service.category_service import CategoryService

category_service = CategoryService(CategoryDAO())

category_bp = Blueprint("category", __name__)

@category_bp.route('/api/categories', methods=['POST', 'GET'])
@jwt_required()
def add_categories():
  if request.method == 'GET':
    categories = category_service.get_all_category()
    category_list = [c.to_dict() for c in categories]
    return jsonify(category_list), 200
  else:
    claim = get_jwt()
    if claim.get('role') != 'ADMIN':
      return jsonify({"message": "Only Admins can create categories"}), 403

    data = request.get_json()
    category_name = data.get("category_name")

    category = category_service.add_category(category_name)

    return jsonify( 
        {
            "message": "Category Created Successfully",
            "category": category.to_dict()
        }
    ), 201
