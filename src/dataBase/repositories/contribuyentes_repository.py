from typing import List
from dataBase.schemas.contribuyente_schema import ContribuyenteSchema
from dataBase.config.config_db import ContribuyenteModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert, and_
import calendar
import datetime


class ContribuyentesRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_contribuyente(self, contribuyente_data: ContribuyenteSchema) -> None:
        try:
            contribuyente_db = ContribuyenteModel(**contribuyente_data.dict())
            self.session.add(contribuyente_db)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error: {e}')
        finally:
            self.session.close()

   