import streamlit as st
import numpy as np
import random
import pandas as pd
import os
import json

# ─────────────────────────────────────────────────────────────────────────────
# 0) Profile Manager
# ─────────────────────────────────────────────────────────────────────────────
PROFILE_DIR = "profiles"
os.makedirs(PROFILE_DIR, exist_ok=True)

# scan saved profiles
saved = [f[:-5] for f in os.listdir(PROFILE_DIR) if f.endswith(".json")]
profiles = ["Default"] + saved

st.sidebar.header("🔖 Profile Manager")
selected_profile = st.sidebar.selectbox("Load profile", profiles, index=0)

def load_default_template():
    tpl = {}
    for card, cfg in BASE_CARDS.items():
        # initial
        for j, pct in enumerate(cfg["initial"][1]):
            tpl[f"{card}_init_{j}"] = pct
        # additional
        if cfg["additional"]:
            for j, pct in enumerate(cfg["additional"][1]):
                tpl[f"{card}_add_{j}"] = pct
    return tpl

if selected_profile == "Default":
    # prefill session_state with template defaults if not already set
    default_tpl = load_default_template()
    for k, v in default_tpl.items():
        if k not in st.session_state:
            st.session_state[k] = v
else:
    # load from disk
    with open(os.path.join(PROFILE_DIR, f"{selected_profile}.json")) as fp:
        profile_data = json.load(fp)
    for k, v in profile_data.items():
        st.session_state[k] = v

# import CSV
uploaded = st.sidebar.file_uploader("Import profile CSV", type="csv")
if uploaded:
    df = pd.read_csv(uploaded, header=None)
    name = st.sidebar.text_input("Name for import", "")
    if name and st.sidebar.button("Save imported profile"):
        prof = dict(zip(df.iloc[:,0], df.iloc[:,1]))
        with open(os.path.join(PROFILE_DIR, f"{name}.json"), "w") as fp:
            json.dump(prof, fp)
        st.sidebar.success(f"Imported as '{name}'")
        st.experimental_rerun()

# save profile
save_name = st.sidebar.text_input("Save current as", "")
if save_name and st.sidebar.button("Save Profile"):
    current = {k: v for k, v in st.session_state.items()}
    with open(os.path.join(PROFILE_DIR, f"{save_name}.json"), "w") as fp:
        json.dump(current, fp)
    st.sidebar.success(f"Saved profile '{save_name}'")
    st.experimental_rerun()

# ─────────────────────────────────────────────────────────────────────────────
# 1) Starting bonus
# ─────────────────────────────────────────────────────────────────────────────
START_VP = 10  # free VP to start

# ─────────────────────────────────────────────────────────────────────────────
# 2) Helper functions
# ─────────────────────────────────────────────────────────────────────────────
def compute_ev(events):
    return [sum(pts * (probs[r]/100) for pts, probs in events) for r in range(5)]

def score_card(events, r):
    return sum(pts for pts, probs in events if random.random() < probs[r]/100)

