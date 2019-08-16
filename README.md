# COMP47360 Research Practicum - Predicting Dublin Bus Journey Times

## Prerequisites

### Git
Used to clone the repository and navigate its branches.

### Anaconda
Anaconda is a Python distibution used to create virtual environments and will be used to both create and manage virtual environments and install some Python libraries.

### Pip
Pip is a package management system for installing python software packages and will be used to install the necessary Python libraries for running the application.

### Nodejs
Nodejs is a Javascript run-time environment used to execute Javascript outside of a browser and will be used to install, build and provide test runs of the React application.

### Redis
Redis is an in-memory data store used as a cache in the application.

### MySQL
MySQL is a relational database management system used to store the data which drives the application.

## Installation

1. Clone the git repository, master is the stable branch and is immutable.

        git clone https://github.com/johnmcl001/DublinBusProject.git

2. Change into the DublinBusProject directory

        cd DublinBusProject

3. (Optional) Create a virtual environment using conda.

        conda create -n DublinBus python=3.7

4. (Optional) Activate the environment created in the previous step.

        conda activate DublinBus

5. Install the required python libraries using pip.

        pip install -r requirements

6. Install mysqlclient with conda.

        conda install mysqlclient

7. Change into the frontend directory.

        cd DublinBus/frontend

8. Install the required node packages.

        npm install

9. Install npx.

        npm install npx

## Running the Application

1. Start the Django backend.

        cd ~/DublinBusProject/DublinBus
        python manage.py runserver

2. Start the redis server.

        redis-server

3. Start the MySQL database.

        sudo systemctl start mysql

4. Start a development build of the React frontend.

        cd ~/DublinBusProject/DublinBus/frontend
        npm run dev

5. Navigate to localhost:1234 in a browser.

5. (Optional) Make a production build of the React frontend.

        cd ~/DublinBusProject/DublinBus/frontend
        npm run build

6. (Optional) Start a production build of the React frontend.

        cd ~/DublinBusProject/DublinBus/frontend
        npm run start

7. (Optional) Navigate to localhost:5000 in a browser






