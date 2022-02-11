import gensim
from gensim.models import Word2Vec  # generate word vectors using Word2Vec
from gensim.models.fasttext import FastText
from gensim.models import KeyedVectors

import csv

from spellchecker import SpellChecker #Correct typos comparing to stackoverflow tags
spell = SpellChecker(language=None, case_sensitive=True)    # To don't consider the default dictionary         

# Import custom dictionary
spell.word_frequency.load_dictionary('/Users/alejandro/Kwykli_GmbH/Projects/Word_Similarity_ADN/custom_dictionary_stackoverflow_tags.gz')
    

from flask import Flask, request, redirect, render_template, session


# ===========  Web Application - Skills Survey ============

app = Flask(__name__)

# -- Load NN Models --
load_model_FT = FastText.load('/Users/alejandro/Kwykli_GmbH/Projects/Word_Similarity_ADN/FasText_10k.model')   
load_model_W2V = Word2Vec.load('/Users/alejandro/Kwykli_GmbH/Projects/Word_Similarity_ADN/word2vec_10k.model')
load_model_GloVe = KeyedVectors.load('/Users/alejandro/Kwykli_GmbH/Projects/Word_Similarity_ADN/GloVe_Nicolas.model')


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Redirect from default URL to /test
@app.route("/", methods=["GET"])
def get_index():
    return redirect("/test")


# @app.route('/test', methods=["POST"])
# def my_intro():
#     return render_template('intro_form.html')

@app.route('/test')
def my_form():
    return render_template('my_form.html')



@app.route('/test', methods=['POST'])
#@app.route('/test', methods=["GET","POST"])
def my_form_post():   
       
    # Create session to identify unique user and its answers
    session['name'] = request.form['name-input']
    session['skill'] = request.form['skill-input']
    
    # Correct possible typos based on stackoverflow tags
    skill_spelling=spell.correction(session['skill'])
    
    
    skill_new = request.form.get('skill-input') #request.form['skill-input']
    #if skill == None:  #or session['skill'] == None:
    if skill_new is None:    
        return render_template('error.html', message="You need to input some skill (e.g., java, fortran) ")
        
    else: 
        
        # -- FastText Model--
        wv_ft = load_model_FT.wv
        
           
        # ---- Get most similar skills (only names) ----
        # FastText
        sim=[item[0] for item in wv_ft.most_similar(skill_spelling, topn=5)]
        sim_skills_ft = ", ".join(sim) #char string   
        
        # Word2Vect
        sim=[item[0] for item in load_model_W2V.wv.most_similar(skill_spelling, topn=5)]
        #sim=[item[0] for item in load_model_W2V.wv.most_similar(session['skill'], topn=5)]
        sim_skills_w2v = ", ".join(sim) #char string  
        
        # GloVe
        sim=[item[0] for item in load_model_GloVe.most_similar(skill_spelling, topn=5)]
        sim_skills_gve = ", ".join(sim) #char string
    
        return render_template('my_form2.html', skill_var_ft=sim_skills_ft, skill_var_w2v=sim_skills_w2v, skill_var_gve=sim_skills_gve, Name_user=session['name'], input_skill=session['skill'])
        #return render_template('my_form2.html', message=message, skill_var_ft=sim_skills_ft, skill_var_w2v=sim_skills_w2v, skill_var_gve=sim_skills_gve, Name_user=session['name'], input_skill=session['skill'])




@app.route('/submitForm', methods=['POST'])
# @app.route('/submitForm', methods=['GET','POST'])
def form_confirmation():

       # Get ratings for each model    
       # session['satisfaction'] = request.form['answer-satisfaction']
       session['rating_A'] = request.form['rating_A']
       session['rating_B'] = request.form['rating_B']
       session['rating_C'] = request.form['rating_C']
       
       # # Save it in a CSV file
       # csvF = open("survey_skills.csv", "a")
       # writer = csv.writer(csvF)
       # writer.writerow([name, skill, satisfaction])
       # csvF.close()

   # return tableAppend("success")   
       return render_template('my_form3.html')



@app.route('/remarks', methods=['POST'])
def remarks_submit():
    
    remarks = request.form.get('comments')
    
    # Get name, skill and rates from session (cookies) 
    name =  session['name']
    skill =  session['skill']
    rate_ModelA =  session['rating_A']
    rate_ModelB =  session['rating_B']
    rate_ModelC =  session['rating_C']

    # ## if remarks !='null'
    if remarks is not None:
        
    # Save it in a CSV file
        csvF = open("survey_skills.csv", "a")
        writer = csv.writer(csvF)
        writer.writerow([name, skill, rate_ModelA, rate_ModelB, rate_ModelC, remarks])
        csvF.close()
    
    else:
        # Save it in a CSV file
        csvF = open("survey_skills.csv", "a")
        writer = csv.writer(csvF)
        writer.writerow([name, skill, rate_ModelA, rate_ModelB, rate_ModelC])
        csvF.close()       
       
    return render_template('my_form4.html')
       
 
    