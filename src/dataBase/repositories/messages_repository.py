from dataBase.schemas.messages_schema import MessageSchema
from dataBase.config.config_db import TimbradosModel, MessagesModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import insert

# TODO: realizar correctamente
class MessagesRepository():
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_message(self, message_data: MessageSchema) -> None:
        try:
            message_db = TimbradosModel(**message_data.dict())
            self.session.add(message_db)
            self.session.commit()
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error: {e}')
        finally:
            self.session.close()

    def get_messages_by_user_id(self, user_id: int) -> None:
        try:
            message_db = self.session.query(
                MessagesModel).filter_by(from_user_id=user_id).first()

            return message_db
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f'Error: {e}')
        finally:
            self.session.close()
