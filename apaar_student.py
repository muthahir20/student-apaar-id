import streamlit as st
from sqlalchemy import create_engine, text

# ------------------------------
# TiDB CONNECTION
# ------------------------------
USERNAME = "kCCeTyfqG4q97x6.root"
PASSWORD = "O5K4JarXblpcn7gg"
HOST = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com"
PORT = 4000
DB_NAME = "students"

engine = create_engine(
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    "?ssl_verify_cert=false&ssl_verify_identity=false"
)

# ------------------------------
# SESSION STATE
# ------------------------------
if "student" not in st.session_state:
    st.session_state.student = None

# ------------------------------
# CUSTOM UI STYLES
# ------------------------------
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 40px;
        color: #4CAF50;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 18px;
        margin-top: -15px;
        margin-bottom: 30px;
    }
    .card {
        padding: 25px;
        border-radius: 12px;
        background-color: #f9f9f9;
        border: 1px solid #ddd;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        max-width: 500px;
        margin: auto;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>Student APAAR Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Enter your details to update APAAR ID</div>", unsafe_allow_html=True)

# ------------------------------
# MAIN UI
# ------------------------------
#st.markdown("<div class='card'>", unsafe_allow_html=True)

reg = st.text_input("Register Number", placeholder="Enter your register number")
aadhar = st.text_input("Aadhar Number", placeholder="Enter your Aadhar number", type="password")

if st.button("Fetch My Details", use_container_width=True):

    if not reg.strip() or not aadhar.strip():
        st.error("⚠ Please enter both Register Number and Aadhar Number")
    else:
        query = text("""
            SELECT register_no, name, department, aadhar, apaar
            FROM students
            WHERE register_no = :reg AND aadhar = :aadhar
        """)

        with engine.connect() as conn:
            result = conn.execute(query, {"reg": reg, "aadhar": aadhar}).fetchone()

        if result:
            st.session_state.student = dict(result._mapping)
        else:
            st.session_state.student = None
            st.error("❌ Invalid Register Number or Aadhar Number")

# ------------------------------
# SHOW STUDENT INFO
# ------------------------------
if st.session_state.student:

    student = st.session_state.student
    st.success("✔ Student Found!")

    st.write("### 👤 Student Information")
    st.info(f"**Name:** {student['name']}")
    st.info(f"**Department:** {student['department']}")
    st.info(f"**Aadhar:** {student['aadhar']}")

    new_apaar = st.text_input(
        "Enter Your APAAR ID",
        placeholder="Enter APAAR ID",
        value=student["apaar"] if student["apaar"] else ""
    )

    if st.button("Update APAAR", use_container_width=True):

        if new_apaar.strip() == "":
            st.error("⚠ APAAR ID cannot be empty!")
        else:
            update_q = text("""
                UPDATE students
                SET apaar = :apaar
                WHERE register_no = :reg
            """)

            with engine.begin() as conn:
                conn.execute(update_q, {"apaar": new_apaar, "reg": student["register_no"]})

            st.success("🎉 APAAR ID Updated Successfully!")

            # Update session state safely by replacing whole dict
            updated_student = dict(st.session_state.student)
            updated_student["apaar"] = new_apaar
            st.session_state.student = updated_student

st.markdown("</div>", unsafe_allow_html=True)
