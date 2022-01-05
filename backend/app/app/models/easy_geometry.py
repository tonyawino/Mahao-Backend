# As adapted from https://gist.github.com/kwatch/02b1a5a8899b67df2623

from sqlalchemy import func
from sqlalchemy.types import UserDefinedType, Float


class EasyGeometry(UserDefinedType):

    def get_col_spec(self):
        return "GEOMETRY"

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, type_=self)

    def column_expression(self, col):
        return func.ST_AsText(col, type_=self)

    def bind_processor(self, dialect):
        def process(value):
            if value is None:
                return None
            if (isinstance(value, list)):
                value = tuple(value)
            assert isinstance(value, tuple)
            lat, lng = value
            return "POINT(%s %s)" % (lng, lat)
        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None:
                return None
            #m = re.match(r'^POINT\((\S+) (\S+)\)$', value)
            #lng, lat = m.groups()
            lng, lat = value[6:-1].split()  # 'POINT(135.00 35.00)' => ('135.00', '35.00')
            return (float(lat), float(lng))
        return process

