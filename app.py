import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urlparse

st.set_page_config(page_title="IG Who Doesn't Follow You Back Checker", layout="centered")

st.title("Instagram Non-Followers Checker")

st.markdown("""
**How to download your Instagram data (HTML):**

1. In the Instagram mobile app or on the web, go to **Settings** → search for **Download Data**.  
2. Enter your email and request your data (you can choose to have it sent to Google Drive).  
3. Make sure **HTML** is selected as the format.  
4. When you receive the ZIP archive, unzip it and locate the files named `following.html` and `followers_1.html` (names may vary slightly).
""")

# File upload widgets
f1 = st.file_uploader("Upload your followers HTML (e.g. followers_1.html)", type="html")
f2 = st.file_uploader("Upload your following HTML (e.g. following.html)", type="html")

def parse_html(file_bytes):
    soup = BeautifulSoup(file_bytes, "html.parser")
    users = set()
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "instagram.com/" not in href:
            continue
        path = urlparse(href).path.strip("/")
        if path and "/" not in path:
            users.add(path)
    return users

if f1 and f2:
    followers = parse_html(f1.read())
    following = parse_html(f2.read())
    non_followers = sorted(following - followers)

    st.write(f"**You follow {len(following)} accounts**, of which **{len(non_followers)}** don’t follow you back.")
    st.dataframe(non_followers, height=300)
