import os
import csv
import time
from threading import Lock



METRICS_DIR = "data/metrics"
METRICS_FILE = os.path.join(METRICS_DIR, "metrics.csv")

file_lock = Lock()



os.makedirs(METRICS_DIR, exist_ok=True)

if not os.path.exists(METRICS_FILE):
    with open(METRICS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",        
            "model",            
            "latency",  
            "response_length"   
        ])



def log_metrics(model: str, latency: float, response_length: int):
    """
    Logs performance metrics for each model call.

    This function is called AFTER a model generates a response.
    It does NOT affect model execution.
    """

    with file_lock: 
        with open(METRICS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                time.time(),
                model,
                round(latency, 3),
                response_length
            ])

        if st.button("Login", use_container_width=True):
            users = load_users()
            hashed = hash_password(password)

            valid = (
                (users["username"] == username) &
                (users["password"] == hashed)
            ).any()

            if valid:
                st.session_state.user = username
                st.success("✅ Login successful")
                st.rerun()
            else:
                st.error("❌ Invalid username or password")

    with tab_register:
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
        confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")

        if st.button("Register", use_container_width=True):
            users = load_users()

            if new_user.strip() == "":
                st.error("Username cannot be empty")
            elif new_user in users["username"].values:
                st.error("Username already exists")
            elif len(new_pass) < 4:
                st.error("Password must be at least 4 characters")
            elif new_pass != confirm:
                st.error("Passwords do not match")
            else:
                save_user(new_user, new_pass)
                st.success("🎉 Registration successful. Please login.")