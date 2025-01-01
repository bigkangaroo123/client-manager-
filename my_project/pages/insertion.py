import streamlit as st

st.title("Add a client")

# Ensure 'clients' exists in session state
if 'clients' not in st.session_state:
    st.session_state.clients = []  # Initialize an empty list for clients

# Use session_state to preserve form input across reruns
if 'client_name' not in st.session_state:
    st.session_state.client_name = ''
if 'billing_rate' not in st.session_state:
    st.session_state.billing_rate = ''

# Inputs linked to session_state
client_name = st.text_input("Enter the name of the client", key="client_name", value=st.session_state.client_name)
billing_rate = st.text_input("Add hourly billing rate with this client", key="billing_rate", value=st.session_state.billing_rate)

add_client_button = st.button("Add Client", key="add_client_button")


if add_client_button:
    # Check for empty fields
    if not client_name:
        st.error("Please input the client's name to proceed...")
    elif not billing_rate:
        st.error("Please also input the billing rate to proceed...")
    else:
        try:
            billing_rate = int(billing_rate)
            if billing_rate <= 0:
                st.error("Please enter a positive integer for the billing rate.")
            else:
                st.session_state.clients.append({"name": client_name, "rate": billing_rate})
                # Clear inputs after successful addition
                st.success(f"Client '{client_name}' with rate {billing_rate}/hour added!")
        except ValueError:
            st.error("Please enter a valid integer for the billing rate.")