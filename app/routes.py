try:
    from flask import render_template, redirect, url_for, request, send_from_directory, flash
    from app import app
    import os, re, json, time
    from werkzeug.utils import secure_filename
    # from werkzeug.datastructures import FileStorage
except:
    print("Not able to import all of the calls needed from the Flask library.")


@app.route('/index')
@app.route('/')
def index():
    """ this Python functions returns a string! """
    s = render_template('index.html', title='Home')  # see templates/index.html for this!
    return s



@app.route('/simple')
def simple():
    """ returns a simple string """
    s = "Hi there, from Flask's Python function, simple() ..."
    return s


def choose_me2(cost_chosen, cuisine_chosen, tag_chosen):
    #Core function that reads in the csv and narrows based on user input
    import pandas as pd
    import numpy as np
    
    restaurants = pd.read_csv('Claremont_DB1.csv')

    if cost_chosen=="Any":
        clean1=restaurants
    else:
        clean1 = restaurants.loc[restaurants['Cost']==cost_chosen] # 
    if cuisine_chosen=="Any":
        clean2=clean1
    else:
          clean2 = clean1.loc[(clean1["Style 1"]==cuisine_chosen) |(clean1["Style 2"]==cuisine_chosen) |(clean1["Style 3"]==cuisine_chosen)]
    if tag_chosen=="Any":
        clean3=clean2
    else:
        clean3 = clean2.loc[clean2['Particularly Good For']==tag_chosen] # get all restaurants with the chosen good for
    if clean3.empty:
        return "There is no restaurant like that", "https://cdn130.picsart.com/320648120422211.png"
    else: 
        choice=clean3.sample(n=1) # get a random restaurant from the clean3 dataframe
        final_restaurant=choice['Name'].values[0] # get the name of the restaurant
        final_link=choice['Link'].values[0]
        return final_restaurant,final_link


@app.route('/selector',methods=['GET','POST'])
def selector():
    if request.method != 'POST':
        return render_template('selector.html', title='Home') 

    if request.method == 'POST':
        cost_chosen = request.form['cost_chosen']
        cuisine_chosen = request.form['cuisine_chosen']
        tag_chosen = request.form['tag_chosen']
        new_text = choose_me2(cost_chosen, cuisine_chosen, tag_chosen)
        return render_template('selector_result.html', 
                                fr_name=new_text[0],
                                fr_link=new_text[1])

