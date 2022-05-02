# Birdmetrics
Birdmetrics is a web application that lets you upload sales data of your company in a CSV format and access certain KPIs and their graphs instantly!

## How to set the project up locally
* Make sure Python 3 is installed on your system
* Clone the repo to your local system
* Add the .env file to the root repository (.../birdmetrics/.env)
* Run the following command to install the dependencies:
`pip install -r requirements.txt`
* Run the following command to set up a development server and run the application:
`python3 run.py`

Go to http://127.0.0.1:5000 in your browser to view and use the app.

## Architecture diagram
![image](https://user-images.githubusercontent.com/93583929/166246620-b996350e-146c-452b-8a33-3d4160c484bd.png)
[Architecture Diagram](https://docs.google.com/drawings/d/e/2PACX-1vRewiKSRx-gMMW6vNoAsi-eUFvRMFTWHceR-GTnvpXS2mQ7tSpvehfgk3pTEy2K2smc32Goaw0B54gP/pub?w=1009&h=456)

## How to use the app
* Register for an account
* Use the same credentials to log into the app
* Click the "Upload" button on the navigation bar
* Select a CSV file that **matches the presented criteria**, press upload file
* Click "Okay" to be redirected to the homepage
* You can now explore different tabs to inspect different metrics and view the "Cohort Retention Heatmap"

View the app live @ birdmetrics.herokuapp.com

### Disclaimer 1: The Plotly interactive graphs take some time to load, make sure to give it some time if you're viewing the app hosted on Heroku :)
### Disclaimer 2: You can use the template provided on the upload page to test the app.
