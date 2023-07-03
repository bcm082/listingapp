from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import Product
from flask import request, redirect, url_for, flash

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
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('edit_product.html', product=product)


@main.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        # You'll get these from the form
        new_product = Product(
            sku=request.form['sku'],
            parent_sku=request.form['parent_sku'],
            product_name=request.form['product_name'],
            product_description=request.form['product_description'],
            quantity=request.form['quantity'],
            price=request.form['price'],
            bullet_point_1=request.form['bullet_point_1'],
            bullet_point_2=request.form['bullet_point_2'],
            bullet_point_3=request.form['bullet_point_3'],
            bullet_point_4=request.form['bullet_point_4'],
            bullet_point_5=request.form['bullet_point_5'],
            image_1=request.form['image_1'],
            image_2=request.form['image_2'],
            image_3=request.form['image_3'],
            image_4=request.form['image_4'],
            image_5=request.form['image_5'],
            image_6=request.form['image_6'],
            image_7=request.form['image_7'],
            upc=request.form['upc'],
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
    writer.writerow(['ID', 'Parent SKU', 'SKU', 'UPC', 'Product Name', 'Quantity', 'Price', 'Bullet 1', 'Bullet 2', 'Bullet 3', 'Bullet 4', 'Bullet 5', 'Image 1', 'Image 2', 'Image 3', 'Image 4', 'Image 5', 'Image 6', 'Image 7'])  # Add other columns if needed

    for product in products:
        writer.writerow([product.id, product.parent_sku, product.sku, product.upc, product.product_name, product.quantity, product.price, product.bullet_point_1, product.bullet_point_2, product.bullet_point_3, product.bullet_point_4, product.bullet_point_5, product.image_1, product.image_2, product.image_3, product.image_4, product.image_5, product.image_6, product.image_7]) 

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
        columns = ['parent_sku', 'sku', 'upc', 'product_name', 'product_description', 'quantity', 'price', 'bullet_point_1', 'bullet_point_2', 'bullet_point_3', 'bullet_point_4', 'bullet_point_5', 'image_1', 'image_2', 'image_3', 'image_4', 'image_5', 'image_6', 'image_7']
        
        for column in columns:
            if column not in df.columns:
                flash(f'Missing column: {column}')
                return redirect(url_for('main.dashboard'))

        for index, row in df.iterrows():
            product = Product.query.filter_by(sku=row['sku']).first()
            if product:
                # Update product if it exists
                product.parent_sku = row['parent_sku']
                product.upc = row['upc']
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
            else:
                # Create new product if it doesn't exist
                new_product = Product(
                    parent_sku=row['parent_sku'],
                    sku=row['sku'],
                    upc=row['upc'],
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
