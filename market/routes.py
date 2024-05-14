from market import app
from flask import render_template, redirect, url_for, flash, request
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market.models import Item, User
from market import db, bcrypt
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    if request.method == 'POST':
        # purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.add_owner(current_user)
                flash(f"Congratulations! You purchsed {p_item_object.name} for $ {p_item_object.price}", category='success')
            else:
                flash(f"Unfortunately, You don't have enough money to buy {p_item_object.name} !", category='danger')

        # sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.remove_owner(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} for $ {s_item_object.price}",
                      category='success')
            else:
                flash(f"Can't Sell !, You don't have the ownership of {s_item_object.name} !", category='danger')

        return redirect(url_for('market_page'))
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items,
                               sell_form=sell_form)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        try:
            user_to_create = User(username=form.username.data,
                                  email= form.email.data,
                                  password=form.password1.data
                                  )
            db.session.close_all()
            db.session.add(user_to_create)
            db.session.commit()
            login_user(user_to_create)
            flash(f'Account created successfully! You are now logged in as {user_to_create.username}', category='success')
            db.session.close()
            return redirect(url_for('market_page'))
        except Exception as e:
            print('exception', e)
            db.session.rollback()
            db.session.close_all()
    else:
        if form.errors !={}:
            for err_msg in form.errors.values():
                flash(f'There was an error with creating the user: {err_msg}',category='danger')


    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form .password.data
        ):
            login_user(attempted_user)
            flash(f'Succesfull! You logged in as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password do not match! Please try again', category='danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logged out !', category='info')
    return redirect(url_for('home_page'))