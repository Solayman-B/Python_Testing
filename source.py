import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'
competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("Sorry, that email wasn't found")
        return render_template('index.html')
    else:
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    competitionDate = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
    if foundClub and foundCompetition:
        if competitionDate > datetime.today():
            return render_template('booking.html',club=foundClub, competition=foundCompetition)
        else:
            flash("You can't book places if the competition already started")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    availablePoints = int(club["points"])
    placesRequired = int(request.form['places'])
    if availablePoints < placesRequired:
        flash("You don't have enough points to purchase this amount of places !")
        return render_template('welcome.html', club=club, competitions=competitions)
    elif int(competition['numberOfPlaces'])-placesRequired < 0:
        flash("There isn't enough places left for this competitions !")
        return render_template('welcome.html', club=club, competitions=competitions)
    elif placesRequired > 12:
        flash("You can't purchase more than 12 places !")
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        availablePoints = availablePoints - placesRequired
        flash('Great-booking complete !')
        return render_template('welcome.html', club=club, placesRequired=placesRequired, competitions=competitions, availablePoints=availablePoints)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))