import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

SQLALCHEMY_DATABASE_URI = "postgres://ytzdndsnqvuldm:1318c09ffc2d43a0a709d7a4fe8afdc634671f636cdb83b23e6c5e45638a05a7@ec2-54-83-9-169.compute-1.amazonaws.com:5432/des9u24kajmdet"
# if os.environ.get('DATABASE_URL') is None:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# else:
#     SQLALCHEMY_DATABASE_URI = os.environ[
#         'postgres://utygragveybltz:f211025758b25654a04569c2be3af825445662e249b2aa31d8d7d7d7c2aae977@ec2-54-235-94-36.compute-1.amazonaws.com:5432/ddmj239v0ej6li']
