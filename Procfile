web: gunicorn run:app 
export FLASK_APP=run
flask db init 
flask db migrate 
flask db upgrade
heroku ps:scale web=1