# ─────────────────────────────────────────────────────────────────────────────
# 3) Base card definitions
# ─────────────────────────────────────────────────────────────────────────────
BASE_CARDS = {
    "Assassination":          {"initial": (5, [20,30,50,70,80]),       "additional": None},
    "Containment":            {"initial": (3, [100,100,100,100,100]),  "additional": (3, [100,100,70,60,50])},
    "Behind Enemy Lines":     {"initial": (3, [0,20,30,60,60]),        "additional": (1, [0,0,20,50,60])},
    "Marked for Death":       {"initial": (5, [0,0,20,30,50]),         "additional": None},
    "Bring it Down":          {"initial": (2, [0,50,60,70,80]),        "additional": (2, [0,40,50,60,70])},
    "No Prisoners":           {"initial": (2, [20,80,90,90,90]),       "additional": (2, [0,60,70,80,80])},
    "Defend Stronghold":      {"initial": (3, [0,100,100,100,100]),    "additional": None},
    "Storm Hostile Objective":{"initial": (4, [0,60,70,80,60]),        "additional": None},
    "Sabotage":               {"initial": (3, [100,90,80,70,60]),      "additional": (3, [0,0,0,0,10])},
    "Cull the Horde":         {"initial": (5, [0,0,0,20,30]),          "additional": None},
    "Overwhelming Force":     {"initial": (3, [10,70,70,80,80]),       "additional": (2, [0,30,70,80,70])},
    "Extend Battlelines":     {"initial": (5, [100,100,100,90,90]),     "additional": None},
    "Recover Assets":         {"initial": (3, [100,80,70,60,60]),      "additional": (6, [0,0,20,30,30])},
    "Engage on All Fronts":   {"initial": (2, [80,30,50,70,80]),       "additional": (2, [0,30,40,50,60])},
    "Area Denial":            {"initial": (2, [100,80,80,80,80]),      "additional": (3, [80,70,70,70,70])},
    "Secure No Man's Land":   {"initial": (2, [100,100,100,100,100]),  "additional": (3, [80,80,70,70,70])},
    "Cleanse":                {"initial": (2, [100,100,100,100,100]),  "additional": (2, [70,70,70,70,70])},
    "Establish Locus":        {"initial": (2, [100,80,80,80,80]),      "additional": (2, [0,0,40,50,70])},
}

round_labels = [f"Round {i+1}" for i in range(5)]
forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 4) CP Tracker
# ─────────────────────────────────────────────────────────────────────────────
st.header("🛡️ Command Points Tracker")
cpg, cps = st.columns(2)
cp_gained = cpg.number_input("CP Gained", min_value=0, value=0)
cp_spent  = cps.number_input("CP Spent",  min_value=0, value=0)
st.metric("Net CP", cp_gained - cp_spent)

# ─────────────────────────────────────────────────────────────────────────────
# 5) Live Scoreboard & Cards Used
# ─────────────────────────────────────────────────────────────────────────────
st.header("📋 Live Scoreboard & Cards Used")
st.markdown(
    "🔎 **Note:** Completed **Secondary Scores** exclude rounds from simulation; "
    "**Primary Scores** are for reference only."
)

secondary_scores = {}
primary_scores   = {}
removed_cards_all = set()

for i in range(1,6):
    st.subheader(f"Round {i}")
    c1, c2, c3 = st.columns([2,2,4])
    secondary_scores[i] = c1.number_input(f"Secondary Score R{i}", min_value=0, value=0, key=f"sec_{i}")
    primary_scores[i]   = c2.number_input(f"Primary Score R{i}",   min_value=0, value=0, key=f"pri_{i}")
    used = c3.multiselect(f"Cards used in R{i}", options=list(BASE_CARDS.keys()), key=f"used_{i}")
    removed_cards_all.update(used)

sec_total = sum(secondary_scores.values())
pri_total = sum(primary_scores.values())
st.markdown("---")
t1, t2, t3 = st.columns(3)
t1.metric("Starting Bonus VP", START_VP)
t2.metric("Secondary Total",    sec_total)
t3.metric("Primary Total",      pri_total)

included_idx = [i-1 for i in range(1,6) if secondary_scores[i]==0]

# ─────────────────────────────────────────────────────────────────────────────
# 6) Projected Victory Points (top of results)
# ─────────────────────────────────────────────────────────────────────────────
proj_placeholder = st.container()  # to fill after simulation

# ─────────────────────────────────────────────────────────────────────────────
# 7) Mission Cards Input
# ─────────────────────────────────────────────────────────────────────────────
st.header("🎯 Your Mission Cards")

categories = [
    "Guaranteed (100%)","Highly Likely (80%)","Likely (70%)",
    "Maybe (50%)","Unlikely (30%)","Highly Unlikely (10%)"
]
mapping = {c:int(c.split("(")[1].strip("%)")) for c in categories}

available = [c for c in BASE_CARDS if c not in removed_cards_all]
selected = st.multiselect("Select cards to include", options=available, default=available)

