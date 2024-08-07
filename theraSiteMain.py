
#needed libraries, dependencies, etc
from flask import Flask, render_template,request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
import os, datetime
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
import random
import string
# from reportlab.pdfgen import canvas 


#defining base file paths
response_base_path = r'C:\Users\esham\OneDrive\Documents\TheraSiteFolder\static\Responses_Output'
response_static_path= r'static\Responses_Output'
base_path2= r'C:\Users\esham\OneDrive\Documents\TheraSiteFolder'


#system instructions and file exchange 
nRSYS_instructionPath = "SYS_instructionsR3.7.3.7.txt"
crSYS_instructionPath = "SYS_instructionsCHAT_Revision.txt"
sysInstructionsFILE = open(os.path.join(base_path2, nRSYS_instructionPath))
sysCHAT_InstructionsFILE= open(os.path.join(base_path2, crSYS_instructionPath))
medical_prompt = ""
patient_summary_message = ""


# def response_summary_toPDF(c, res):
#     c.drawString(8.5,0, res)

def generate_random_id(length=30):
  """Generates a random ID of specified length containing letters and numbers."""
  characters = string.ascii_letters + string.digits
  return ''.join(random.choice(characters) for _ in range(length)) 

#declarative list of functions 
def geminiConfigure(sys1, sys2):
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    global report_model1, chat_model2 

    report_model1 = genai.GenerativeModel(
        model_name = 'gemini-1.5-flash',
        system_instruction=sys1.read()
    )
    chat_model2 = genai.GenerativeModel(
        model_name = 'gemini-1.5-flash',
        system_instruction=sys2.read()
    )
    # if(sys == None):
    #     print("hello")
    #     model = genai.GenerativeModel(
    #         model_name = 'gemini-1.5-flash'
    #     )
    # else: 
    #     model = genai.GenerativeModel(
    #         model_name = 'gemini-1.5-flash',
    #         system_instruction= sys.read()
    #     )
        
def functionFileCreation(dtt): 
    for i in range(0, len(dtt), 1):
        if(i == len(dtt)): break
        if(dtt[i] == "-"):
            dtt = dtt[0:i] + dtt[i+1:len(dtt)] 
            i += 1
        if(dtt[i] == ":"):
            dtt =dtt[0:i] + dtt[i+1:len(dtt)]
            i += 1
        if(dtt[i] == " "):
            dtt =dtt[0:i] + "_" + dtt[i+1:len(dtt)]
            i += 1
    
    return dtt

#needed instance functions, and display vairables for working shuffle order 
load_dotenv(find_dotenv())

#configuring model with needed dimension, agent selection, and specification of hyper-parameters, as well as needed, prompt engineering requirements 
#geminiConfigure(sysInstructionsFILE)
def geminiRunEvaluation(rt):
    #function
    # geminiConfigure(None)
    # geminiConfigure(sysInstructionsFILE)
    def medPromptRun(md):
        #md = input("What is the professional summary: ")
        global response
        response = report_model1.generate_content(md)
        responseOutputFile.write(response.text)
        responseOutputFile.close()
        # response_summary_toPDF(sm)
        # sm.showPage()
        # sm.save()
        
    #instance internal variables
    
    global id, response_output_file_path
    date_time = functionFileCreation(str(datetime.datetime.now()))
    id = generate_random_id()
    response_output_file_path = os.path.join(response_static_path, ("response" + id + date_time +".txt"))
    responseOutputFile = open(os.path.join(response_base_path,("response" + id + date_time +".txt")), "x")
    medical_prompt = rt
    
    # sum = canvas.Canvas("response" + date_time + ".pdf")
    
    #final response function
    medPromptRun(medical_prompt)
    return (response.text)

#__________________________________________


#flask python hosting task running 
db = SQLAlchemy()
app = Flask(__name__)

#database_setup
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///main.db"
db.init_app(app)

class Prompt_Answer3(db.Model): 
    prompt: Mapped[str] = mapped_column(unique=False)
    answer: Mapped[str] = mapped_column(primary_key = True)
    
class medicalReport(db.Model):
    id: Mapped[str] = mapped_column(primary_key= True)
    url_to_txt: Mapped[str] = mapped_column(primary_key= True)
    
geminiConfigure(sysInstructionsFILE, sysCHAT_InstructionsFILE)
    
with app.app_context():
    db.create_all()

@app.route('/home')
def home_Page(): 
    return render_template('home.html')

@app.route('/', methods=['POST','GET'])
def main_Page():
    if request.method == 'POST':
        patient_weight = request.form['weight']
        patient_height = request.form['height']
        patient_gender = request.form['gender']
        patient_age = request.form['age']
        patient_symptom_summary = request.form['symptomSummary']
        patient_background = request.form['backgroundInfo']
        
        global patient_summary_message, medical_review_preview
        
        patient_summary_message = patient_weight + "," + patient_height + "," + patient_gender + "," + patient_age+ "," + patient_symptom_summary + ", " + patient_background
        
        
        medical_review_preview = geminiRunEvaluation(patient_summary_message)
        # prompt_Generation = Prompt_Answer3(prompt = patient_summary_message, answer = medical_review_preview)
        # db.session.add(prompt_Generation)
        # db.session.commit()
        # geminiConfigure(sysCHAT_InstructionsFILE)
        
        reportGeneration = medicalReport(id = id, url_to_txt = '' + response_output_file_path + '')
        db.session.add(reportGeneration)
        db.session.commit() 
        return redirect(url_for('chat_Page'))

        
        #geminiRunEvaluation(message)
    return render_template('index.html')

@app.route('/chat', methods=['POST','GET'])
def chat_Page():
    print(medicalReport.query.all())
    # print(geminiRunEvaluation(patient_summary_message))
    global chat, chatUser
    chat = chat_model2.start_chat(history=[])
    chatUser = ""
    # chat_response = chat.send_message(patient_summary_message)
    # print(chat_response.text)
    
    # if request.method == 'POST':
    #     chatUser = request.form['chat_message']
    #     if (chatUser != " " or chatUser != "I am satisfied with my care"):
    #         print(chatUser)
    #         chat_response = chat.send_message(chatUser)
    #         print(chat_response.text)
    
    return render_template('chat.html')

@app.route('/doctor_login', methods=['POST', 'GET'])
def doctor_login(): 
    reports = medicalReport.query.all()
    return render_template('doctor_login.html', reports = reports)

@app.route('/getFirstResponse', methods=['GET', 'POST'])
def get_first_bot_response():
    chat_response1 = chat.send_message(patient_summary_message)
    return (chat_response1.text)

@app.route('/get', methods=['GET', 'POST'])
def get_bot_response(): 
    print("hello")
    chatUser = request.args.get('msg')
    chat_response = chat.send_message(chatUser)
    print(chat_response.text)
    return (chat_response.text)
    
    

if __name__ == '__main__':
    app.run(debug=True)
    

    
    
    
    
    