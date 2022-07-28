try:
    from flask import render_template, request
    from app import app
    import os
except:
    print("Not able to import all of the calls needed from the Flask library.")

basedir = os.path.abspath(os.path.dirname(__file__))


def choose_me(cost_chosen, cuisine_chosen, tag_chosen):
    # Core function that reads in the csv and narrows based on user input
    import pandas as pd
    import numpy as np

    restaurants = pd.read_csv(os.path.join(basedir, 'Claremont_DB1.csv'))

    if cost_chosen == "Any":
        clean1 = restaurants
    else:
        clean1 = restaurants.loc[restaurants['Cost'] == cost_chosen]  #
    if cuisine_chosen == "Any":
        clean2 = clean1
    else:
        clean2 = clean1.loc[(clean1["Style 1"] == cuisine_chosen) | (clean1["Style 2"] == cuisine_chosen) | (
                    clean1["Style 3"] == cuisine_chosen)]
    if tag_chosen == "Any":
        clean3 = clean2
    else:
        clean3 = clean2.loc[
            clean2['Particularly Good For'] == tag_chosen]  # get all restaurants with the chosen good for
    if clean3.empty:
        return "There is no restaurant like that", "https://cdn130.picsart.com/320648120422211.png"
    else:
        choice = clean3.sample(n=1)  # get a random restaurant from the clean3 dataframe
        final_restaurant = choice['Name'].values[0]  # get the name of the restaurant
        final_link = choice['Link'].values[0]
        return final_restaurant, final_link


@app.route('/', methods=['GET', 'POST'])
def selector():
    # python function that takes in variables from index.html, feeds them into the core function,
    # then renders the selector_result page
    if request.method != 'POST':
        return render_template('index.html', title='Home')

    if request.method == 'POST':
        cost_chosen = request.form['cost_chosen']
        cuisine_chosen = request.form['cuisine_chosen']
        tag_chosen = request.form['tag_chosen']
        new_text = choose_me(cost_chosen, cuisine_chosen, tag_chosen)
        return render_template('selector_result.html',
                               fr_name=new_text[0],
                               fr_link=new_text[1])
