from src.database.models import User


class UserService:
    @classmethod
    def find_user_by_username(cls, session, username):
        return session.query(User).filter_by(
            username=username
        ).first()

    @classmethod
    def find_user_by_uuid(cls, session, uuid):
        return session.query(User).filter_by(
            uuid=uuid
        ).first()
