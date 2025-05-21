import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="40K VP Simulator", layout="wide")
st.title("40K Mission Card VP Simulator")

st.markdown("""
You can **edit**, **add**, **delete**, or **deactivate** any mission directly in the table below.  
- To **remove** a card from the simulation, either delete its row or set **Active** to `False`.  
- To **add** a new card, click the **+** below the table and fill in its fields (including **Active**).
""")

# 1) Base mission definitions
base_events = {
    "Assassination":            [(5, [0.2,0.3,0.5,0.7,0.8])],
    "Containment":              [(3, [1,1,1,1,1]), (6, [1,1,0.7,0.6,0.5])],
    "Behind Enemy Lines":       [(3, [0,0.2,0.3,0.6,0.6]), (4, [0,0,0.2,0.5,0.6])],
    "Marked for Death":         [(5, [0,0,0.2,0.3,0.5])],
    "Bring it Down":            [(2, [0,0.5,0.6,0.7,0.8]), (4,[0,0.4,0.5,0.6,0.7]),
                                 (6,[0,0.1,0.1,0,0]), (8,[0,0.05,0.05,0,0])],
    "No Prisoners":             [(2, [0.2,0.8,0.9,0.9,0.9]), (4,[0,0.6,0.7,0.8,0.8]),
                                 (5,[0,0.6,0.7,0.8,0.75])],
    "Defend Stronghold":        [(3, [0,1,1,1,1])],
    "Storm Hostile Objective":  [(4, [0,0.6,0.7,0.8,0.6])],
    "Sabotage":                 [(3, [1,0.9,0.8,0.7,0.6]), (6,[0,0,0,0,0.1])],
    "Cull the Horde":           [(5, [0,0,0,0.2,0.3])],
    "Overwhelming Force":       [(3, [0.1,0.7,0.7,0.8,0.8]), (5,[0,0.3,0.7,0.8,0.7])],
    "Extend Battlelines":       [(5, [1,1,1,0.9,0.9])],
    "Recover Assets":           [(3, [1,0.8,0.7,0.6,0.6]), (6,[0,0,0.2,0.3,0.3])],
    "Engage on All Fronts":     [(2, [0.8,0.3,0.5,0.7,0.8]), (4,[0,0.3,0.4,0.5,0.6])],
    "Area Denial":              [(2, [1,0.8,0.8,0.8,0.8]), (5,[0.8,0.7,0.7,0.7,0.7])],
    "Secure No Man's Land":     [(2, [1,1,1,1,1]), (5,[0.8,0.8,0.7,0.7,0.7])],
    "Cleanse":                  [(2, [1,1,1,1,1]), (4,[0.7,0.7,0.7,0.7,0.7])],
    "Establish Locus":          [(2, [1,0.8,0.8,0.8,0.8]), (4,[0,0,0.4,0.5,0.7])]
}

# 2) Build DataFrame with an Active flag
rows = []
for card, evs in base_events.items():
    for pts, probs in evs:
        rows.append({
            "Card":   card,
            "Points": pts,
            "P(R1)":  probs[0],
            "P(R2)":  probs[1],
            "P(R3)":  probs[2],
            "P(R4)":  probs[3],
            "P(R5)":  probs[4],
            "Active": True,
        })
df = pd.DataFrame(rows)

# 3) Editable table (add/remove rows; toggle Active)
edited = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    key="prob-table"
)

# 4) Parse back only the rows where Active==True
card_events = {}
for _, row in edited[edited["Active"]].iterrows():
    c = row["Card"]
    p = float(row["Points"])
    probs = [row[f"P(R{i})"] for i in range(1,6)]
    card_events.setdefault(c, []).append((p, probs))

# 5) Sidebar controls
st.sidebar.header("Simulation Settings")
n_trials      = st.sidebar.number_input("Trials", 1000, 100000, 30000, 1000)
reshuffle_r1  = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule", True)
allow_discard = st.sidebar.checkbox("Allow One-Card Discard/Redraw", True)

# Round-1 forbidden reshuffle cards
forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# 6) Compute per-card EV under “one-score-only” model
card_ev = {}
for c, evs in card_events.items():
    # sort descending by VP so we test highest first
    sorted_evs = sorted(evs, key=lambda x: x[0], reverse=True)
    ev_list = []
    for r in range(5):
        rem, ev = 1.0, 0.0
        for pts, probs in sorted_evs:
            pr = probs[r]
            ev += pts * pr * rem
            rem *= (1 - pr)
        ev_list.append(ev)
    card_ev[c] = ev_list

# 7) Determine redraw candidates by comparing against deck-average EV
cards_to_redraw = {}
for r in range(5):
    pool = [c for c in card_ev if not (r == 0 and reshuffle_r1 and c in forbidden_r1)]
    avg_ev = np.mean([card_ev[c][r] for c in pool])
    cards_to_redraw[f"Round {r+1}"] = sorted([c for c in pool if card_ev[c][r] < avg_ev])
df_redraw = pd.DataFrame({
    "Round": list(cards_to_redraw.keys()),
    "Cards to Redraw": [", ".join(cards_to_redraw[r]) for r in cards_to_redraw]
})

# 8) Monte-Carlo simulation
scores = np.zeros((n_trials, 5))
for t in range(n_trials):
    discards = set()
    for r in range(5):
        pool = [c for c in card_events if c not in discards]
        if r == 0 and reshuffle_r1:
            pool = [c for c in pool if c not in forbidden_r1]
        draw = random.sample(pool, 2)

        if allow_discard:
            evs = [card_ev[c][r] for c in draw]
            rem = [c for c in pool if c not in draw]
            rep_ev = np.mean([card_ev[c][r] for c in rem])
            if rep_ev > min(evs):
                idx = evs.index(min(evs))
                discards.add(draw[idx])
                draw[idx] = random.choice(rem)

        # score each card once
        pts = 0
        for c in draw:
            for p, probs in sorted(card_events[c], key=lambda x: x[0], reverse=True):
                if random.random() < probs[r]:
                    pts += p
                    break
        scores[t, r] = pts

# 9) Display results
exp_vp = scores.mean(axis=0)
df_result = pd.DataFrame({
    "Round":       [f"Round {i+1}" for i in range(5)],
    "Expected VP": np.round(exp_vp, 4)
})

st.subheader("Expected VP by Round")
st.dataframe(df_result, use_container_width=True)

st.subheader("Cards to Redraw by Round")
st.dataframe(df_redraw, use_container_width=True)

if allow_discard:
    # no-discard baseline
    scores_nd = np.zeros_like(scores)
    for t in range(n_trials):
        for r in range(5):
            pool = list(card_events)
            if r == 0 and reshuffle_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            hand = random.sample(pool, 2)
            pts = 0
            for c in hand:
                for p, probs in sorted(card_events[c], key=lambda x: x[0], reverse=True):
                    if random.random() < probs[r]:
                        pts += p
                        break
            scores_nd[t, r] = pts
    nd = scores_nd.mean(axis=0)
    df_cmp = pd.DataFrame({
        "Round":           [f"Round {i+1}" for i in range(5)],
        "With Discard":    np.round(exp_vp,4),
        "Without Discard": np.round(nd,   4)
    })
    st.subheader("With vs. Without Discard")
    st.dataframe(df_cmp, use_container_width=True)
