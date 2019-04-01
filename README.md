# Flask API 

This is designed as a basic json API to serve **products** and **orders** resources.

## API resources

| URL                | Method    | Description             |
| -------------------|-----------|------------------------ |
| /products/         | GET       | Get all products        |
| /products/         | POST      | Create new product      |
| /products/<int:id> | DELETE    | Delete product by id    |
| /products/<int:id> | PUT       | Update product by id    |
| /orders/           | GET       | Get all orders          |
| /orders/<int:id>   | DELETE    | Delete order by id      |
| /orders/<int:id>   | PUT       | Update order by id      |

## Heroku deployment

### Configs

```
heroku config:set FLASK_APP=flasky.py
heroku config:set FLASK_CONFIG=heroku
```
The Heroku Postgres add on will set DATABASE_URL. Make sure to set a SECRET_KEY also.

### Set up database

This project uses SQLAlchemy to define the database model. The script `manage.py` uses Flask-Migrate and Flask-Script to allow setup, migration and deployment of the model without losing existing data.
```
heroku run bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade