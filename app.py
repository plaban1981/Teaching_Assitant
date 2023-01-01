import streamlit as st
from PIL import Image
import os
import openai
from random import choice
from dotenv import load_dotenv
#from aiassitant import ask


load_dotenv()
openai.api_key = os.getenv("API_KEY")
#Inject Start Tex
start_sequence = "\nAI:"
#Inject Restart Text
restart_sequence = "\nHuman: "

#
@st.cache
def ask(question, chat_log=None):
   #prompt_text = f'{chat_log}{restart_sequence}:{question}{start_sequence}:' 
   if chat_log is None:
      p_text = "Hello I am your AI powered Teaching Assistant bot.\nHuman: Hey, how are you doing?\nAI: I'm good! What would you like to chat about?"
      prompt_text = f'{start_sequence}{p_text}{restart_sequence}{question}'
       
   else:
      prompt_text = f'{chat_log}{restart_sequence}:{question}{start_sequence}:' 
   print(prompt_text)
   response = openai.Completion.create(
               model="text-davinci-003",
               prompt=prompt_text,
               temperature=0.7,
               max_tokens=512,
               top_p=1,
               frequency_penalty=0,
               presence_penalty=0
               )

   answer = response.choices[0].text
   new_prompt = prompt_text + start_sequence + answer + restart_sequence
   return answer, new_prompt

#
image_path = "chatbots_python.jpg"
image = Image.open(image_path)


st.set_page_config(page_title="AI Teaching Assistant Bot", layout="centered")
st.image(image, caption='Teaching Assitant Bot', use_column_width=True)
# page header
st.title(f"Teaching Assitant Bot")
with st.form("Prediction_form"):
   text = st.text_input("Enter your question:")
   #st.title(text)
   #
   # Create a list of options for the drop-down menu
   options = ['y', 'n']
   # Create the drop-down menu
   selected_option = st.sidebar.selectbox('Select an option:', options)
   # Display the selected option
   st.write(f'You selected: {selected_option}')
    
   #
   submit = st.form_submit_button("Converse with the bot")
   #
   if submit:
        chat_log = None
        print(selected_option)
        if selected_option == "y":
           response,chat_log = ask(text,chat_log)
           print(response)
        else:
            response = "Thank You."
        #choice = input("Do you want to continue (y/n): ") 
        #print(result)
        # output header
        st.header("Response from the bot")
        # output results
        st.markdown(response)