from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_login import current_user
from database.models import Product, Transaction, db
from database.config import connection
from api.app.create_app import cache
from .utils import Operations
from datetime import datetime
from psycopg2 import sql


bp_views = Blueprint('bp_views', __name__)

operation = Operations(cache=cache,
                       cache_key='products')

@bp_views.route('/')
def home():
    return render_template('home.html')


@bp_views.route('/market', methods=["GET","POST"])
def market():
    if not current_user.is_authenticated:
        return redirect(url_for("bp_auth.login"))

    allProducts = Product.query.all()
    product_cache_key = 'products'
    product_list = cache.get(product_cache_key) or []
    total_products = len(product_list)
   
    return render_template("market.html", allProducts=allProducts, total_products=total_products)


@bp_views.route('/checkout', methods=["GET", "POST"])
def checkout():
    if not current_user.is_authenticated:
        flash('You need to be logged in to checkout.', 'warning')
        return redirect(url_for("bp_auth.login"))
    
    products_list = operation.get_products()
    total, products_cart, quantity = operation.cart_information(products_list=products_list, Product=Product)
    
    if len(products_list) == 0:
        return redirect(url_for("bp_views.market"))
    
    if request.method == 'POST':
        created_at = datetime.utcnow()
        client_id = current_user.id
        address = request.form.get("address")
        second_address = request.form.get("second_address")
        country = request.form.get("country")
        state = request.form.get("state")
        zip_code = request.form.get("zip_code")
        card_number = request.form.get("card_number")
        expiration_date = request.form.get("expiration_date")
        cvv = request.form.get("cvv")
        total = request.form.get("submit-value")
        


        if len(card_number)>19 or len(card_number)<16:
            flash("Insert a valid number card", "alert")
        elif len(cvv)<3 or len(cvv)>3:
            flash("Insert a valid cvv number", "alert")
        elif '/' not in expiration_date:
            flash("Invalid expiration date format [MM/YY]", "alert")
        elif int(expiration_date.split("/")[1])<datetime.now().year:
            flash("Expired card", "danger")
        elif int(expiration_date.split("/")[0])<0 or int(expiration_date.split("/")[0])>12 :
            flash("Invalid expiration date month", "alert")
        else:
            transaction = Transaction(created_at=created_at,
                                      client_id=client_id,
                                      total=str(total),
                                      address=address,
                                      second_address=second_address,
                                      country=country,
                                      state=state,
                                      zip_code=zip_code,
                                      card_number=card_number)
            
            try:
                db.session.add(transaction)
                
                products_list = operation.get_products()
                products_quantity = operation.get_product_quantity(products=products_list)

                       
                sqlQ =sql.SQL("""
                    UPDATE products
                    SET inventory = inventory - %s
                    WHERE id = %s;
                """)

                cursor = connection.cursor()
                for id in products_quantity:
                    print(id, products_quantity[id])
                    cursor.execute(sqlQ,(products_quantity[id], int(id)))

                connection.commit()
                db.session.commit()
                cursor.close()
                connection.close()
                
                flash('Transaction successful!', 'success')
                cache.clear()

                return redirect(url_for('bp_views.market'))
            
            except Exception as e:
                db.session.rollback()
                print("Error:", str(e))
                flash('Failed to save transaction.', 'danger')
        
    return render_template("checkout.html", products_list=products_cart, total_products=quantity, total=total)


@bp_views.route('/add_product', methods=["POST"])
def add_product():
    product = request.form.get("product_id")
    if not product:
        return jsonify({'error': 'No product provided'}), 400
    products_list = operation.add_product(product)
    return jsonify({'message': 'Product added', 'product_list': products_list})


@bp_views.route('/clear_cart', methods=["POST"])
def clear_cart():
    cache.clear()
    return redirect(url_for('bp_views.market'))


@bp_views.route('/delete_product', methods=["POST"])
def delete_product():
    product = request.form.get("product_id")
    if not product:
        return jsonify({'error': 'No product provided'}), 400
    operation.delete_product(product)
    return jsonify({'message': 'Product deleted'})



