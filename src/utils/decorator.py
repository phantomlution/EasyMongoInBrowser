from functools import wraps
import json
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


def flask_response(func):
    @wraps(func)
    def response(*args, **kwargs):
        try:
            data = func(*args, **kwargs)
            return JSONEncoder().encode({
                "code": "200",
                "data": data
            })
        except Exception as e:
            print(e)
            return JSONEncoder().encode({
                "code": '400',
                "message": str(e)
            })
    return response
