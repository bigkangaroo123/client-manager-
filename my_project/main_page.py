<<<<<<< HEAD
import streamlit as st

st.set_page_config(
    page_title="EasyManage", 
    page_icon="🗿"
)

st.title("Welcome to EasyManage! :D")

st.markdown(
    """
    EasyManage is an efficient and easy way to manage your clients and their projects
    You have the ability to:

    - Add all your clients
    - Add all the projects you have with your clients
    - Make a personal note for yourself of the tasks required to complete each task, with a personal deadline feature (not required)
    - Keep track of the hours you spent doing each task, which will add up and calculate how much money you made from that project

    Navigate through the different pages using the side bar!
"""
)
=======
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
>>>>>>> 82a7b8034ee932020eb8626624fcf43d299eac17
