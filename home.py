import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import arabic_reshaper
from bidi.algorithm import get_display
import os

st.set_page_config(
    page_title="MoneyMoon Eid Images",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌙",
)

# Initialize session state for language
if "language" not in st.session_state:
    st.session_state.language = "English"

# Language toggle function
def toggle_language():
    if st.session_state.language == "English":
        st.session_state.language = "Arabic"
    else:
        st.session_state.language = "English"



# Define translations
translations = {
    "English": {
        "title": "MoneyMoon Eid Images! 🎉",
        "sidebar_text": "Developed by MoneyMoon's team",
        "greeting": "Moneymoon family wishes you a happy Eid Al-Fitr! Please type your name and click the button to get your Eid Al-Fitr 2025 greeting card!",
        "name_label": "Name:",
        "generate_button": "Generate Eid Image",
        "caption": "Your Eid Image",
        "download": "Download the Image!",
    },
    "Arabic": {
        "title": "🎉!عيد موني مون ",
        "sidebar_text": "تم التطوير بواسطة فريق موني مون",
        "greeting": "عائلة موني مون تتمنى لكم عيد فطر سعيد! يرجى كتابة اسمك والضغط على الزر للحصول على بطاقة تهنئة عيد الفطر",
        "name_label": ":الاسم",
        "generate_button": "إنشاء بطاقة التهنئة",
        "caption": "صورتك للعيد",
        "download": "!تحميل الصورة",
    }
}

# Get the current language texts
lang = st.session_state.language
texts = translations[lang]

with st.sidebar:
    st.image("./MM-LOGO.png")
    # Language toggle button using session state
    st.button(
        "عربي" if st.session_state.language == "English" else "EN",
        key="lang_toggle",
        on_click=toggle_language
    )
    st.sidebar.write(texts["sidebar_text"])

st.title(texts["title"])


def create_image_with_name(name, template_path="./Moneymoon-Ramadan.jpg"):
    # Open the template image
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)

    # Reshape and fix Arabic text direction
    reshaped_text = arabic_reshaper.reshape(name)
    bidi_text = get_display(reshaped_text)

    # Load custom Arabic font
    font_path = os.path.join("fonts", "Amiri-Regular.ttf")  # Ensure this file exists!
    try:
        font = ImageFont.truetype(font_path, size=80)
    except IOError:
        font = ImageFont.load_default()  # Fallback, but won't support Arabic

    # Get text size
    bbox = draw.textbbox((0, 0), bidi_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text on the image
    img_width, img_height = img.size
    x = (img_width - text_width) / 2
    y = (img_height - text_height) / 2

    # Draw text on the image
    draw.text((x, y-100), bidi_text, font=font, fill="#008afe")

    return img


st.write(texts["greeting"])
name = st.text_input(texts["name_label"])

img = None
if st.button(texts["generate_button"]):
    img = create_image_with_name(name)
    st.image(img, caption=texts["caption"])

    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    st.download_button(
        label=texts["download"],
        data=img_bytes,
        file_name="eid_image.png",
        mime="image/png",
    )
