from pathlib import Path
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Repository_leaderboard import LeaderBoard_Repository


engine = create_engine("sqlite:///leaderboard.db", pool_pre_ping=True)
declarative_base().metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)


@app.route("/feed", methods=["POST"])
def feed():
    data_path = request.json.get("data_path")
    if not data_path:
        return jsonify({"message": "data_path is missing"}), 400
    

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    nbre_message_userId = LeaderBoard_Repository(session).get_messages_count_by_user_id()
    get_all_leadboard = LeaderBoard_Repository(session).get_all_messages()
    
    all_lead = []
    for lead in get_all_leadboard:
        all_lead.append({"id": lead.id, "user_id": lead.user_id, "name": lead.name, "message": nbre_message_userId[lead.user_id]})
    return all_lead
    
    
    
if __name__ == "__main__":
    app.run()   