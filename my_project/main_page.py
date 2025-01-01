import streamlit as st
from pages import insertion, viewing
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="EasyManage", 
    page_icon="🗿"
)

st.sidebar.success("Select a tab above")

st.title(" # Welcome to EasyManage! 🗿 ")

add_clients = st.button("Click to add clients")
view_clients = st.button("Click to view clients")

if add_clients:
    switch_page(insertion)

if view_clients:
    switch_page(viewing)
