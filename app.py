import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from utils.status_codes import StatusCode
import logging
import json

level = logging.getLevelName(os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger('main')
logger.setLevel(level)
ch = logging.StreamHandler()
ch.setLevel(level)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import User, CommercialActivity, Product, Feedback, Visit


@app.route('/')
def home():
    return 'WIMP Backend up!'


# = Users =
@app.route('/users')
def users():
    try:
        all_users = User.query.all()
        return jsonify(all_users)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/user/<int:user_id>', methods=['GET', 'DELETE'])
def get_or_delete_user(user_id: int):
    try:
        if request.method == 'GET':
            fetched_user = User.query.filter(User.user_id == user_id).first()
            return jsonify(fetched_user)
        elif request.method == 'DELETE':
            User.query.filter(User.user_id == user_id).delete()
            db.session.commit()
            return "OK", StatusCode.OK.value
        else:
            return StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/user', methods=['POST'])
def create_or_update_user():
    try:
        if request.method != 'POST':
            return StatusCode.BAD_REQUEST
        else:
            request_user: User = User(**request.get_json())
            if request_user.user_id is None:
                db.session.add(request_user)
            else:
                User.query.filter(User.user_id == request_user.user_id).update(request.get_json())
            db.session.commit()
            return str(request_user.user_id)
    except TypeError as e:
        logger.error(str(e))
        return str(e), StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


# = Products =
@app.route('/products')
def products():
    try:
        all_products = Product.query.all()
        return jsonify(all_products)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/product/<int:product_id>', methods=['GET', 'DELETE'])
def get_or_delete_product(product_id: int):
    try:
        if request.method == 'GET':
            fetched_product = (
                Product.query.filter(
                    Product.product_id == product_id
                ).first()
            )
            return jsonify(fetched_product)
        elif request.method == 'DELETE':
            Product.query.filter(
                Product.product_id == product_id
            ).delete()
            db.session.commit()
            return "OK", StatusCode.OK.value
        else:
            return StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/product', methods=['POST'])
def create_or_update_product():
    try:
        if request.method != 'POST':
            return StatusCode.BAD_REQUEST
        else:
            request_product: Product = Product(**request.get_json())
            if request_product.product_id is None:
                db.session.add(request_product)
            else:
                Product.query.filter(
                    Product.product_id == request_product.product_id
                ).update(request.get_json())
            db.session.commit()
            return str(request_product.product_id)
    except TypeError as e:
        logger.error(str(e))
        return str(e), StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


# = Commercial Activities =
@app.route('/commercial-activities')
def commercial_activities():
    try:
        all_activities = CommercialActivity.query.all()
        return jsonify(all_activities)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/commercial-activity/<int:activity_id>', methods=['GET', 'DELETE'])
def get_or_delete_commercial_activity(activity_id: int):
    try:
        if request.method == 'GET':
            fetched_activities = (
                CommercialActivity.query.filter(
                    CommercialActivity.commercial_activity_id == activity_id
                ).first()
            )
            return jsonify(fetched_activities)
        elif request.method == 'DELETE':
            CommercialActivity.query.filter(
                CommercialActivity.commercial_activity_id == activity_id
            ).delete()
            db.session.commit()
            return "OK", StatusCode.OK.value
        else:
            return StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/commercial-activity', methods=['POST'])
def create_or_update_commercial_activity():
    try:
        if request.method != 'POST':
            return StatusCode.BAD_REQUEST
        else:
            request_activity: CommercialActivity = CommercialActivity(**request.get_json())
            if request_activity.commercial_activity_id is None:
                db.session.add(request_activity)
            else:
                CommercialActivity.query.filter(
                    CommercialActivity.commercial_activity_id == request_activity.commercial_activity_id
                ).update(request.get_json())
            db.session.commit()
            return str(request_activity.commercial_activity_id)
    except TypeError as e:
        logger.error(str(e))
        return str(e), StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/visit/<int:user_id>/<int:activity_id>', methods=['POST'])
def create_visit_for_user(user_id: int, activity_id: int):
    try:
        if request.method != 'POST':
            return StatusCode.BAD_REQUEST.value
        else:
            creating_visit: Visit = Visit(user_id=user_id, commercial_activity_id=activity_id)
            db.session.add(creating_visit)
            db.session.commit()
            return str(creating_visit.visit_id)
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value
