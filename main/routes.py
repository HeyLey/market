from flask import render_template, request, url_for, redirect, session
from flask import Blueprint
from main.models import User, Order, Item, db
import datetime

import logging

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('main.show_items'))
    return redirect(url_for('main.login'))


@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'user' in session:
        return redirect(url_for('main.show_items'))
    if request.method == 'POST':
        users = User.query.all()
        usernames = []
        for u in users:
            usernames.append(u.username)
        username = request.form['username']
        password = request.form['password']
        if username not in usernames or password != User.query.filter_by(username=username).first().password:
            error = 'Invalid Credentials. Please try again.'
            logging.info(error)
        else:
            logging.info("Logged")
            session['user'] = username
            return redirect(url_for('main.show_user_acc', username=username))
    return render_template('login.html', error=error)


@bp.route('/<string:username>')
def show_user_acc(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        logging.debug(f'User {username} not found.')
        return redirect(url_for('main.show_items'))
    elif 'user' not in session or session['user'] != username:
        logging.info(f'Wrong')
        return redirect(url_for('main.show_items'))
    else:
        user_id = user.user_id
        orders = Order.query.filter_by(user_id=user_id).all()
        items = Item.query.filter_by(user_id=user_id).all()
        balance = user.balance
        return render_template('user_page.html', username=username, orders=orders, items=items, balance=balance)


@bp.route('/sell_item', methods=['GET', 'POST'])
def sell_item():
    if 'user' in session:
        error = None
        username = session['user']
        if request.method == 'POST':
            about = request.form['about']
            pic = request.form['pic']
            price = request.form['price']
            if about == "" or price == "":
                error = "Please add product info."
                return render_template('sell_item.html', username=username, error=error)
            user_id = User.query.filter_by(username=username).first().user_id
            new_product = Item(user_id=user_id, about=about, pic=pic, price=price)
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('main.show_user_acc', username=username))
        return render_template('sell_item.html', username=username, error=error)
    return redirect(url_for('main.login'))


@bp.route('/products')
def show_items():
    items = Item.query.filter_by(is_in_stock=True).all()
    if 'user' in session:
        return render_template('products.html', items=items, username=session['user'])
    return render_template('products.html', items=items)


@bp.route('/thank_you/<username>')
def thank_you(username):
    return render_template('thank_you.html', username=username)


@bp.route('/delete_item/<item_id>', methods=['POST'])
def delete_item(item_id):
    if 'user' in session:
        username = session['user']
        user = User.query.filter_by(username=username).first()
        item = Item.query.filter_by(user_id=user.user_id).filter_by(is_in_stock=True).filter_by(item_id=item_id).first()
        if item is not None:
            db.session.delete(item)
            db.session.commit()
        return redirect(url_for('main.show_user_acc', username=username))
    return redirect(url_for('main.show_items'))


@bp.route('/return_item/<item_id>', methods=['POST'])
def return_item(item_id):
    if 'user' in session:
        if item_id is not None:

            username = session['user']
            buyer = User.query.filter_by(username=username).first()

            order = Order.query.filter_by(user_id=buyer.user_id).filter_by(is_ret=False).filter_by(item_id=item_id).first()

            if order is not None:
                item = Item.query.filter_by(item_id=item_id).first()
                seller_id = item.user_id
                item_price = item.price
                seller = User.query.filter_by(user_id=seller_id).first()

                buyer.balance = buyer.balance + item_price
                seller.balance = seller.balance - item_price

                item.is_in_stock = True

                order.is_ret = True
                order.returned_on = datetime.datetime.now()
                db.session.commit()
        return redirect(url_for('main.show_user_acc', username=username))
    return redirect(url_for('main.show_items'))


@bp.route('/buy_item/<item_id>', methods=['POST'])
def buy_item(item_id):
    if 'user' in session:
        if item_id is not None:
            item = Item.query.filter_by(item_id=item_id).filter_by(is_in_stock=True).first()
            if item is None:
                return redirect(url_for('main.show_items'))

            username = session['user']
            buyer = User.query.filter_by(username=username).first()
            seller_id = item.user_id
            seller = User.query.filter_by(user_id=seller_id).first()
            if buyer == seller:
                return redirect(url_for('main.show_items'))
            else:
                item_price = item.price
                seller = User.query.filter_by(user_id=seller_id).first()

                buyer.balance = buyer.balance - item_price
                seller.balance = seller.balance + item_price

                item.is_in_stock = False

                new_order = Order(user_id=buyer.user_id, item_id=item_id, price=item.price)
                db.session.add(new_order)
                db.session.commit()
        return redirect(url_for('main.thank_you', username=username))
    return redirect(url_for('main.login'))

