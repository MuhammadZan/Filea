"""Define an Abstract Base Class (ABC) for models."""
import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class BaseModel():
    """ Generalize __repr__ and to_json for MongoEngine documents """

    print_filter = ('_id',)
    
    def __repr__(self):
        """ Define a base way to print models
            Fields inside `print_filter` are excluded """
        return '%s(%s)' % (self.__class__.__name__, {
            field: value
            for field, value in self._to_dict().items()
            if field not in self.print_filter
        })

    to_json_filter = ('_id',)
    
    @property
    def json(self):
        """ Define a base way to jsonify models
            Fields inside `to_json_filter` are excluded """
        result = {}
        for field, value in self._to_dict().items():
            if field not in self.to_json_filter:
                if isinstance(value, datetime.datetime):
                    result[field] = value.isoformat()
                elif isinstance(value, datetime.date):
                    result[field] = value.isoformat()
                else:
                    result[field] = value
        return result

    def _to_dict(self):
        """ Convert document to dictionary
            Allows to_json to be overriden without impacting __repr__ """
        result = {}
        for field_name in self._fields:
            value = getattr(self, field_name, None)
            result[field_name] = value
        # Include id as a string
        if hasattr(self, 'id'):
            result['id'] = str(self.id)
        return result
