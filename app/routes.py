# Authors: 
# CS For Insight 
# (Summer19 - JG)

try:
    from flask import render_template, redirect, url_for, request, send_from_directory, flash
    from app import app
    import os, re, json, time
    from werkzeug.utils import secure_filename
    # from werkzeug.datastructures import FileStorage
except:
    print("Not able to import all of the calls needed from the Flask library.")


# The "empty" home page and /index both render ... the index.html template
@app.route('/index')
@app.route('/')
def index():
    """ this Python functions returns a string! """
    s = render_template('index.html', title='Home')  # see templates/index.html for this!
    return s


# Flask simply handles the traffic of strings from place to place!
@app.route('/simple')
def simple():
    """ returns a simple string """
    s = "Hi there, from Flask's Python function, simple() ..."
    return s


# Flask simply handles the traffic of strings from place to place!
@app.route('/simplehtml')
def simplehtml():
    """ the string can be html... """
    s = """
<html>
<head>
</head>
<body>
<h1>Hi there!</h1>
<p>I'm in HTML...</p>
<p style="font-size:84px;">Emojis at 84 point: <br>  😀 ☕ </p>
</body>
</html>
"""
    return s
    

# Flask simply handles the traffic of strings from place to place!
@app.route('/simplejson')
def simplejson():
    """ the string can be json... """
    d = {"key":"value", "answer":42}
    s = json.dumps(d)   # converts dictionary d to a string s
    return s     # try grabbing this json data -- using requests!


@app.route('/timestamp')
def seconds_since_1970():
    """ returns a json structure with two key-value pairs:
            'seconds': <the floating-point # of seconds since 1/1/1970>
            'origin': '1/1/1970'
    """
    elapsed_seconds = time.time()  # built-in, counts seconds since 1970
    d = { 'seconds': elapsed_seconds, 
          'origin' : '1/1/1970' }
    s = json.dumps(d)  # using the json library to "dump" a string
    return s    # try grabbing this json data -- using requests!


#
# substitution Python function!
#
# This is the only function in which changes are needed!
#
def substitute(old_text, substitutions):
    new_text=old_text
    """ our substitution engine:
        old_text: the body of text in which to make substitutions
        dictionary_of_substitutions:
          a Python dictionary with
            keys ~ the strings to replace (get rid of)
            values ~ the strings to replace the keys with! 
            
        return value, nex_text: the new text, with substitutions made!
        This is the function to change, to create xkcd-type substitutions!
    """
    for i in old_text.split():
        if i in substitutions.keys():
            new_text = new_text.replace(i, substitutions[i])
        else:
            pass
    return new_text    # return the result



# Substitutions page, when we click submit, it calls the above function...
@app.route('/subs',methods=['GET','POST'])
def subs():
    """ handles the substitutions! """
    if request.method != 'POST':
        return render_template('subs.html', title='Home')

    if request.method == 'POST':
        # larger textarea
        old_textarea = request.form['textarea_input']
        # old words and new words (their replacements)
        old_word1 = request.form['original_text1']
        old_word2 = request.form['original_text2']
        old_word3 = request.form['original_text3']
        new_word1 = request.form['replacement_text1']
        new_word2 = request.form['replacement_text2']
        new_word3 = request.form['replacement_text3']
        # create a dictionary of substitutions
        substitutions = {}
        substitutions[old_word1] = new_word1
        substitutions[old_word2] = new_word2
        substitutions[old_word3] = new_word3
        # do the transformation in Python
        new_text = substitute(old_textarea, substitutions)
        return render_template('subsResults.html', 
                                old_text=old_textarea, 
                                new_text=new_text)


def choose_me(cost_chosen, cuisine_chosen, tag_chosen):
    import pandas as pd
    import numpy as np

    restaurants = pd.read_csv('Claremont_DB1.csv')

    #print("What cost range would you like to search for?")
    cost_chosen=input()

    #print("What type of cuisine would you like to search for?")
    cuisine_chosen=input()

    #print("What tags would you like to search for?")
    tag_chosen=input()

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
    choice=clean3.sample(n=1) # get a random restaurant from the clean3 dataframe
    final_restaurant=choice['Name'].values[0] # get the name of the restaurant
    return final_restaurant


@app.route('/selector',methods=['GET','POST'])
def selector():
    if request.method != 'POST':
        return render_template('subs.html', title='Home')

    if request.method == 'POST':
        old_textarea = request.form['textarea_input']
        cost_chosen = request.form['original_text1']
        cuisine_chosen = request.form['original_text2']
        tag_chosen = request.form['original_text3']
        new_text = choose_me(cost_chosen, cuisine_chosen, tag_chosen)
        return render_template('subsResults.html', 
                                final_restaurant=final_restaurant)

