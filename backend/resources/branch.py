from flask_restful import Resource
from models import Branch

class BranchListResource(Resource):
    def get(self):
        branches = Branch.query.all()
        return [{"id": b.id, "name": b.name} for b in branches], 200
