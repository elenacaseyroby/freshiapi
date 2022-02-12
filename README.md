# Freshi API

## Tooling
* install git and connect to your github account: https://docs.github.com/en/github/getting-started-with-github/set-up-git#setting-up-git
* install github desktop: https://desktop.github.com/
* install homebrew: https://docs.brew.sh/Installation
* install xcode & command line tools if they aren't already on your mac
* install python3: `brew install python3`
* Since for later versions of python, certificates are not pre installed we will need to install them ourselves.  To do this open Applications/Python 3.7 and double click "Install Certificates.command".  This will run the necessary scripts.  If the "Install Certificates.command" file does not exist, read this: stackoverflow.com/a/44649450/412896 
* install node in /usr/local/bin: https://nodejs.org/en/

## Local Environment Set Up
1. download repo
3. change directories into repo: `cd ~/freshi`
4. get .env file from Casey and store it in the outer freshi directory
5. connect to db: connect to live db in aws. export database. create local database and import data.  add local database credentials to .env file.
7. create virtual environment: `python3 -m venv env`
8. start virtual env: `source env/bin/activate`
9. install django dependencies: `pip install -r requirements.txt`
10. start backend server: `python3 manage.py runserver`
11. change directories to frontend: `cd frontend`
12. install node dependencies: `npm install`
13. start frontend server: `npm start`

## Making changes to the code
1. change directories into repo: `cd ~/freshi`
2. make sure you are on the main branch: `git checkout main`
3. update your main branch from the remote repository on github so it's up to date: `git pull origin main`
4. make a new branch and check it out (make the name descriptive): `git checkout -b my-feature-name`
5. make a change to the code & save
6. check the change was tracked by git: `git status`
7. add all tracked changes: `git add .`
8. commit (save) the changes to the branch and a message describing the changes: `git commit -m "feature now does x differently"
9. push changes to your remote branch in github for review: `git push origin my-feature-name`
10. changes will be reviewed and merged into the main branch in github

## Deploying changes to the code
1. change directories into repo: `cd ~/freshi`
2. make sure you are on the main branch: `git checkout main`
3. update your main branch from the remote repository on github so it's up to date: `git pull origin main`
4. push back to main: `git push origin main`
5. now that github is up to date, we can deploy to staging: `eb deploy freshi-staging`
6. check that everything's working
7. deploy to production: `eb deploy freshi-prod`

## Running Tests
...add later... 

## Staging 
...add later... 

## Production
...add later... 

## Syncing foods and nutrition facts from USDA FoodData Central
1. Make sure nutrients, nutrients_usdanutrients, units, unit_conversions are all filled in the db already.
2. Add the following FoodData Central csvs to our Amazon S3 bucket freshi-app/food-sync-csvs: food.csv, nutrient.csv, food_nutrient.csv, food_portion.csv, market_acquisition.csv, food_category.csv 
3. Run this management command in your virtual env: `python manage.py sync_foods_from_usda`
