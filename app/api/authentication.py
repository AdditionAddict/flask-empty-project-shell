from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_login import current_user
from .errors import unauthorized, forbidden
from . import api
from ..models import User

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(name_or_token, password):
    """Return True if login valid; Uses the User method verify_password;
    If password is blank, token is assumed"""
    print('login:', name_or_token, password)
    if name_or_token == '':
        return False
    if password == '':
        g.current_user = User.verify_auth_token(name_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(username=name_or_token).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)

@auth.error_handler
def auth_error():
    return jsonify({'success': False})

@api.route('/login', methods=['POST'])
@auth.login_required
def get_token():
    print('login route')
    if g.current_user.is_anonymous or g.token_used:
        print('auth failed')
        print(g.current_user.is_anonymous)
        print(g.token_used)
        return jsonify({'success': False})
    print('auth succeed')
    print(jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600, 'success': True}))
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600, 'success': True})
