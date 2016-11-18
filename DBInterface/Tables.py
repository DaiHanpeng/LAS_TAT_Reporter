from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String,DATETIME,TEXT
from sqlalchemy.ext import declarative

def TableArgsMeta(table_args):

    class _TableArgsMeta(declarative.DeclarativeMeta):

        def __init__(cls, name, bases, dict_):
            if (    # Do not extend base class
                    '_decl_class_registry' not in cls.__dict__ and
                    # Missing __tablename_ or equal to None means single table
                    # inheritance no table for it (columns go to table of
                    # base class)
                    cls.__dict__.get('__tablename__') and
                    # Abstract class no table for it (columns go to table[s]
                    # of subclass[es]
                    not cls.__dict__.get('__abstract__', False)):
                ta = getattr(cls, '__table_args__', {})
                if isinstance(ta, dict):
                    ta = dict(table_args, **ta)
                    cls.__table_args__ = ta
                else:
                    assert isinstance(ta, tuple)
                    if ta and isinstance(ta[-1], dict):
                        tad = dict(table_args, **ta[-1])
                        ta = ta[:-1]
                    else:
                        tad = dict(table_args)
                    cls.__table_args__ = ta + (tad,)
            super(_TableArgsMeta, cls).__init__(name, bases, dict_)

    return _TableArgsMeta


BaseModel = declarative_base(
            name='Base',
            metaclass=TableArgsMeta({'mysql_engine': 'InnoDB'}))



#BaseModel = declarative_base()

class TAT_Table(BaseModel):
    __tablename__ = 'tat'
    sample_id = Column(String(48), primary_key=True, nullable=False)
    lis_order = Column(String(24))
    las_inlab = Column(String(24))
    centrifuge_in = Column(String(24))
    centrifuge_out = Column(String(24))
    decap = Column(String(24))
    advia_query = Column(String(24))
    advia_result = Column(String(24))
    centaur_query = Column(String(24))
    centaur_result = Column(String(24))
    seal = Column(String(24))
    store = Column(String(24))
    lis_upload = Column(String(24))

    def __init__(self,sample_id):
        self.sample_id = sample_id


class TAT_Update_Timestamp_Table(BaseModel):
    __tablename__ = 'tat_last_update_timestamp'
    type_id = Column(String(16), primary_key=True, nullable=False)
    last_file_update_timestamp = Column(String(24))
    last_record_update_timestamp = Column(String(24))

    def __init__(self,type_id,last_file_update_timestamp='0',last_record_update_timestamp='0'):
        self.type_id = type_id
        self.last_file_update_timestamp = last_file_update_timestamp
        self.last_record_update_timestamp = last_record_update_timestamp

