import pandas as pd
import mysql.connector

df = pd.read_csv("tp_final_data_pipeline/samples/users.csv")

def stockageJsonSQL(data):
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="leaderboard"
    )
    cursor = mydb.cursor()
    #Remplissage de la langue french
    for row in data["first_name"]:
        sql = "INSERT INTO users (first_name) VALUES (%s)"
        val = (row,)
        cursor.execute(sql, val)
    #Validation finales des insertions
    mydb.commit()
    print(cursor.rowcount, "enregistrement inséré.")
    #Fermeture de la connexion SQL
    cursor.close()
    mydb.close()
    
stockageJsonSQL(df)