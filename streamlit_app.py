import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="40K VP Simulator", layout="wide")
st.title("40K Mission Card VP Simulator")

st.markdown("""
Edit the probability table below. Each row represents one (Card, Points) event and its **P(R1)**–**P(R5)** scoring chances.  
""")

# 1) Define all mission events
card_events = {
    "Assassination": [(5, [0.2, 0.3, 0.5, 0.7, 0.8])],
    "Containment":   [(3, [1.0, 1.0, 1.0, 1.0, 1.0]),
                       (6, [1.0, 1.0, 0.7, 0.6, 0.5])],
    "Behind Enemy Lines": [(3, [0,   0.2, 0.3, 0.6, 0.6]),
                            (4, [0,   0,   0.2, 0.5, 0.6])],
    "Marked for Death":    [(5, [0,   0,   0.2, 0.3, 0.5])],
    "Bring it Down":       [(2, [0,   0.5, 0.6, 0.7, 0.8]),
                            (4, [0,   0.4, 0.5, 0.6, 0.7]),
                            (6, [0,   0.1, 0.1, 0.0, 0.0]),
                            (8, [0,   0.05,0.05,0.0, 0.0])],
    "No Prisoners":        [(2, [0.2, 0.8, 0.9, 0.9, 0.9]),
                            (4, [0,   0.6, 0.7, 0.8, 0.8]),
                            (5, [0,   0.6, 0.7, 0.8, 0.75])],
    "Defend Stronghold":   [(3, [0,   1.0, 1.0, 1.0, 1.0])],
    "Storm Hostile Objective": [(4, [0, 0.6, 0.7, 0.8, 0.6])],
    "Sabotage":            [(3, [1.0, 0.9, 0.8, 0.7, 0.6]),
                            (6, [0,   0.0, 0.0, 0.0, 0.1])],
    "Cull the Horde":      [(5, [0,   0.0, 0.0, 0.2, 0.3])],
    "Overwhelming Force":  [(3, [0.1, 0.7, 0.7, 0.8, 0.8]),
                            (5, [0,   0.3, 0.7, 0.8, 0.7])],
    "Extend Battlelines":  [(5, [1.0, 1.0, 1.0, 0.9, 0.9])],
    "Recover Assets":      [(3, [1.0, 0.8, 0.7, 0.6, 0.6]),
                            (6, [0,   0.0, 0.2, 0.3, 0.3])],
    "Engage on All Fronts":[(2, [0.8, 0.3, 0.5, 0.7, 0.8]),
                            (4, [0,   0.3, 0.4, 0.5, 0.6])],
    "Area Denial":         [(2, [1.0, 0.8, 0.8, 0.8, 0.8]),
                            (5, [0.8, 0.7, 0.7, 0.7, 0.7])],
    "Secure No Man's Land":[(2, [1.0, 1.0, 1.0, 1.0, 1.0]),
                            (5, [0.8, 0.8, 0.7, 0.7, 0.7])],
    "Cleanse":             [(2, [1.0, 1.0, 1.0, 1.0, 1.0]),
                            (4, [0.7, 0.7, 0.7, 0.7, 0.7])],
    "Establish Locus":     [(2, [1.0, 0.8, 0.8, 0.8, 0.8]),
                            (4, [0.0, 0.0, 0.4, 0.5, 0.7])],
}

# 2) Build a uniform DataFrame from these events
rows = []
for card, events in card_events.items():
    for pts, probs in events:
        rows.append({
            "Card": card,
            "Points": pts,
            "P(R1)": probs[0],
            "P(R2)": probs[1],
            "P(R3)": probs[2],
            "P(R4)": probs[3],
            "P(R5)": probs[4],
        })
df = pd.DataFrame(rows)

# 3) Let the user edit probabilities in-place
edited = st.data_editor(df, num_rows="dynamic", key="prob-table")

# 4) Parse back into card_events structure
card_events = {}
for _, row in edited.iterrows():
    card = row["Card"]
    pts  = float(row["Points"])
    probs = [row[f"P(R{i})"] for i in range(1,6)]
    card_events.setdefault(card, []).append((pts, probs))

# 5) Sidebar controls
st.sidebar.header("Simulation Settings")
n_trials     = st.sidebar.number_input("Monte-Carlo Trials", value=30000, min_value=1000, step=1000)
reshuffle_r1 = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule", value=True)
allow_discard= st.sidebar.checkbox("Allow One-Card Discard/Redraw", value=True)

# Round-1 forbidden cards
forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# Precompute EV lookup
card_ev = {
    c: [sum(pts * probs[r] for pts, probs in evs) for r in range(5)]
    for c, evs in card_events.items()
}

# 6) Run simulation
scores = np.zeros((n_trials, 5))
for t in range(n_trials):
    discards = set()
    for r in range(5):
        # build draw pool
        pool = [c for c in card_events if c not in discards]
        if r == 0 and reshuffle_r1:
            pool = [c for c in pool if c not in forbidden_r1]
        draw = random.sample(pool, 2)

        # optional discard/redraw
        if allow_discard:
            evs = [card_ev[c][r] for c in draw]
            rest = [c for c in pool if c not in draw]
            rep_ev = np.mean([card_ev[c][r] for c in rest])
            if rep_ev > min(evs):
                idx = evs.index(min(evs))
                discards.add(draw[idx])
                kept = draw[1 - idx]
                draw = [kept, random.choice(rest)]

        # scoring
        pts = 0
        for c in draw:
            for p, probs in card_events[c]:
                if random.random() < probs[r]:
                    pts += p
        scores[t, r] = pts

# 7) Show results
exp_vp = scores.mean(axis=0)
df_result = pd.DataFrame({
    "Round":           [f"Round {i+1}" for i in range(5)],
    "Expected VP":     np.round(exp_vp, 4)
})

st.subheader("Expected VP by Round")
st.dataframe(df_result, use_container_width=True)

if allow_discard:
    # also compute no‐discard baseline
    scores_nd = np.zeros_like(scores)
    for t in range(n_trials):
        for r in range(5):
            pool = list(card_events.keys())
            if r == 0 and reshuffle_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            hand = random.sample(pool, 2)
            pts = 0
            for c in hand:
                for p, probs in card_events[c]:
                    if random.random() < probs[r]:
                        pts += p
            scores_nd[t, r] = pts
    nd = scores_nd.mean(axis=0)
    df_cmp = pd.DataFrame({
        "Round":          [f"Round {i+1}" for i in range(5)],
        "With Discard":   np.round(exp_vp,4),
        "Without Discard":np.round(nd,4),
    })
    st.subheader("With vs. Without Discard")
    st.dataframe(df_cmp, use_container_width=True)
