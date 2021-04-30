from flask import render_template, request, jsonify
from app import app
from app import database as db_helper

@app.route("/", methods=['GET'])
def homepage():
    trendlist = db_helper.get_trends()
    songlist = db_helper.get_songs_without_trends()

    return render_template("index.html", trend_list = trendlist, song_list=songlist)

@app.route("/create", methods=['POST'])
def create():
    data = request.get_json()
    trendname = request.form['trendname']
    songname = request.form['songname']
    # conn = db.connect()
    result = db_helper.insert_new_trend(trendname, songname)
    return "<p>" + str(result) + "</p>"


@app.route("/search", methods=['GET'])
def search():

    trendname = request.args.get('trendname2')
    result = db_helper.get_songs_for_trend(trendname)
    return "<p>" + str(result) + "</p>"



@app.route("/update", methods=['POST'])
def update():
    data = request.get_json()

    trendname = request.form['newtrendname']
    songname = request.form['songname3']
    result = db_helper.change_trend_for_song(trendname, songname)
    return "<p>" + str(result) + "</p>"


@app.route("/delete", methods=['POST'])
def delete():
    songname = request.form['songname5']
    result = db_helper.delete_song_from_trend(songname)
    return "<p>" + str(result) + "</p>"

@app.route("/special", methods=['GET'])
def special():
    songslist = db_helper.get_popular_songs(request.args.get('numresults'))
    result = {'success': True, 'response': 'Done'}
    return render_template("songslist.html", songlist = songslist)


@app.route("/artisttrends", methods=['GET'])
def artisttrends():
    result = db_helper.stored_procedure_artist_trends(request.args.get('year_artist_trend'))
    
    return render_template("artisttrendslist.html", artisttrendslist=result)
    