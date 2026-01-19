import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key form the enviornment
gemini_api_key = os.getenv('TestProject2')

# Lets configure the model
model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key
)

# Design the  UI of application
st.title(":orange[Healthify:] :blue[Your Personal Health Assistant]")
st.markdown('''
            This application will assist you to get better and customized Health advice.
            You can ask your health related issues and get the personalized guidance.''' )
Tips = '''
Follow These Steps:
* Enter your details in sidebar
* Rate your activity and fitness on the scale of 0-5
* Submit your details.
* Ask your question on the main page.
* Click on Generate and Relax.'''

# Design the sidebar for all the user parameters
st.sidebar.header(':red[ENTER YOUR DETAILS]')
Name = st.sidebar.text_input('Enter your Name')
Gender = st.sidebar.selectbox('Select your gender',['Male','Female','Other'])
Age = st.sidebar.text_input('Enter your Age')
Weight = st.sidebar.text_input('Enter your Weight in Kgs')
Height = st.sidebar.text_input('Enter your Height in cms')
BMI = pd.to_numeric(Weight)/((pd.to_numeric(Height)/100)**2)
Active = st.sidebar.slider('Rate your Activity (0-5)',0,5,step=1)
Fitness = st.sidebar.slider('Rate your Fitness (0-5)',0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{Name}, Your BMI is: {BMI:.2f}Kg/m^2")

# Lets use the gemini model to generate the report 
user_input = st.text_input('Ask Anything:')
prompt = '''
<Role> You are an expert in Health and Wellness and has 20+ years experience in Guiding people.
<Goal> Generate the customized report addressing the problem the user has asked. Here is the question that
user has asked: {user_input}
<Context> Here are the details that the user has provided.
Name={Name}
Age={Age}
Height={Height}
Weight={Weight}
Gender={Gender}
BMI={BMI}
Activity Rating (0-5)={Active}
Fitness Rating (0-5)={Fitness}

</context>
<format> Start with the greeting using user's name, then provide a detailed and structured health advice report by first identifying the problem,
identifying the root cause of the problem and remedies. Mention the doctor from which specialization can be visited if required.
Mention any change in the diet plan which is required. Use bullet points or numbered lists where appropriate for clarity.
Go step by step so that it is completely clear. In last create a final summary of all the things that has been discussed.
Conclude with motivational tips to encourage a healthy lifestyle. 
</format>
<Instructions> Strictly do not advice any medicines. If the problem seems serious,
 always recommend consulting a healthcare professional for accurate diagnosis 
 and treatment.</format>

 '''


if st.button('Generate'):
    response = model.invoke(prompt)
    st.write(response.content)
