import gensim
from gensim.models import Word2Vec  # generate word vectors using Word2Vec
from gensim.models.fasttext import FastText
import csv

from flask import Flask, request, redirect, render_template, session
# from flask import Flask, jsonify, redirect, render_template, request


# ===========  Web Application - Skills Survey ============

app = Flask(__name__)

# -- Load NN Models --
loaded_model = FastText.load('/Users/alejandro/Kwykli_GmbH/Projects/Word_Similarity_ADN/FasText_10k.model')   



app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Redirect from default URL to /test
@app.route("/", methods=["GET"])
def get_index():
    return redirect("/test")


@app.route('/test')
def my_form():
    return render_template('my_form.html')


#--Define ~ global variables/lists
#name_list = []
#skill_list = []

@app.route('/test', methods=['POST'])
#@app.route('/test', methods=["GET","POST"])
def my_form_post():   
    
    # Get name and skill from the form
    #name = request.form.get('name-input')
    #processed_text = request.form['skill-input']
    # name_list.append(name)
    # skill_list.append(processed_text)
    
    session['name'] = request.form['name-input']
    session['skill'] = request.form['skill-input']
    
    
    
    # -- FastText Model--
    wv_ft = loaded_model.wv
           
    # Get most similar skills (only names)
    sim=[item[0] for item in wv_ft.most_similar(session['skill'], topn=5)]
    sim_skills = ", ".join(sim) #char string   
     
   # return render_template('my_form2.html', skill_var=sim_skills, Name_user=name, input_skill=processed_text)
    return render_template('my_form2.html', skill_var=sim_skills, Name_user=session['name'], input_skill=session['skill'])



@app.route('/submitForm', methods=['POST'])
# @app.route('/submitForm', methods=['GET','POST'])
def form_confirmation():
    
       # Get name and skill from global variables
       # name = name_list.pop()
       # skill = skill_list.pop()
       
       name =  session['name']
       skill =  session['skill']

       satisfaction = request.form.get('answer-satisfaction') #From the form

       # Save it in a CSV file
       csvF = open("survey_skills.csv", "a")
       writer = csv.writer(csvF)
       writer.writerow([name, skill, satisfaction])
       csvF.close()

   # return tableAppend("success")   
       return render_template('my_form3.html')

