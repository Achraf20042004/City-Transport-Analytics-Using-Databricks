import streamlit as st
import sqlite3
import hashlib
from agent import ask_city  # your pipeline file with ask_city, CITY_TABLES

st.set_page_config(page_title="City Transport Assistant", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }
    h1, h2, h3, .stMarkdown, label, p {
        color: #f5f5f5 !important;
    }
    .stTextInput input, .stTextInput input:focus {
        background-color: rgba(255,255,255,0.08);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 8px;
    }
    .stButton button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5em 1.5em;
        font-weight: 600;
        transition: 0.2s;
    }
    .stButton button:hover {
        transform: scale(1.03);
        box-shadow: 0 4px 12px rgba(0,114,255,0.4);
    }
    .answer-box {
        background: rgba(255,255,255,0.08);
        border-left: 4px solid #00c6ff;
        padding: 1em;
        border-radius: 8px;
        margin-top: 1em;
        color: white;
    }
</style>
""", unsafe_allow_html=True)


def hash_pw(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def check_login(username, password):
    conn = sqlite3.connect("auth.db")
    cur = conn.execute(
        "SELECT password_hash, role, city FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    if row is None:
        return None

    stored_hash, role, city = row
    if hash_pw(password) == stored_hash:
        return {"role": role, "city": city}
    return None

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        result = check_login(username, password)
        if result:
            st.session_state.user = {"username": username, **result}
            st.rerun()
        else:
            st.error("Invalid username or password")

else:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown(
            f"<p style='color:#cfd8dc; font-size:0.9em;'>Signed in as "
            f"<strong style='color:white;'>{st.session_state.user['username']}</strong> "
            f"· {st.session_state.user['role'].replace('_', ' ').title()}</p>",
            unsafe_allow_html=True
        )
    with col2:
        if st.button("Log out"):
            st.session_state.user = None
            st.rerun()

    if st.session_state.user["role"] == "manager":
        st.subheader("Add a City Responsible")

        cities = ["Chandigarh", "Coimbatore", "Indore", "Jaipur", "Kochi",
                  "Lucknow", "Mysore", "Surat", "Vadodara"]

        new_username = st.text_input("New username")
        new_password = st.text_input("New password", type="password")
        selected_city = st.selectbox("Assign city", cities)

        if st.button("Create city responsible"):
            conn = sqlite3.connect("auth.db")
            try:
                conn.execute(
                    "INSERT INTO users (username, password_hash, role, city) VALUES (?, ?, 'city_responsible', ?)",
                    (new_username, hash_pw(new_password), selected_city)
                )
                conn.commit()
                st.success(f"Created '{new_username}' for {selected_city}")
            except sqlite3.IntegrityError:
                st.error("Username already exists")
            finally:
                conn.close()

        st.subheader("Existing City Responsibles")
        conn = sqlite3.connect("auth.db")
        rows = conn.execute(
            "SELECT username, city FROM users WHERE role = 'city_responsible'"
        ).fetchall()
        conn.close()

        if rows:
            for uname, city in rows:
                st.write(f"- **{uname}** → {city}")
        else:
            st.write("No city responsibles yet.")

    if st.session_state.user["role"] == "city_responsible":
        city = st.session_state.user["city"]
        st.subheader(f"Chatbot — {city}")

        question = st.text_input("Ask a question about your city's trips")
        if st.button("Ask") and question:
            with st.spinner("Thinking..."):
                answer = ask_city(question, city)
            st.markdown(f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True)