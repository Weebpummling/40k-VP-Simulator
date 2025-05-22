import streamlit as st
import numpy as np
import random
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# 1) Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def compute_ev(events):
    """Compute EV per round for mission cards (pts × pct/100)."""
    return [
        sum(pts * (probs[r] / 100) for pts, probs in events)
        for r in range(5)
    ]

def score_card(events, round_idx):
    """Sample each event once in round round_idx; sum all points scored."""
    return sum(
        pts
        for pts, probs in events
        if random.random() < probs[round_idx] / 100
    )

def compute_primary_ev(distribution):
    """Compute EV per round for an exclusive primary‐VP distribution."""
    return [
        sum(pts * (p[r] / 100) for pts, p in distribution)
        for r in range(5)
    ]

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base card definitions
# ─────────────────────────────────────────────────────────────────────────────

BASE_CARDS = {
    "Assassination":         {"initial": (5, [20,30,50,70,80]),      "additional": None},
    "Containment":           {"initial": (3, [100,100,100,100,100]), "additional": (3, [100,100,70,60,50])},
    "Behind Enemy Lines":    {"initial": (3, [0,20,30,60,60]),       "additional": (1, [0,0,20,50,60])},
    "Marked for Death":      {"initial": (5, [0,0,20,30,50]),        "additional": None},
    "Bring it Down":         {"initial": (2, [0,50,60,70,80]),       "additional": (2, [0,40,50,60,70])},
    "No Prisoners":          {"initial": (2, [20,80,90,90,90]),      "additional": (2, [0,60,70,80,80])},
    "Defend Stronghold":     {"initial": (3, [0,100,100,100,100]),   "additional": None},
    "Storm Hostile Objective":{"initial": (4, [0,60,70,80,60]),     "additional": None},
    "Sabotage":              {"initial": (3, [100,90,80,70,60]),     "additional": (3, [0,0,0,0,10])},
    "Cull the Horde":        {"initial": (5, [0,0,0,20,30]),         "additional": None},
    "Overwhelming Force":    {"initial": (3, [10,70,70,80,80]),      "additional": (2, [0,30,70,80,70])},
    "Extend Battlelines":    {"initial": (5, [100,100,100,90,90]),    "additional": None},
    "Recover Assets":        {"initial": (3, [100,80,70,60,60]),     "additional": (6, [0,0,20,30,30])},
    "Engage on All Fronts":  {"initial": (2, [80,30,50,70,80]),      "additional": (2, [0,30,40,50,60])},
    "Area Denial":           {"initial": (2, [100,80,80,80,80]),     "additional": (3, [80,70,70,70,70])},
    "Secure No Man's Land":  {"initial": (2, [100,100,100,100,100]), "additional": (3, [80,80,70,70,70])},
    "Cleanse":               {"initial": (2, [100,100,100,100,100]), "additional": (2, [70,70,70,70,70])},
    "Establish Locus":       {"initial": (2, [100,80,80,80,80]),     "additional": (2, [0,0,40,50,70])},
}

round_labels   = [f"Round {i+1}" for i in range(5)]
forbidden_r1   = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 3) Your mission‐cards input
# ─────────────────────────────────────────────────────────────────────────────

st.header("Your Mission Cards")
selected_y = st.multiselect(
    "Choose your cards",
    options=list(BASE_CARDS.keys()),
    default=list(BASE_CARDS.keys())
)

your_card_events = {}
for card in selected_y:
    cfg = BASE_CARDS[card]
    evs = []
    st.markdown(f"**{card}** — Initial VP: {cfg['initial'][0]}")
    cols = st.columns(5)
    probs = [
        cols[i].number_input(f"{card} R{i+1} (%)", 0, 100, cfg['initial'][1][i], key=f"you_{card}_init_{i}")
        for i in range(5)
    ]
    evs.append((cfg['initial'][0], probs))
    if cfg['additional']:
        st.markdown(f"{card} — Additional VP: {cfg['additional'][0]}")
        cols2 = st.columns(5)
        probs2 = [
            cols2[i].number_input(f"{card} R{i+1} add (%)", 0, 100, cfg['additional'][1][i], key=f"you_{card}_add_{i}")
            for i in range(5)
        ]
        evs.append((cfg['additional'][0], probs2))
    your_card_events[card] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 4) Your primary‐VP distribution
# ─────────────────────────────────────────────────────────────────────────────

st.header("Your Primary VP Distribution")
n_out_y = st.number_input("Number of primary outcomes", 1, 5, 2, key="you_n_out")
your_primary = []
for idx in range(n_out_y):
    pts = st.number_input(f"Outcome {idx+1} VP", 0, 10, idx, key=f"you_pr_pts_{idx}")
    cols = st.columns(5)
    p = [
        cols[i].number_input(f"R{i+1} (%)", 0, 100, 0, key=f"you_pr_{idx}_{i}")
        for i in range(5)
    ]
    your_primary.append((pts, p))

# ─────────────────────────────────────────────────────────────────────────────
# 5) Opponent mission‐cards input
# ─────────────────────────────────────────────────────────────────────────────

st.header("Opponent Mission Cards")
selected_o = st.multiselect(
    "Choose opponent cards",
    options=list(BASE_CARDS.keys()),
    default=list(BASE_CARDS.keys())
)

opp_card_events = {}
for card in selected_o:
    cfg = BASE_CARDS[card]
    evs = []
    cols = st.columns(5)
    probs = [
        cols[i].number_input(f"Opp {card} R{i+1} (%)", 0,100,cfg['initial'][1][i], key=f"opp_{card}_init_{i}")
        for i in range(5)
    ]
    evs.append((cfg['initial'][0], probs))
    if cfg['additional']:
        cols2 = st.columns(5)
        probs2 = [
            cols2[i].number_input(f"Opp {card} R{i+1} add (%)", 0,100,cfg['additional'][1][i], key=f"opp_{card}_add_{i}")
            for i in range(5)
        ]
        evs.append((cfg['additional'][0], probs2))
    opp_card_events[card] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 6) Opponent primary‐VP distribution
