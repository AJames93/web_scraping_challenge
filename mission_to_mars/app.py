from flask import Flask, render_template, redirect
import pymongo
import mars_scrape

#PyMongo to connect
client = pymongo.MongoClient('mongodb://localhost:27017')
db = client.mars_db
collection = db.mars
#Flask
app = Flask(__name__)

# Route to render index.html template using data from Mongo
@app.route('/')
def home():
	mars = collection.find_one()
	return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
	scrape_mars.scrape()
	return redirect('/', code = 302)


if __name__ == "__main__":
    app.run(debug=True)