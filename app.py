import datetime
import logging
import os
from typing import Optional, List

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from geopy.distance import distance

from utils.enums import Availability
from utils.math import compute_square_exponential_mean
from utils.status_codes import StatusCode

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

from models import User, CommercialActivity, Product, Feedback, FeedbackType, Visit, Offer


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
            fetched_activity: CommercialActivity = (
                CommercialActivity.query.filter(
                    CommercialActivity.commercial_activity_id == activity_id
                ).first()
            )
            return jsonify(fetched_activity)
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


@app.route('/commercial-activity-products/<int:activity_id>', methods=['GET'])
def get_product_for_activity(activity_id: int):
    try:
        if request.method == 'GET':
            fetched_activity: CommercialActivity = (
                CommercialActivity.query.filter(
                    CommercialActivity.commercial_activity_id == activity_id
                ).first()
            )
            for product in fetched_activity.products:
                offer = Offer.query.filter(
                    Offer.product_id == product.product_id and
                    Offer.commercial_activity_id == activity_id
                ).first()
                if offer is None:
                    product.availability = Availability.no_availability
                else:
                    product.availability = (
                        Availability.low_availability if offer.availability >= 1.4 else Availability.no_availability
                    )
            return jsonify(fetched_activity.serialize(include_products=True))
        else:
            return "method not allowed", StatusCode.NOT_ALLOWED.value
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


@app.route('/feedback/<int:user_id>/<int:product_id>/<int:commercial_activity_id>', methods=['POST'])
def create_feedback(user_id: int, product_id: int, commercial_activity_id):
    try:
        if request.method != 'POST':
            return StatusCode.BAD_REQUEST.value
        else:
            feedback_type = FeedbackType[request.get_json()["feedback_type"]]
            feedback_comment = (
                str(request.get_json()["feedback_comment"])
                if "feedback_comment" in request.get_json()
                else None
            )
            feedback_value = (
                str(request.get_json()["feedback_comment"])
                if "feedback_value" in request.get_json()
                else None
            )
            if feedback_value is not None and feedback_type != FeedbackType.queue_awaiting:
                return "Cannot give a value for this kind of feedback", StatusCode.BAD_REQUEST.value
            inserting_feedback = Feedback(
                feedback_type=feedback_type,
                feedback_comment=feedback_comment,
                feedback_value=feedback_value,
                feedback_timestamp=datetime.datetime.utcnow(),
                user_id=user_id,
                product_id=product_id
            )
            db.session.add(inserting_feedback)
            last_feedbacks = Feedback.query.filter(
                Feedback.product_id == product_id and
                Feedback.feedback_timestamp >= datetime.datetime.utcnow() - datetime.timedelta(hours=2) and
                (
                    Feedback.feedback_type == FeedbackType.no_availability or
                    Feedback.feedback_type == FeedbackType.low_availability
                )
            ).order_by(Feedback.feedback_timestamp).limit(20)
            quantity_feedbacks = [f.feedback_type.value for f in last_feedbacks]
            for i in quantity_feedbacks:
                logger.error(i)
            availability = compute_square_exponential_mean(quantity_feedbacks)
            offer: Optional[Offer] = Offer.query.filter(
                Offer.product_id == product_id and
                CommercialActivity.commercial_activity_id == commercial_activity_id
            ).first()
            if offer is not None:
                Offer.query.filter(
                    Offer.offer_id == offer.offer_id
                ).update({"availability": availability})
            else:
                db.session.add(Offer(
                    product_id=product_id,
                    commercial_activity_id=commercial_activity_id,
                    availability=availability
                ))
            db.session.commit()
            return "OK"
    except KeyError as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value


@app.route('/near-product-availability/<float:lat>/<float:lon>/<float:radius_m>/<int:product_id>', methods=['GET'])
def get_near_product_availability(
    lat: float,
    lon: float,
    radius_m: float,
    product_id: int,
):
    results: List[dict] = []
    try:
        if request.method != 'GET':
            return "method not allowed", StatusCode.NOT_ALLOWED.value
        else:
            near_activities = []
            # TODO: Rework
            activities: List[CommercialActivity] = CommercialActivity.query.all()
            for activity in activities:
                if distance(
                    (activity.position_lat, activity.position_lon),
                    (lat, lon)
                ).meters <= radius_m and product_id in [p.product_id for p in activity.products]:
                    near_activities.append(activity)

            for activity in near_activities:
                offer: Offer = Offer.query.filter(
                    Offer.product_id == product_id and
                    Offer.commercial_activity_id == activity.commercial_activity_id
                ).first()
                if offer.availability >= 1.4:
                    adding_dict = activity.serialize()
                    adding_dict["product_availability"] = Availability.low_availability.name
                    results.append(adding_dict)
            return jsonify(results)
    except KeyError as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.BAD_REQUEST.value
    except Exception as e:
        logger.error(str(e), exc_info=True)
        return str(e), StatusCode.ERROR.value
