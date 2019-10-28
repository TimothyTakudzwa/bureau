export FLASK_APP=run
flask db init 
flask db migrate 
flask db upgrade
web: gunicorn run:app 

heroku ps:scale web=1