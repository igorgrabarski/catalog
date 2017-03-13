"""
Implementation of Catalog Application
Created by Igor Grabarski
March, 13, 2017
"""
from flask import Flask
from flask import abort
from flask import jsonify
from flask import flash
from flask import url_for
from flask import redirect
from flask import request
from flask import render_template
from flask import session as local_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from entities import *
from collections import OrderedDict
import random
import string
from oauth2client import client, crypt


app = Flask(__name__)

"""
Secret key is needed for Flask session implementation . Change it to
your own!
"""
app.secret_key = \
    'kugk4gku23f4f23yf4jhch43chj43c5jhl4c6jghd6ghkdclhjcvk5cvh23c5n235cxgh2'

"""
Insert your own CLIENT_ID
To get one, go to https://console.developers.google.com/
"""
CLIENT_ID = 'WRITE_YOUR_CLIENT_ID_HERE'


# ********* One-time created 'heavy' engine instance and a session *********
engine = create_engine('postgresql:///catalog', echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()


# ***************************** Main page route *****************************
@app.route('/')
def home():
    return redirect(url_for('main', category_id=1, item_id=0))


# ************************** Category and/or item choice route **************
@app.route('/<int:category_id>/<int:item_id>/')
def main(category_id, item_id):

    # Anti - forgery protection string
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    local_session['state'] = state

    categories = session.query(Category).all()

    items = session.query(Item).filter_by(category_id=category_id).all()

    """
    This block of code fetches the description of active item and its author:
    """
    if len(items) > 0:
        if item_id == 0:
            description = items[0]
        else:
            description = session.query(Item).filter_by(id=item_id).one()
        author = session.query(User).filter_by(id=description.user_id).one()
    else:
        description = {'description': 'None'}
        author = {'user_name': 'None'}

    return render_template('index.html',
                           categories=categories,
                           items=items,
                           description=description,
                           author=author,
                           category_active_id=category_id,
                           local_session=local_session,
                           state=state)


# ********************************* Add item route ***********************
"""
    Only authenticated user and only with POST method
    is allowed to add new item
"""


@app.route('/add_item/', methods=['POST'])
def add_item():

    if 'name' in local_session:
        category_id = request.form['category']
        name = request.form['item_name']
        description = request.form['item_description']
        user_id = local_session['id']

        item = Item(
            name=name,
            description=description,
            category_id=category_id,
            user_id=user_id)

        session.add(item)

        session.commit()

        flash('Item Added', 'popup')
    else:
        abort(403)

    return redirect(url_for('main', category_id=1, item_id=0))


# ********************************* Edit item route ***********************
"""
    Only authenticated user and only with POST method
    is allowed to edit his/her items
"""


@app.route('/edit_item/', methods=['POST'])
def edit_item():
    item_id = request.form['item_id']
    creator_id = session.query(Item).filter_by(id=item_id).one().user_id
    if 'name' in local_session:
        """ Here we check if the person that is trying to edit the item
            is the one who has created it.
        """
        if local_session['id'] == creator_id:
            item = session.query(Item).filter_by(id=item_id).one()

            item.name = request.form['item_name']
            item.description = request.form['item_description']

            session.add(item)
            session.commit()
            flash('Item Updated', 'popup')
        else:
            flash('Not allowed to edit this item', 'popup')

        return redirect(url_for('main', category_id=1, item_id=0))
    else:
        abort(403)


# ********************************* Delete item route *********************
"""
    Only authenticated user and only with POST method
    is allowed to delete his/her items
"""


@app.route('/delete_item/', methods=['POST'])
def delete_item():
    item_id = request.form['item_id']
    creator_id = session.query(Item).filter_by(id=item_id).one().user_id
    if 'name' in local_session:
        """ Here we check if the person that is trying to delete the item
            is the one who has created it.
        """
        if local_session['id'] == creator_id:
            item = session.query(Item).filter_by(
                id=request.form['item_id']).one()
            session.delete(item)
            session.commit()
            flash('Item Deleted', 'popup')
        else:
            flash('Not allowed to delete this item', 'popup')
    else:
        flash('Please sign in', 'popup')
    return redirect(url_for('main', category_id=1, item_id=0))


# ********************************* API endpoint route ********************
"""
    Any user can access this endpoint and download
    the JSON with all related data
"""


@app.route('/catalog.json/')
def get_json():

    categories = [c.serialize for c in session.query(Category).all()]

    items = [i.serialize for i in session.query(Item).all()]

    for c in categories:
        if 'Item' not in c:
            c['Item'] = []
        for item in items:
            if item['cat_id'] == c['id']:
                c['Item'].append(item)
        if len(c['Item']) == 0:
            del c['Item']

    return jsonify(Category=categories)


# ************************************** Sign in route ********************
"""
    Only unlogged user and only with POST method is allowed to sign in
"""


@app.route('/login/', methods=['POST'])
def login():
    if request.form.get('state') != local_session['state']:
        flash('Wrong Credentials', 'popup')
        return redirect(url_for('main', category_id=1, item_id=0))

    # Check if user is not already signed in
    if 'name' not in local_session:
        # Here we receive the ID token from frontend JS 'onSignIn' function
        id_token = request.form.get('id_token')

        try:
            idinfo = client.verify_id_token(id_token, CLIENT_ID)

            # User's Google account verification
            if idinfo['iss'] not in \
                    ['accounts.google.com', 'https://accounts.google.com']:
                raise crypt.AppIdentityError("Wrong issuer.")

        except crypt.AppIdentityError:
            flash('Wrong credentials', 'popup')
            return 'signedin'

        # Flask session creation
        local_session['id'] = idinfo['sub']
        local_session['name'] = request.form.get('name')
        local_session['image'] = request.form.get('imageUrl')
        local_session['email'] = request.form.get('email')

        """
        The block below adds the first-time Google
        authenticated user to the local database
        """
        users = [u.serialize for u in session.query(User).all()]

        for user in users:
            if local_session['id'] == user['id']:
                flash('Signed in as ' + local_session['name'], 'popup')
                return 'signedin'

        user = User(id=local_session['id'],
                    user_name=local_session['name'],
                    image_url=local_session['image'],
                    email=local_session['email'],
                    provider='google')
        session.add(user)
        session.commit()

        flash('Signed in as ' + local_session['name'], 'popup')
        return 'signedin'
    else:
        return 'Already signed in'


# ************************************** Sign out route *******************
"""
    Only signed in user and only with POST method is allowed to sign out
"""


@app.route('/logout/', methods=['POST'])
def logout():
    if 'name' in local_session:
        local_session.pop('name', None)
        flash('Signed out', 'popup')
        return 'signedout'
    else:
        return 'Not signed in'


# *********************** Application invocation block ********************
if __name__ == '__main__':
    # Change debug to 'True' in development. Never use it on production
    # machine!!!
    app.debug = False

    # Change the host and the port to appropriate values on your server
    app.run(host='0.0.0.0', port=8000)
