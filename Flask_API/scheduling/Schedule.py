# Clase para organizar la agenda quirúrgica
# Es un recurso de la API
import pandas as pd
from flask import request, jsonify
from flask_restful import Resource
import sys
sys.path.append('../../')
import Modelos.Utils.common as utils
from Optimizacion.Genético import utilsGenetico as utilsG
from deap import base, creator, tools, algorithms

class Schedule(Resource):
    pass