import streamlit as st

st.title("Run Simulation Gate Test")

# Sidebar inputs (you can add yours here later)
trials = st.sidebar.number_input("Trials", 1000, 200000, 30000, 1000)

# Simple Run button
run_sim = st.sidebar.button("Run Simulation ▶️")

# Gate execution
if not run_sim:
    st.info("Configure your settings, then click ▶️ Run Simulation.")
    st.stop()

# --- Everything below here only runs after you click! ---
st.success("✅ The simulation is now running (or would run)!")
st.write(f"You requested {trials} trials.")
