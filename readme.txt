I have used mysql database for my work.
main.py is the only script used. It uses flask framework to render the webpages. Pandas is used for easy handling of data within python.

lines 20-24 have variables related to database stored. They should be modified appropriately before starting the script. Script
    assumes that the mysql server runs at localhost:3306

3 extra python modules are needed to be downloaded for the script. Use the commands:

----------------------------

python3 -m pip install flask
python3 -m pip install pandas
python3 -m pip install sqlalchemy

----------------------------

After installing the modules, run the script from the folder nineleaps with command:

----------------------------

python3 main.py

----------------------------
Then access the html page at : http://localhost:5000
The pretty print page is randomized and gives new result on every refresh.