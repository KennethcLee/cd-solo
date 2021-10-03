from flask_app.controllers import logins, games, scores

from flask_app import app

if __name__=="__main__":
    app.run(debug=True, port=8088)