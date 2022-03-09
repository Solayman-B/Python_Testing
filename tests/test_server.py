from source import loadClubs, loadCompetitions


def test_should_import_list_of_clubs():
	clubs = loadClubs()
	assert clubs[0]['email']== 'john@simplylift.co'

def test_should_import_list_of_competitions():
	competitions = loadCompetitions()
	assert competitions[0]['name']== "Spring Festival"

def test_valid_email(client):
	response = client.post("/showSummary", data={'email':'john@simplylift.co'})
	data = response.data.decode()
	assert "Logout" in data

def test_invalid_email(client):
	response = client.post("/showSummary", data={'email':'wrong@simplylift.co'})
	data = response.data.decode()
	assert "Welcome to the GUDLFT Registration Portal!" in data

def test_enought_points_to_purchase(client, competitions_data, clubs_data):
	response = client.post("/purchasePlaces", data={
		"competition":"Spring Festival",
		"club":"Simply Lift",
		"places":"15",
													})
	data = response.data.decode()
	assert "You don&#39;t have enough points to purchase this amount of places !" in data