from itsdangerous import URLSafeTimedSerializer

from . import app

SECRET_KEY = 'my_precious'
SECURITY_PASSWORD_SALT = 'my_precious_two'
def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECRET_KEY'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=app.config['SECRET_KEY'],max_age=expiration)
    except:
        return False
    return email