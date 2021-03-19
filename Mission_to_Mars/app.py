from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app=Flask(__name__)

mongo_conn='mongodb://localhost:27017'
client=pymongo.MongoClient(mongo_conn)

#Home route into MongoDB
@app.route('/')
def index():
    planet_mars = client.mars_db.mars.find()
    if planet_mars:
        return render_template('index.html', data_from_flask=planet_mars)
    else:
        return 'Data not found'

#Scrape route
@app.route('/scrape')
def scrape():
    mars_data = scrape_mars.scrape_info()
    print(mars_data)
    client.mars_db.mars.update({}, mars_data, upsert=True)
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)