from flask import Flask

app = Flask(__name__)

# Import the API routes
from routes.endpoints import *
from flasgger import Swagger


# Required because app is imported in other modules
if __name__== '__main__':
    Swagger(app)
    app.run(debug=True)