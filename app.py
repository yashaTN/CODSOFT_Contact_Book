import streamlit as st
import pandas as pd

# --- Page Setup ---
st.set_page_config(page_title="📞 Contact Book", page_icon="📇", layout="centered")
st.title("📞 Contact Book App")
st.write("Manage your contacts easily with this simple Streamlit app!")

# --- Initialize Contact Storage ---
if "contacts" not in st.session_state:
    st.session_state.contacts = pd.DataFrame(columns=["Name", "Phone", "Email", "Address"])

# --- Function to Add Contact ---
def add_contact(name, phone, email, address):
    new_contact = pd.DataFrame({
        "Name": [name],
        "Phone": [phone],
        "Email": [email],
        "Address": [address]
    })
    st.session_state.contacts = pd.concat([st.session_state.contacts, new_contact], ignore_index=True)

# --- Function to Delete Contact ---
def delete_contact(name):
    st.session_state.contacts = st.session_state.contacts[st.session_state.contacts["Name"] != name]

# --- Function to Update Contact ---
def update_contact(old_name, new_name, phone, email, address):
    index = st.session_state.contacts[st.session_state.contacts["Name"] == old_name].index
    if not index.empty:
        i = index[0]
        st.session_state.contacts.at[i, "Name"] = new_name
        st.session_state.contacts.at[i, "Phone"] = phone
        st.session_state.contacts.at[i, "Email"] = email
        st.session_state.contacts.at[i, "Address"] = address

# --- Tabs for UI ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["➕ Add", "📋 View", "🔍 Search", "✏️ Update", "🗑️ Delete"])

# --- 1. Add Contact ---
with tab1:
    st.subheader("Add a New Contact")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    address = st.text_area("Address")
    if st.button("Add Contact"):
        if name and phone:
            add_contact(name, phone, email, address)
            st.success(f"✅ Contact '{name}' added successfully!")
        else:
            st.warning("⚠️ Please enter at least a name and phone number.")

# --- 2. View Contacts ---
with tab2:
    st.subheader("All Contacts")
    if len(st.session_state.contacts) == 0:
        st.info("No contacts added yet.")
    else:
        st.dataframe(st.session_state.contacts, use_container_width=True)

# --- 3. Search Contact ---
with tab3:
    st.subheader("Search Contact")
    search_term = st.text_input("Enter name or phone number to search")
    if st.button("Search"):
        results = st.session_state.contacts[
            st.session_state.contacts["Name"].str.contains(search_term, case=False, na=False) |
            st.session_state.contacts["Phone"].str.contains(search_term, case=False, na=False)
        ]
        if len(results) > 0:
            st.success("✅ Contact(s) Found:")
            st.dataframe(results, use_container_width=True)
        else:
            st.warning("❌ No matching contact found.")

# --- 4. Update Contact ---
with tab4:
    st.subheader("Update Contact")
    if len(st.session_state.contacts) == 0:
        st.info("No contacts available to update.")
    else:
        selected_name = st.selectbox("Select a contact to update", st.session_state.contacts["Name"])
        contact_data = st.session_state.contacts[st.session_state.contacts["Name"] == selected_name].iloc[0]

        new_name = st.text_input("New Name", value=contact_data["Name"])
        new_phone = st.text_input("New Phone", value=contact_data["Phone"])
        new_email = st.text_input("New Email", value=contact_data["Email"])
        new_address = st.text_area("New Address", value=contact_data["Address"])

        if st.button("Update Contact"):
            update_contact(selected_name, new_name, new_phone, new_email, new_address)
            st.success(f"✅ Contact '{selected_name}' updated successfully!")
            st.rerun()

# --- 5. Delete Contact ---
with tab5:
    st.subheader("Delete Contact")
    if len(st.session_state.contacts) == 0:
        st.info("No contacts available to delete.")
    else:
        selected_name = st.selectbox("Select a contact to delete", st.session_state.contacts["Name"])
        if st.button("Delete"):
            delete_contact(selected_name)
            st.error(f"🗑️ Contact '{selected_name}' deleted.")
            st.rerun()

# --- Footer ---
st.markdown("---")
st.caption("✨ Built with Streamlit & Python — Contact Manager by [Your Name]")
