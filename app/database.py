import random
from app import db

def query_name():
    return random.choice(["Alice", "Bob", "Chris", "Dolly"])

def get_trends():
    conn = db.connect()
    query_response = conn.execute("SELECT Trends.trend_name, Songs.name FROM Trends Join Songs on Songs.song_id = Trends.recent_song_id").fetchall()

    # print(query_response)
    conn.close()
    return query_response

def get_songs_without_trends():
    conn = db.connect()
    query_response = conn.execute("SELECT name FROM Songs;").fetchall()
    conn.close()
    # print(query_response)
    return query_response

def delete_song_from_trend(songname):
    conn = db.connect()
    conn = db.connect()
    query_1 = "SELECT song_id from Songs WHERE name LIKE \"" + songname + "\" ;"
    query_response1 = conn.execute(query_1).fetchall()
    if query_response1 == []:
        conn.close()
        return "Error: Song does not exist in database."
    song_id = query_response1[0][0]
    
    query_2 = "SELECT * from SongTrends WHERE song_id LIKE \"" + str(song_id) + "\" ;"
    query_response2 = conn.execute(query_2).fetchall()
    # print("2", query_2)
    if query_response2 == []:
        conn.close()
        return "Error: Song does not already have a trend associated with it."
        
    
    query_response = conn.execute("DELETE FROM SongTrends WHERE song_id LIKE \"" + str(song_id) + "\";")
    conn.close()
    # print(query_response)
    return "Successfully removed."
# todo modify
def insert_new_trend(trendname, songname):
    conn = db.connect()
    query_1 = "SELECT song_id from Songs WHERE name LIKE \"" + songname + "\" ;"
    query_response1 = conn.execute(query_1).fetchall()
    if query_response1 == []:
        conn.close()
        return "Error: Song does not exist in database."
        
    
    song_id = query_response1[0][0]

    query_2 = "SELECT trend_name from SongTrends WHERE song_id LIKE \"" + str(song_id) + "\" ;"
    query_response2 = conn.execute(query_2).fetchall()

    if(query_response2 == []):

        query_3 = "INSERT INTO SongTrends VALUES( \"" + str(song_id) + "\", \"" + trendname + "\" ) ;"
        query_response3 = conn.execute(query_3)

        query_4 = "SELECT song_id FROM SongTrends WHERE trend_name LIKE \"" + trendname + "\" ;"
        query_response4 = conn.execute(query_4).fetchall()
        song_id2 = query_response4[0][0]
        
        query_5 = "SELECT name, album, artist FROM Songs WHERE song_id LIKE \"" + song_id2 + "\";"
        query_response5 = conn.execute(query_5).fetchall()

        conn.close()
        return "Added Song to Trend Successfully ----> Just in case you were curious, the most recently added song to trend was: (Song Name: "+str(query_response5[0][0]) +"\n\n, Album: "+ str(query_response5[0][1]) + "\n\n, Artist: " + str(query_response5[0][2]) + ")"
    conn.close()
    return "Error: Song already belongs to another trend (\""+str(query_response2[0][0])+"\") in database. Try Again."
    
def get_songs_for_trend(trendname):
    conn = db.connect()
    query = "SELECT name FROM SongTrends natural join Songs WHERE trend_name LIKE \"" + str(trendname) + "\" ;"
    # print(query)
    query_response = conn.execute(query).fetchall()
    if(query_response == []):
        return "This trend does not have any songs associated with it."
    return query_response

def change_trend_for_song(trendname, songname):
    conn = db.connect()
    query_1 = "SELECT song_id from Songs WHERE name LIKE \"" + songname + "\" ;"
    query_response1 = conn.execute(query_1).fetchall()
    if query_response1 == []:
        conn.close()
        return "Error: Song does not exist in database."
    song_id = query_response1[0][0]
    
    query_2 = "SELECT * from SongTrends WHERE song_id LIKE \"" + str(song_id) + "\" ;"
    query_response2 = conn.execute(query_2).fetchall()
    # print("2", query_2)
    if query_response2 == []:
        conn.close()
        return "Error: Song does not already have a trend associated with it."
        
    

    query_3 = "UPDATE SongTrends SET trend_name = \"" + str(trendname) + "\" WHERE song_id LIKE \"" + str(song_id) + "\" ;"
    # print(query_3)
    query_response2 = conn.execute(query_3)
    conn.close()
    return "Successfully updated."
    

def get_popular_songs(numresults):
    conn = db.connect()
    query = """SELECT name, artist, release_year  
        FROM Songs NATURAL JOIN (SELECT song_id, COUNT(*) AS numplaylists  
        FROM PlaylistSongs 
        GROUP BY song_id 
        HAVING numplaylists = 2) AS temp LIMIT """+numresults+";" 
    query_results =conn.execute(query).fetchall()
    conn.close()
    # parsed_results = []
    # for result in query_results:
    return (query_results)

def stored_procedure_artist_trends(artist_year):
    #############STORED PROCEDURE#########################
    connection = db.raw_connection()
    try:
        cursor = connection.cursor()
        cursor.callproc("ArtistTrends", [2010])
        results = list(cursor.fetchall())
        cursor.close()
        connection.commit()
    finally:
        connection.close()

    return results