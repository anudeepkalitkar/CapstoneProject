# CapstoneProject
Note: train before predict
Run docker-compose up 
     open 0.0.0.0:80 for main app
     open 0.0.0.0.81 for swagger UI
To run the project without docker:
step 1: run the following commands in terminal
     cd Webapi
     pip install -r requirements.txt
     run main.py
step 2: open localhost:5000 in browser and train the model
step 3: run the following commands on another terminal
    cd webapp
    npm install
    npm start
step 4: open 192.168.0.1:5000 for the UI

#Capstone milestones
  milestone1 - Consumer and Producer folders
  milestone2 - model folder along with milestone1
  milestone3 - Webapi folder along with mileston2
  milestone4 - Complete zip file
