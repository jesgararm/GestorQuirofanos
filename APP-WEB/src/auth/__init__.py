from flask import Blueprint
auth_blueP = Blueprint('auth', __name__, template_folder='templates')
from . import routes