import streamlit as st
from bs4 import BeautifulSoup
from urllib.parse import urlparse

st.title("Instagram Non-Followers Checker")

# File upload widgets
f1 = st.file_uploader("Upload Followers html file", type="html")
f2 = st.file_uploader("Upload Following html file", type="html")

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
