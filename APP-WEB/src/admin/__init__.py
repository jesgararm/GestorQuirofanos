from flask import Blueprint
adminBP = Blueprint('admin', __name__, template_folder='templates')
from . import routes