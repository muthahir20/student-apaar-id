import streamlit as st
from sqlalchemy import create_engine

# ---------------------------------------------------------
# TiDB CONNECTION
# ---------------------------------------------------------
USERNAME = "kCCeTyfqG4q97x6.root"
PASSWORD = "O5K4JarXblpcn7gg"
HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
PORT = 4000
DB_NAME = "students"

engine = create_engine(
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    "?ssl_verify_cert=false&ssl_verify_identity=false"
)
# ---------------------------------------------------------
# STATE FIX (IMPORTANT)
# ---------------------------------------------------------
if "student_loaded" not in st.session_state:
    st.session_state.student_loaded = False
if "student_data" not in st.session_state:
    st.session_state.student_data = None

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
st.title("Student APAAR ID Form")

register_no = st.text_input("Enter Your Register Number")

# FETCH BUTTON
if st.button("Fetch Details"):
    with engine.connect() as conn:
        row = conn.execute(
            text("SELECT name, department, aadhar, apaar FROM students WHERE register_no=:r"),
            {"r": register_no}
        ).fetchone()

    if row:
        st.session_state.student_loaded = True
        st.session_state.student_data = row
    else:
        st.error("Register Number Not Found!")

# SHOW STUDENT DETAILS IF LOADED
if st.session_state.student_loaded:
    name, dept, aadhar, existing_apaar = st.session_state.student_data

    st.success("Record Found!")
    st.write(f"**Name:** {name}")
    st.write(f"**Department:** {dept}")
    st.write(f"**Aadhar:** {aadhar}")

    apaar_input = st.text_input(
        "Enter APAAR ID", value=existing_apaar or "", key="apaar_input"
    )

    # SUBMIT BUTTON (NOW WORKS)
    if st.button("Submit APAAR ID"):
        with engine.begin() as conn:
            result = conn.execute(
                text("UPDATE students SET apaar=:a WHERE register_no=:r"),
                {"a": apaar_input, "r": register_no}
            )

        st.success("APAAR ID Saved Successfully!")

        # reset state
        st.session_state.student_loaded = False
        st.session_state.student_data = None


