from flasgger import LazyJSONEncoder, LazyString, Swagger
from flask import Flask

from utils.ec2_initializer import ec2_dynamo_init

app = Flask(__name__)


# Import the API routes
from routes.endpoints import *

app.json_encoder = LazyJSONEncoder


# Required because app is imported in other modules
if __name__ == "__main__":
    template = dict(
        swaggerUiPrefix=LazyString(
            lambda: request.environ.get("HTTP_X_SCRIPT_NAME", "")
        )
    )
    swagger = Swagger(app, template=template)
    ec2_dynamo_init()
    app.run(debug=True)
