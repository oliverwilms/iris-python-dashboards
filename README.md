# IRIS-python-dashboards

This app shows data visualization. For example, Covid19 data was used. The Dash framework used to build Dashboards is a Python framework created by plotly for building interactive web applications. Dash is open source and building an application using this framework is viewed in a web browser.

## Installation

### Docker
The repo is dockerised so you can  clone/git pull the repo into any local directory

```
$ git clone https://github.com/NjekTt/iris-python-dashboards.git
```

Open the terminal in this directory and run:

```
$ docker-compose up -d
```

## App

After installation open http://localhost:8080/

The main page will show the first dashboard, which visualizes Covid data taken from the local IRIS database

On the left is the navigation menu.

- Overview - shows the general dashboard
- Timeline - a map is shown, there is a player at the bottom of the map, timeline shows the dynamics of data on the world map
- IRIS python usage - guide how python embedded was used, how data was retrieved from the IRIS database and a small example of using the IRIS Native API for Python

# Screencast

## Overview

![image](https://user-images.githubusercontent.com/47400570/154855794-b573bc8a-5078-402c-aac9-e3adb55bb5a7.png)

## Timeline

![image](https://user-images.githubusercontent.com/47400570/154858243-fb1e714d-b18d-4245-a52b-aa0e7b660c50.png)

## IRIS python usage

![image](https://user-images.githubusercontent.com/47400570/154858265-665dfe69-2742-4e8b-852c-0fc9af121040.png)

