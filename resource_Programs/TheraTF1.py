import os, datetime
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

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

def startProgramDelay():
    print("\nTheraTest File V1 A")

    print("""\nd888888P dP                                   .d888888  dP
    88    88                                  d8'    88  88 
    88    88d888b. .d8888b. 88d888b. .d8888b. 88aaaaa88a 88 
    88    88'  `88 88ooood8 88'  `88 88'  `88 88     88  88 
    88    88    88 88.  ... 88       88.  .88 88     88  88 
    dP    dP    dP `88888P' dP       `88888P8 88     88  dP""")

def geminiConfigure():
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    global model 

    model = genai.GenerativeModel(
        model_name = 'gemini-1.5-flash',
        system_instruction= sysInstructionsFILE.read()
    )
    
def medPromptRun(md):
    md = input("What is the professional summary: ")
    response = model.generate_content(md)
    responseOutputFile.write(response.text)
    responseOutputFile.close()
    print("\n"+ response.text)
    


response_base_path = r'C:\Users\esham\OneDrive\Documents\AI Research TheraAI (24.14.7)\Responses_Output'
base_path = r'C:\Users\esham\OneDrive\Documents\AI Research TheraAI (24.14.7)'
date_time = functionFileCreation(str(datetime.datetime.now()))
nRSYS_instructionPath = "SYS_instructionsR3.7.3.7.txt"
sysInstructionsFILE = open(os.path.join(base_path, nRSYS_instructionPath))
responseOutputFile = open(os.path.join(response_base_path,("response" + date_time +".txt")), "x")
medical_prompt = ""

#new formatting, clean-up-organization 
load_dotenv(find_dotenv())
startProgramDelay()
geminiConfigure()
medPromptRun(medical_prompt)

#from openai import OpenAI


# print("\n"+ os.getenv('OPENAI_API_KEY'))
# print("\n" + os.getenv('GEMINI_API_KEY'))
# print(sysInstructionsFILE.read())







# 7/14/24 issues with environemnt vairables reading (need dotenv suppor)
# major issues with retrieving credits available for the openAI subjects research 
# will need to looks to other solutions of developing posssible reactionable ai system model for MLM, LLM, and NLP completion 

# load_dotenv(find_dotenv())
# print(os.getenv('OPENAI_API_KEY'))

# client = OpenAI(
#     api_key=os.getenv('OPENAI_API_KEY')
# )

# response = client.chat.completions.create(
#   model="gpt-3.5-turbo-0125",
#   response_format={ "type": "json_object" },
#   messages=[
#     {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
#     {"role": "user", "content": "Who won the world series in 2020?"}
#   ]
# )

# print(response.choices[0].message.content)
