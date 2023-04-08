from dataBase.schemas.timbrados_schema import TimbradoSchema
from dataBase.config.config_db import Timbrados
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert


class TimbradosRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_timbrado(self, timbrado_data: TimbradoSchema) -> None:
        try:
            timbrado_db = Timbrados(**timbrado_data.dict())
            self.session.add(timbrado_db)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error: {e}')
        finally:
            self.session.close()
