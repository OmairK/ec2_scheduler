from flask import Flask

app = Flask(__name__)

# Import the API routes
from routes.endpoints import *

# Required because app is imported in other modules
if __name__== '__main__':
    app.run(debug=True)