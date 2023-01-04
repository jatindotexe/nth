import json

import qrcode
from flask import Blueprint, render_template, flash, jsonify
from flask import request
from flask_login import login_required, current_user

from website.models import Product, Query
from . import db

views = Blueprint('views', __name__)

instances = []


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        product_description = request.form.get('product')

        info = request.form.get('nutritional-info')

        if len(str(product_description)) < 1:
            flash('Product Description is too short!', category='error')
        else:
            new_product = Product(data=product_description, nutritional_info=info)
            db.session.add(new_product)
            db.session.commit()
            instances.append(new_product)
            flash('Product added!', category='success')
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        # Add the products information to the QR code object
        qr.add_data(f"Product Description: {product_description}\nNutritional Facts: {info}")
        qr.make(fit=True)

        # Create an image from the QR code object
        img = qr.make_image(fill_color="black", back_color="white")

        img.save(f"website/static/images/qrcodes/product_QR_{new_product.id}.png")

    return render_template("home.html", user=current_user, product_list=instances)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Product.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})


@views.route('/delete-query', methods=['POST'])
def delete_query():
    query = json.loads(request.data)
    queryId = query['queryId']
    query = Product.query.get(queryId)
    if query:
        db.session.delete(query)
        db.session.commit()

    return jsonify({})


@views.route('/customer')
def customer():
    return render_template("customer.html", user=current_user)


@views.route('/ourProducts')
def ourProduct():
    return render_template("our-products.html", user=current_user, product_list=instances)


query_instances = []


@views.route('/Contact', methods=['GET', 'POST'])
def Contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        Phone = request.form.get('Phone')
        message = request.form.get('message')
        new_query = Query(email=email, name=name, phone=Phone, message=message)
        db.session.add(new_query)

        query_instances.append(new_query)
        db.session.commit()
        flash('Your query has been submitted', category='success')
    return render_template("Contact.html", user=current_user, query_instances=query_instances)


@views.route('/driverportal')
def driverportal():
    return render_template("driverportal.html", user=current_user)


@views.route('/queries', methods=['GET', 'POST'])
@login_required
def queries():
    return render_template("queries.html", user=current_user, query_instances=query_instances)
