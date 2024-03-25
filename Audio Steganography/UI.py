import streamlit as st
from streamlit_option_menu import option_menu
from stepic import encode
from eyed3 import load
from stepic import decode
from PIL import Image
import os
from os import system
import base64

# Sidebar menu
with st.sidebar:
    selected = option_menu("Menu", ['Home',"Encode","Decode"], 
        icons=['clipboard-heart-fill', 'chat-right-dots-fill','disc'], menu_icon="cast", default_index=0)

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Home Page Content
if selected == "Home":

    set_background("BGI.png")
    st.title("🔒 Audio Steganography App 🎶")
    st.header("Encrypt your secret messages into audio files! ")

    # Homepage content with styling
    st.markdown(
        """
        <div style='text-align: justify;'>
            This app allows you to perform <strong>audio steganography</strong>, a technique used to hide secret messages within audio files. 
            You can encode your plaintext messages into an image, and then embed that image into an audio file. 
            This makes it possible to transmit sensitive information covertly through audio channels.
        </div>
        """,
        unsafe_allow_html=True
    )

    # How it works section with styling
    st.markdown(
        """
        <div style='text-align: justify; margin-top: 20px;'>
            <h3>How it works:</h3>
            <ol>
                <li>Upload an image (PNG format only) containing your secret message.</li>
                <li>Enter your plaintext message. ✍️</li>
                <li>Click on the <strong>'Encrypt'</strong> button to encode your message into the image.</li>
                <li>Upload an audio file (MP3 format only) to embed the encoded image into it.</li>
                <li>Once uploaded, the app will embed the image into the audio file, creating a new audio file with the hidden message.</li>
                <li>Download the encrypted audio file and share it with the intended recipient.</li>
            </ol>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Use Cases section with styling
    st.markdown(
        """
        <div style='text-align: justify; margin-top: 20px;'>
            <h3>Real Life Use Cases:</h3>
            <ul>
                <li> Secure communication of sensitive information. 🔐</li>
                <li> Covert Operations & data transmission in audio files.📡</li>
                <li> Authentication & Tamper Detection 🕵️‍♀️</li>
                <li> Digital Rights Management (DRM) 📡</li>
                <li> Invisible Metadata Embedding </li>
                <li> Forensic Analysis 🕵️‍♀️</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Start by selecting the 'Encode' option from the sidebar menu section with styling
    st.markdown(
        """
        <div style='text-align: justify; margin-top: 20px;'>
            <p>Start by selecting the <strong>'Encode'</strong> option from the sidebar menu to encrypt your message into an audio file!</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Encoder
elif selected == "Encode":
    set_background("BGI.png")
    current_dir = os.getcwd()
    uploaded_image = st.file_uploader("Upload an Image (.png only accepted)", type=["png"], accept_multiple_files=False)
    if uploaded_image is not None:
        with open(os.path.join(current_dir, uploaded_image.name), "wb") as f:
                f.write(uploaded_image.getbuffer())    
    
    uploaded_audio = st.file_uploader("Upload an Audio (.mp3 only accepted)", type=["mp3"], accept_multiple_files=False)
    if uploaded_audio is not None : 
        with open(os.path.join(current_dir, uploaded_audio.name), "wb") as f:
            f.write(uploaded_audio.getbuffer())
    
    data = st.text_input("Enter Plaintext")
    submit3 = st.button("Encrypt")   
    if submit3:

        #Encrypting the text into image           
        img = Image.open(uploaded_image.name)
        img_name = "Encrypted_Image.png"
        img_stegano = encode(img, data.encode())
        img_stegano.save(img_name)
        
        #Encrypting the image into Audio
        audio = load(uploaded_audio.name)
        audio.initTag()
        audio.tag.images.set(3, open(img_name, "rb").read(), "image/png")
        encrypted_audio_name = "Encrypted_Audio.mp3"
        audio.tag.save(encrypted_audio_name)

        st.markdown("Data Encrypted")

# Page to Describe about the website
elif selected == "Decode":
    set_background("BGI.png")
    # Add information about the application or any other content for the "About" section
    st.write("Decoding Text : ")
    uploaded_audio = st.file_uploader("Upload Encrypted Audio (.mp3 only accepted)", type=["mp3"], accept_multiple_files=False)
    if st.button("Decrypt") :
        if uploaded_audio is not None:

            audio = load("Encrypted_Audio.mp3")
            img = open("temp_img.png", "wb")
            img.write(audio.tag.images[0].image_data)

            img.close()
            img = Image.open("temp_img.png")
            text = decode(img)

            system("del temp_img.png")
            st.markdown("Encrypted data is: "+ str(text))