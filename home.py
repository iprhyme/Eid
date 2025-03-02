import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import arabic_reshaper
from bidi.algorithm import get_display

st.set_page_config(
    page_title="Eid Images Generator",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.sidebar.write("Developed by Yazeed")

st.title("Eid Images Generator! 🎉")

def create_image_with_name(name, template_path="./template.jpg"):
    # Open the template image
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)

    # Reshape Arabic text for proper rendering
    reshaped_text = arabic_reshaper.reshape(name)
    bidi_text = get_display(reshaped_text)  # Fix right-to-left order

    # Try to use a TrueType font that supports Arabic
    try:
        font = ImageFont.truetype("arial.ttf", size=30)  # Change font if needed
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text dimensions
    try:
        bbox = draw.textbbox((0, 0), bidi_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        text_width, text_height = draw.textsize(bidi_text, font=font)

    # Calculate position to center the text
    img_width, img_height = img.size
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2

    # Draw the name on the image
    draw.text((x, y), bidi_text, font=font, fill="black")

    return img


st.write("Welcome to Eid Images! Just type your name and click the button to see your Eid image!")

name=st.text_input("Name:")
st.write("Click the button to see your Eid image!")
img=None
if st.button("Generate Eid Image"):
    img=create_image_with_name(name)
    st.image(img, caption="Your Eid Image")


# Convert image to bytes for download
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    # Provide a download button
    st.download_button(
        label="Download the Image!",
        data=img_bytes,
        file_name="eid_image.png",
        mime="image/png",
    )

with st.expander("Contacts Information"):
    st.text("Contact Us via:")
    st.markdown("[Twitter](https://x.com/_YazeedA)")
    st.markdown("[LinkedIn](https://www.linkedin.com/in/yazeedalobaidan/)")
    
    