card_events = {}
for card in selected:
    cfg = BASE_CARDS[card]; evs=[]
    st.markdown(f"**{card}** — Initial VP: {cfg['initial'][0]}")
    cols = st.columns(5)
    probs = [mapping[cols[j].selectbox(f"R{j+1}", categories, index=3, key=f"{card}_init_{j}")] for j in range(5)]
    evs.append((cfg['initial'][0], probs))
    if cfg['additional']:
        st.markdown(f"{card} — Additional VP: {cfg['additional'][0]}")
        cols2 = st.columns(5)
        probs2 = [mapping[cols2[j].selectbox(f"R{j+1} add", categories, index=3, key=f"{card}_add_{j}")] for j in range(5)]
        evs.append((cfg['additional'][0], probs2))
    card_events[card] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 8) Sidebar: settings & run guard
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar.form("settings_form"):
    st.header("Simulation Settings")
    n_trials      = st.number_input("Trials", 1000,200000,30000,1000)
    seed_str      = st.text_input("Random Seed (optional)")
    apply_r1      = st.checkbox("Apply R1 Reshuffle", True)
    allow_discard = st.checkbox("Allow Discard", True)
    run_sim       = st.form_submit_button("Run Simulation ▶️")

if not run_sim:
    st.info("Adjust settings, then click ▶️ Run Simulation.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 9) Simulation helper & run
# ─────────────────────────────────────────────────────────────────────────────
if seed_str:
    random.seed(int(seed_str)); np.random.seed(int(seed_str))

def run_sim(card_events):
    ev_lookup = {c: compute_ev(evs) for c,evs in card_events.items()}
    # redraw
    redraw={}
    for r in included_idx:
        pool=[c for c in ev_lookup if not(r==0 and apply_r1 and c in forbidden_r1)]
        avg=np.mean([ev_lookup[c][r] for c in pool]) if pool else 0
        redraw[f"Round {r+1}"] = sorted(c for c in pool if ev_lookup[c][r]<avg)
    df_redraw=pd.DataFrame({"Round":list(redraw),"Cards to Redraw":[", ".join(redraw[r]) for r in redraw]})
    scores=np.zeros((n_trials,5))
    for t in range(n_trials):
        disc=set()
        for r in included_idx:
            pool=[c for c in card_events if c not in disc]
            if r==0 and apply_r1: pool=[c for c in pool if c not in forbidden_r1]
            if not pool: continue
            hand=random.sample(pool,2)
            if allow_discard:
                evs_list=[ev_lookup[c][r] for c in hand]
                rem=[c for c in pool if c not in hand]
                rep=np.mean([ev_lookup[c][r] for c in rem]) if rem else 0
                if rep>min(evs_list):
                    idx=int(np.argmin(evs_list)); disc.add(hand[idx])
                    hand[idx]=random.choice(rem) if rem else hand[idx]
            scores[t,r]=sum(score_card(card_events[c],r) for c in hand)
    return scores.mean(axis=0), df_redraw

mission_ev, redraw_df = run_sim(card_events)

# ─────────────────────────────────────────────────────────────────────────────
# 10) Fill projection placeholder
# ─────────────────────────────────────────────────────────────────────────────
exp_mission   = mission_ev[included_idx].sum()
scoreboard_tot= START_VP + sec_total + pri_total
projected_tot = scoreboard_tot + exp_mission

with proj_placeholder:
    st.markdown("## 📊 Projected Victory Points")
    m1,m2=st.columns(2)
    m1.metric("Current+Bonus+Score", f"{scoreboard_tot:.0f}")
    m2.metric("Projected Total VP",   f"{projected_tot:.2f}")
    st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# 11) Detailed Results
# ─────────────────────────────────────────────────────────────────────────────
st.header("🎯 Mission VP by Future Rounds")
st.table(pd.DataFrame({
    "Round":[round_labels[i] for i in included_idx],
    "Expected VP":np.round(mission_ev[included_idx],4)
}))
st.subheader("Cards to Redraw by Round")
st.table(redraw_df)
