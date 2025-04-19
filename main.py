import mysql.connector as sql
from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

db = sql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="musicdbms")
pointer = db.cursor(dictionary=True)

@app.route("/", methods=['POST','GET'])
def home():
    global db, pointer
    if request.method == 'POST':
        title= request.form["searchtitle"]
        query=f"SELECT * FROM allsongs WHERE title LIKE '{title}%'"
        pointer.execute(query)
        songs=pointer.fetchall()
        return render_template("index.html", songs=songs)
    else:
        query=f'SELECT * FROM allsongs;'
        pointer.execute(query)
        songs=pointer.fetchall()
        return render_template("index.html", songs=songs)

@app.route("/artist/<artst>")
def showartist(artst):
    global db, pointer
    query=f"SELECT * FROM allsongs WHERE artist LIKE '{artst}%';"
    pointer.execute(query)
    songs=pointer.fetchall()
    return render_template("artist.html", songs=songs, artst=artst)

@app.route("/album/<albm>")
def showalbum(albm):
    global db, pointer
    query=f"SELECT * FROM allsongs WHERE album='{albm}';"
    pointer.execute(query)
    songs=pointer.fetchall()
    return render_template("album.html", songs=songs, albm=albm)

@app.route("/custom")
def showcustom():
    global db, pointer
    query=f"SELECT * FROM custom;" 
    pointer.execute(query)
    songs=pointer.fetchall()
    return render_template("custom.html", songs=songs)

@app.route("/custom/add", methods=['POST', 'GET'])
def addcustom():
    global db, pointer
    if request.method == 'POST':
        trackid=request.form["trackid"]
        query=f"INSERT INTO CUSTOM SELECT * FROM ALLSONGS where trackID={trackid};"
        pointer.execute(query)
        db.commit()
        return render_template("addsongs.html")
    else: 
        return render_template("addsongs.html")


@app.route("/custom/remove", methods=['POST', 'GET'])
def removecustom():
    global db, pointer
    if request.method == 'POST':
        trackid=request.form["trackid"]
        query=f"DELETE FROM CUSTOM WHERE trackid={trackid};"
        pointer.execute(query)
        db.commit()
        return render_template("removesongs.html")
    else: 
        return render_template("removesongs.html")

if __name__== "__main__":
    app.run(debug=True, use_reloader=False)
