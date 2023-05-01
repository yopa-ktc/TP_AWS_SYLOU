from pathlib import Path
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.Repository_leaderboard import LeaderBoard_Repository
from feed_database import feed_database


engine = create_engine("sqlite:///leaderboard.db", pool_pre_ping=True)
declarative_base().metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
app = Flask(__name__)

#API REST : localhost:5000/feed, elle est appellée pour alimentée la base de données
#Si le corps de la requete ne contient pas le chemin du fichier il y'a erreur :
#Si le chemin est bon alors la methode feeddatabase de notre classe feedbase est appelée.
@app.route("/feed", methods=["POST"])
def feed():
    data_path = request.json.get("data_path")
    if data_path != "pipeline_result.csv":
        message = "Erreur sur le chemin du fichier !"
    else:
        feed_database(data_path)
        message = "insertion terminée !"
    return jsonify({"message" : message})


#API REST : localhost:5000/leaderboard, elle est appellée pour récupérer les messages par noms d'auteurs
#Une première fonction "get_messages_count_by_user_id" compte le nombre de messages et l'associe à un user_id
#Une seconde fonction "get_all_messages" renvoie tous les valeurs de la table leaderboard
#A la fin, nous faisons une association pour renvoyer toutes les lignes avec le nombre de messages
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