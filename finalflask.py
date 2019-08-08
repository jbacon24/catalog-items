
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Beauty, BeautyItem
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Beauty Items Application"


# Connect to Database and create database session
engine = create_engine('sqlite:///beautyitems.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
    for x in xrange(32))
    login_session['state'] = state
        # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output

# Disconnect user from session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s'), access_token
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# Display a product in JSON format
@app.route('/product/<int:beauty_id>/item/JSON')
def beautyProductsJSON(beauty_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    beauty = session.query(Beauty).filter_by(id=beauty_id).one()
    items = session.query(BeautyItem).filter_by(beauty_id=beauty_id).all()
    return jsonify(BeautyItems=[i.serialize for i in items])

# Display beauty item in JSON format
@app.route('/product/<int:beauty_id>/item/<int:item_id>/JSON')
def beautyItemJSON(beauty_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    Beauty_Item = session.query(BeautyItem).filter_by(id=item_id).one()
    return jsonify(Beauty_Item=Beauty_Item.serialize)

# Display all products in JSON format
@app.route('/product/JSON')
def productsJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    beauty = session.query(Beauty).all()
    return jsonify(beauty=[r.serialize for r in beauty])


# Show all products on homepage of app
@app.route('/')
@app.route('/product/')
def showProducts():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    products = session.query(Beauty).order_by(asc(Beauty.name))
    return render_template('products.html', products=products)

# Create a new product
@app.route('/product/new/', methods=['GET', 'POST'])
def newProduct():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newProduct = Beauty(name=request.form['name'])
        session.add(newProduct)
        session.commit()
        return redirect(url_for('showProducts'))
    else:
        return render_template('newProduct.html')

# Edit a product
@app.route('/product/<int:beauty_id>/edit/', methods=['GET', 'POST'])
def editProduct(beauty_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedProduct = session.query(
        Beauty).filter_by(id=beauty_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedProduct.name = request.form['name']
            return redirect(url_for('showProducts'))
    else:
        return render_template(
            'editProduct.html', product=editedProduct)

# Delete a product
@app.route('/product/<int:beauty_id>/delete/', methods=['GET', 'POST'])
def deleteProduct(beauty_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    productToDelete = session.query(
        Beauty).filter_by(id=beauty_id).one()
    if request.method == 'POST':
        session.delete(productToDelete)
        session.commit()
        return redirect(
            url_for('showProducts', beauty_id=beauty_id))
    else:
        return render_template(
            'deleteProduct.html', product=productToDelete)

# Show a beauty item
@app.route('/product/<int:beauty_id>/')
@app.route('/product/<int:beauty_id>/item/')
def showItem(beauty_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    beauty = session.query(Beauty).filter_by(id=beauty_id).one()
    items = session.query(BeautyItem).filter_by(
        beauty_id=beauty_id).all()
    return render_template('item.html', items=items, beauty=beauty)

# Create a new beauty item
@app.route(
    '/product/<int:beauty_id>/item/new/', methods=['GET', 'POST'])
def newBeautyItem(beauty_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newItem = BeautyItem(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], feature=request.form['feature'], beauty_id=beauty_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItem', beauty_id=beauty_id))
    else:
        return render_template('newbeautyitem.html', beauty_id=beauty_id)

# Edit a beauty item
@app.route('/product/<int:beauty_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editBeautyItem(beauty_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedItem = session.query(BeautyItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['feature']:
            editedItem.feature = request.form['feature']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showItem', beauty_id=beauty_id))
    else:

        return render_template(
            'editbeautyitem.html', beauty_id=beauty_id, item_id=item_id, item=editedItem)

# Delete a beauty item
@app.route('/product/<int:beauty_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteBeautyItem(beauty_id, item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    itemToDelete = session.query(BeautyItem).filter_by(id=item_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showItem', beauty_id=beauty_id))
    else:
        return render_template('deleteBeautyItem.html', item=itemToDelete)


if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
