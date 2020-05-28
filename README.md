#Server 

In order to run the backend, which is on server.py, a few installs are required. Most of the dependencies are listed on the pipfile. I will direct how to install and get the server running. Please note the database will be created and stored in the folder containing server.py.

1.) first install pipenv using pip3 install pipenv which will activate the virtual environment and create the Pipfile.
2.)install cors using pip install -U flask-cors
3.) go into the pipenv shell using pipenv shell to activate the virtual environment
4.) Then install the packages using pipenv install flask flask-sqlalchemy
5.) Then within the pipenv shell run python server.py

Note that client assumes the server is running on port 5000