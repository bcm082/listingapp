from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import Product
from flask import request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import requests

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@login_required
@main.route('/dashboard')
def dashboard():
    products = Product.query.all()
    return render_template('dashboard.html', products=products, name=current_user.name)


@main.route('/edit_product/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.sku = request.form['sku']
        product.parent_sku = request.form['parent_sku']
        product.upc = request.form['upc']
        product.product_name = request.form['product_name']
        product.product_description = request.form['product_description']
        product.quantity = request.form['quantity']
        product.price = request.form['price']
        product.bullet_point_1 = request.form['bullet_point_1']
        product.bullet_point_2 = request.form['bullet_point_2']
        product.bullet_point_3 = request.form['bullet_point_3']
        product.bullet_point_4 = request.form['bullet_point_4']
        product.bullet_point_5 = request.form['bullet_point_5']
        product.image_1 = request.form['image_1']
        product.image_2 = request.form['image_2']
        product.image_3 = request.form['image_3']
        product.image_4 = request.form['image_4']
        product.image_5 = request.form['image_5']
        product.image_6 = request.form['image_6']
        product.image_7 = request.form['image_7']
        product.video = request.form['video']
        product.aplus_1 = request.form['aplus_1']
        product.aplus_2 = request.form['aplus_2']
        product.aplus_3 = request.form['aplus_3']
        product.aplus_4 = request.form['aplus_4']
        product.aplus_5 = request.form['aplus_5']
        product.aplus_6 = request.form['aplus_6']
        product.aplus_7 = request.form['aplus_7']
        product.brand_name = request.form['brand_name']
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('edit_product.html', product=product)


@main.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        # You'll get these from the form
        new_product = Product(
            sku=request.form.get('sku'),
            parent_sku=request.form.get('parent_sku'),
            product_name=request.form.get('product_name'),
            product_description=request.form.get('product_description'),
            quantity=request.form.get('quantity'),
            price=request.form.get('price'),
            bullet_point_1=request.form.get('bullet_point_1'),
            bullet_point_2=request.form.get('bullet_point_2'),
            bullet_point_3=request.form.get('bullet_point_3'),
            bullet_point_4=request.form.get('bullet_point_4'),
            bullet_point_5=request.form.get('bullet_point_5'),
            image_1=request.form.get('image_1'),
            image_2=request.form.get('image_2'),
            image_3=request.form.get('image_3'),
            image_4=request.form.get('image_4'),
            image_5=request.form.get('image_5'),
            image_6=request.form.get('image_6'),
            image_7=request.form.get('image_7'),
            upc=request.form.get('upc'),
            asin = request.form.get('asin'),
            video = request.form.get('video'),
            aplus_1 = request.form.get('aplus_1'),
            aplus_2 = request.form.get('aplus_2'),
            aplus_3 = request.form.get('aplus_3'),
            aplus_4 = request.form.get('aplus_4'),
            aplus_5 = request.form.get('aplus_5'),
            aplus_6 = request.form.get('aplus_6'),
            aplus_7 = request.form.get('aplus_7'),
            brand_name = request.form.get('brand_name'),
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('add_product.html')


@main.route('/search', methods=['POST'])
def search():
    search = request.form.get('search')
    field_options = request.form.get('field_options')
    
    if not search:  # If the search field is empty, query all products
        products = Product.query.all()
    else:
        if field_options == "SKU":
            products = Product.query.filter(Product.sku.contains(search)).all()
        elif field_options == "Product Name":
            products = Product.query.filter(Product.product_name.contains(search)).all()
        elif field_options == "UPC":
            products = Product.query.filter(Product.upc.contains(search)).all()

    return render_template('dashboard.html', name=current_user.name, products=products)



import io
import csv
from flask import Response

@main.route('/export', methods=['GET'])
def export_data():
    products = Product.query.all()  # Get all products from the database

    # Create a string buffer
    proxy = io.StringIO()

    # Create a CSV writer and write to the string buffer
    writer = csv.writer(proxy)
    writer.writerow(['ID', 'parent_sku', 'sku', 'asin', 'upc', 'brand_name','product_name', 'product_description', 'quantity', 'price', 'bullet_point_1', 'bullet_point_2', 'bullet_point_3', 'bullet_point_4', 'bullet_point_5', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7', 'video','aplus_1', 'aplus_2', 'aplus_3', 'aplus_4', 'aplus_5', 'aplus_6', 'aplus_7'])  # Add other columns if needed

    for product in products:
        writer.writerow([product.id, product.parent_sku, product.sku, product.asin ,product.upc, product.brand_name ,product.product_name, product.product_description ,product.quantity, product.price, product.bullet_point_1, product.bullet_point_2, product.bullet_point_3, product.bullet_point_4, product.bullet_point_5, product.image_1, product.image_2, product.image_3, product.image_4, product.image_5, product.image_6, product.image_7, product.video ,product.aplus_1, product.aplus_2, product.aplus_3, product.aplus_4, product.aplus_5, product.aplus_6, product.aplus_7]) 

    # Create a byte buffer from the string buffer
    mem = io.BytesIO()
    mem.write(proxy.getvalue().encode('utf-8'))
    # moving to the start of the buffer stream
    mem.seek(0)
    proxy.close()

    return Response(
        mem, 
        mimetype='text/csv', 
        headers={'Content-Disposition': 'attachment;filename=products.csv'}
    )


import pandas as pd
from sqlalchemy.exc import IntegrityError

@main.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file:
        df = pd.read_csv(file)
        columns = ['parent_sku', 'sku', 'asin', 'upc', 'brand_name','product_name', 'product_description', 'quantity', 'price', 'bullet_point_1', 'bullet_point_2', 'bullet_point_3', 'bullet_point_4', 'bullet_point_5', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7', 'video','aplus_1', 'aplus_2', 'aplus_3', 'aplus_4', 'aplus_5', 'aplus_6', 'aplus_7']
        
        for column in columns:
            if column not in df.columns:
                flash(f'Missing column: {column}')
                return redirect(url_for('main.dashboard'))

        for index, row in df.iterrows():
            product = Product.query.filter_by(sku=row['sku']).first()
            if product:
                # Update product if it exists
                product.parent_sku = row['parent_sku']
                product.asin = row['asin']
                product.upc = row['upc']
                product.brand_name = row['brand_name']
                product.product_name = row['product_name']
                product.product_description = row['product_description']
                product.quantity = row['quantity']
                product.price = row['price']
                product.bullet_point_1 = row['bullet_point_1']
                product.bullet_point_2 = row['bullet_point_2']
                product.bullet_point_3 = row['bullet_point_3']
                product.bullet_point_4 = row['bullet_point_4']
                product.bullet_point_5 = row['bullet_point_5']
                product.image_1 = row['image_1']
                product.image_2 = row['image_2']
                product.image_3 = row['image_3']
                product.image_4 = row['image_4']
                product.image_5 = row['image_5']
                product.image_6 = row['image_6']
                product.image_7 = row['image_7']
                product.video = row['video']
                product.aplus_1 = row['aplus_1']
                product.aplus_2 = row['aplus_2']
                product.aplus_3 = row['aplus_3']
                product.aplus_4 = row['aplus_4']
                product.aplus_5 = row['aplus_5']
                product.aplus_6 = row['aplus_6']
                product.aplus_7 = row['aplus_7']
            else:
                # Create new product if it doesn't exist
                new_product = Product(
                    parent_sku=row['parent_sku'],
                    sku=row['sku'],
                    asin=row['asin'],
                    upc=row['upc'],
                    brand_name=row['brand_name'],
                    product_name=row['product_name'],
                    product_description=row['product_description'],
                    quantity=row['quantity'],
                    price=row['price'],
                    bullet_point_1=row['bullet_point_1'],
                    bullet_point_2=row['bullet_point_2'],
                    bullet_point_3=row['bullet_point_3'],
                    bullet_point_4=row['bullet_point_4'],
                    bullet_point_5=row['bullet_point_5'],
                    image_1=row['image_1'],
                    image_2=row['image_2'],
                    image_3=row['image_3'],
                    image_4=row['image_4'],
                    image_5=row['image_5'],
                    image_6=row['image_6'],
                    image_7=row['image_7'],
                    video=row['video'],
                    aplus_1=row['aplus_1'],
                    aplus_2=row['aplus_2'],
                    aplus_3=row['aplus_3'],
                    aplus_4=row['aplus_4'],
                    aplus_5=row['aplus_5'],
                    aplus_6=row['aplus_6'],
                    aplus_7=row['aplus_7']
                )
                db.session.add(new_product)
            
        try:
            db.session.commit()
            flash('Product uploaded successfully.')
        except IntegrityError:
            db.session.rollback()
            flash('There was an error uploading the product.')
        
    return redirect(url_for('main.dashboard'))

@main.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted!')
    return redirect(url_for('main.dashboard'))

# Walmart API
@main.route('/list_on_walmart/<product_id>', methods=['POST'])
def list_on_walmart(product_id):
    product = Product.query.get_or_404(product_id)

    walmart_api_url = "https://marketplace.walmartapis.com/v3/items"

    headers = {
        'Content-Type': 'application/xml',
        'Authorization': 'Basic YourWalmartApiAccessKey',
        'WM_SVC.NAME': 'Walmart Marketplace',
        'WM_QOS.CORRELATION_ID': '123456abcdef',
        'WM_SEC.ACCESS_TOKEN': 'YourWalmartApiAccessToken',
    }

    product_data = {
        'sku': product.sku,
        'upc': product.upc,
        # Include other necessary product fields here...
    }

    response = requests.post(walmart_api_url, headers=headers, data=product_data)

    if response.status_code == 200:
        return {"status": "success", "message": "Product listed on Walmart successfully!"}
    else:
        return {"status": "error", "message": "Failed to list product on Walmart."}