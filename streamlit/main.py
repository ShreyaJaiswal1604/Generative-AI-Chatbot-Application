import streamlit as st
import base64
from dotenv import load_dotenv
load_dotenv()

# Set page title and icon
st.set_page_config(
    page_title="Chatbot Home",
    page_icon="🤖",
    initial_sidebar_state='collapsed'
)

# Main title
st.title("Welcome to Chatbot 🌟")
# Description
st.write("This is a chatbot application designed to assist you with YouTube links and PDF files.")

# Emojis for decoration
st.write(":speech_balloon: :video_camera: :page_facing_up:")

st.image('../images/04-img.jpeg', caption='Let\'s get started', width=500)
# Set background image
def sidebar_bg(side_bg):

   side_bg_ext = 'png'

   st.markdown(
      f"""
      <style>
      [data-testid="stSidebar"] > div:first-child {{
          background: url(data:image/{side_bg_ext};base64,{base64.b64encode(open(side_bg, "rb").read()).decode()});
      }}
      </style>
      """,
      unsafe_allow_html=True,
      )
   
side_bg_ext = '../images/01-img.png'

sidebar_bg(side_bg_ext)



# if(st.button('Let\'s get started')):
#    st.switch_page('pages/1_uploa.py')
