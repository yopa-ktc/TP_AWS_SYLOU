from typing import List
from sqlalchemy.orm import Session

from app.Model_leaderboard import Leaderboard


class LeaderBoard_Repository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_messages_by_id(self, user_id: int) -> Leaderboard:
        return self.db_session.query(Leaderboard).filter(Leaderboard.id == user_id).first()

    def get_all_messages(self) -> List[Leaderboard]:
        return self.db_session.query(Leaderboard).all()

    def create_Leaderboard(self, user_id: int, name: str, message: str) -> Leaderboard:
        new_Leaderboard = Leaderboard(user_id = user_id, name=name, message=message)
        self.db_session.add(new_Leaderboard)
        self.db_session.commit()
        return new_Leaderboard