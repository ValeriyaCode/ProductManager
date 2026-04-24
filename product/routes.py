from flask import Blueprint, request, render_template, url_for, session, redirect, flash
from action_db import *

# Створення логічного модулю
product_bp = Blueprint('product', __name__, template_folder='templates')


def is_logged():
    return 'company_name' in session


def current_company():
    name_company = session.get('company_name')
    if not name_company:
        return None
    return get_company_by_name(name_company)


@product_bp.route('/', methods=['GET', 'POST'])
def index():
    if not is_logged():
        return redirect(url_for('auth.login'))

    # отримання компанії, під якою людина залогінилась
    company = current_company()

    if request.method == 'POST':
        name = request.form.get('name').lower()
        price = float(request.form.get('price'))
        category = request.form.get('category').lower()

        if product_exist(name, company.id):
            flash('Такий товар вже є!')
        else:
            add_product(name, price, category, company.id)
            flash('Товар додано!')

        return redirect(url_for('product.index'))

    # збираємо всі категорії
    all_categories = get_all_categories(company.id)

    # фіксуємо обрану категорії
    choice_category = request.args.get('category', 'all')

    # фільтруємо список товарів
    if choice_category == 'all':
        filter_products = get_all_products(company.id)
    else:
        filter_products = get_product_by_category(choice_category, company.id)

    return render_template('product/index.html',
                           products=filter_products,
                           categories=all_categories,
                           choice_category=choice_category)


@product_bp.route('/delete/<name>')
def delete(name):
    if not is_logged():
        return redirect(url_for('auth.login'))

    company = current_company()
    delete_product(name, company.id)

    flash(f'Товар {name} - видалено!')
    return redirect(url_for('product.index'))


@product_bp.route('/edit')
def edit():
    return render_template('product/edit.html')