# ─────────────────────────────────────────────────────────────────────────────

st.header("Opponent Primary VP Distribution")
n_out_o = st.number_input("Opp primary outcomes", 1,5,2, key="opp_n_out")
opp_primary = []
for idx in range(n_out_o):
    pts = st.number_input(f"Opp Outcome {idx+1} VP", 0,10,idx, key=f"opp_pr_pts_{idx}")
    cols = st.columns(5)
    p = [
        cols[i].number_input(f"R{i+1} (%)", 0,100,0, key=f"opp_pr_{idx}_{i}")
        for i in range(5)
    ]
    opp_primary.append((pts, p))

# ─────────────────────────────────────────────────────────────────────────────
# 7) Sidebar form: settings + run guard
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar.form("settings_form"):
    st.header("Simulation Settings")
    n_trials      = st.number_input("Trials", 1000, 200000, 30000, 1000)
    seed_str      = st.text_input("Random Seed (optional)")
    apply_r1      = st.checkbox("Apply Round-1 Reshuffle Rule", True)
    allow_discard = st.checkbox("Allow Discard/Redraw", True)
    included      = st.multiselect("Include Rounds", round_labels, default=round_labels)
    run_sim       = st.form_submit_button("Run Simulation ▶️")

if not run_sim:
    st.info("Configure inputs above, then click ▶️ Run Simulation.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 8) Parse settings & prepare
# ─────────────────────────────────────────────────────────────────────────────

if seed_str:
    random.seed(int(seed_str))
    np.random.seed(int(seed_str))

included_idx = [round_labels.index(r) for r in included]

# Simulation helper
def run_simulation(card_events):
    # EV lookup
    ev_lookup = {c: compute_ev(evs) for c, evs in card_events.items()}
    # redraw candidates
    redraw = {}
    for r in included_idx:
        pool = [
            c for c in ev_lookup
            if not (r == 0 and apply_r1 and c in forbidden_r1)
        ]
        avg = np.mean([ev_lookup[c][r] for c in pool]) if pool else 0
        redraw[f"Round {r+1}"] = sorted(c for c in pool if ev_lookup[c][r] < avg)
    df_redraw = pd.DataFrame({
        "Round": list(redraw),
        "Cards to Redraw": [", ".join(redraw[r]) for r in redraw]
    })
    # Monte Carlo
    scores = np.zeros((n_trials, 5))
    for t in range(n_trials):
        disc = set()
        for r in range(5):
            pool = [c for c in card_events if c not in disc]
            if r == 0 and apply_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            if not pool:
                continue
            hand = random.sample(pool, 2)
            if allow_discard:
                evs_list = [ev_lookup[c][r] for c in hand]
                rem = [c for c in pool if c not in hand]
                rep = np.mean([ev_lookup[c][r] for c in rem]) if rem else 0
                if rep > min(evs_list):
                    idx = int(np.argmin(evs_list))
                    disc.add(hand[idx])
                    hand[idx] = random.choice(rem) if rem else hand[idx]
            scores[t, r] = sum(score_card(card_events[c], r) for c in hand)
    return scores.mean(axis=0), df_redraw

# Run for user and opponent
user_mission_ev, user_redraw_df = run_simulation(your_card_events := your_card_events)
opp_mission_ev,  opp_redraw_df  = run_simulation(opp_card_events)

# Primary EVs
user_primary_ev = compute_primary_ev(your_primary)
opp_primary_ev  = compute_primary_ev(opp_primary)

# ─────────────────────────────────────────────────────────────────────────────
# 9) Display Results
# ─────────────────────────────────────────────────────────────────────────────

# Your side
st.header("Results — Your Side")
st.subheader("Mission VP by Round")
st.table(pd.DataFrame({
    "Round":       [f"Round {i+1}" for i in included_idx],
    "Expected VP": np.round(user_mission_ev[included_idx],4)
}))
st.subheader("Primary VP by Round")
st.table(pd.DataFrame({
    "Round":       round_labels,
    "Expected VP": np.round(user_primary_ev,4)
}))
st.subheader("Cards to Redraw by Round")
st.table(user_redraw_df)

# Opponent side
st.header("Results — Opponent Side")
st.subheader("Mission VP by Round")
st.table(pd.DataFrame({
    "Round":       [f"Round {i+1}" for i in included_idx],
    "Expected VP": np.round(opp_mission_ev[included_idx],4)
}))
st.subheader("Primary VP by Round")
st.table(pd.DataFrame({
    "Round":       round_labels,
    "Expected VP": np.round(opp_primary_ev,4)
}))
st.subheader("Cards to Redraw by Round")
st.table(opp_redraw_df)

# ─────────────────────────────────────────────────────────────────────────────
# 10) Total Expected VP
# ─────────────────────────────────────────────────────────────────────────────

user_mission_total  = user_mission_ev[included_idx].sum()
opp_mission_total   = opp_mission_ev[included_idx].sum()
user_primary_total  = sum(user_primary_ev)
opp_primary_total   = sum(opp_primary_ev)
user_total          = user_mission_total + user_primary_total
opp_total           = opp_mission_total  + opp_primary_total

st.markdown("---")
c1, c2 = st.columns(2)
c1.metric("Your Total VP",     f"{user_total:.2f}")
c2.metric("Opponent Total VP", f"{opp_total:.2f}")
