from flask import Flask
from waitress import serve
from data import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Z,kjrjTds_secret_key'


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=5000)
    db_session.global_init("db/users_data.db")
    app.run()
