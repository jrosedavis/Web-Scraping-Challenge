from flask import Flask
from flask import render_template, redirect
import pymongo
import scrape_mars

app=Flask(__name__)

mongo_conn='mongodb://localhost:27017'
client=pymongo.MongoClient(mongo_conn)

#Home route into MongoDB
@app.route('/')
def index():
    planet_mars = client.mars_db.mars.find()
    return render_template('index.html', planet_mars=planet_mars)

#Scrape route
@app.route('/scrape')
def scrape():
    mars = client.mars_db.mars
    mars_info = scrape_mars.scrape_all()
    mars.update({}, mars_info, upsert=True)
    return 'Scraping Complete'


if __name__ == "__main__":
    app.run(debug=True)