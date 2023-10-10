from typing import List
from dataBase.schemas.timbrados_schema import TimbradoSchema
from dataBase.config.config_db import TimbradosModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, and_
import calendar
import datetime


class TimbradosRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_timbrado(self, timbrado_data: TimbradoSchema) -> None:
        try:
            timbrado_db = TimbradosModel(**timbrado_data.dict())
            self.session.add(timbrado_db)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error: {e}')
        finally:
            self.session.close()

    def get_timbrado_by_date(self, month: int, year: int) -> List[TimbradoSchema]:
        try:
            num_days = calendar.monthrange(year, month)[1]
            start_date = datetime.date(year, month, 1)
            end__date = datetime.date(year, month, num_days)

            timbrados_db = self.session.query(
                TimbradosModel).filter(and_(TimbradosModel.end_date >= start_date, TimbradosModel.end_date <= end__date)).all()
        
            return timbrados_db
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error: {e}')
        finally:
            self.session.close()
