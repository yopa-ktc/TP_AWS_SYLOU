from typing import List, Dict, Any
from sqlalchemy import func
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
    
    def get_all_messages_grouped_by_user_id(self) -> List[Dict[str, Any]]:
        query = self.db_session.query(Leaderboard.user_id, Leaderboard.name, Leaderboard.message)\
                    .group_by(Leaderboard.user_id)\
                    .order_by(Leaderboard.user_id.asc())

        messages_by_user_id = [{"user_id": user_id, "name": name, "message_count": message_count}
                               for user_id, name, message_count in query.all()]

        return messages_by_user_id
    
    def get_messages_count_by_user_id(self) -> Dict[int, int]:
        result = self.db_session.query(
            Leaderboard.user_id,
            func.count(Leaderboard.id)
        ).group_by(Leaderboard.user_id).all()
        return dict(result)