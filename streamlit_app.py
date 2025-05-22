import streamlit as st
from streamlit import column_config
import pandas as pd
import numpy as np
import random

# ─────────────────────────────────────────────────────────────────────────────
# 1) Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def compute_ev(events):
    """Compute EV per round under independent‐events model (pts × pct/100)."""
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

def validate_probabilities(df):
    """Warn if any percentage column is outside 0–100."""
    pct_cols = [c for c in df.columns if c.endswith("(%)")]
    for col in pct_cols:
        bad = df[(df[col] < 0) | (df[col] > 100)]
        if not bad.empty:
            st.warning(f"Values in “{col}” must be between 0 and 100.")
            break

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base template: exactly one row per card, two VPs locked
# ─────────────────────────────────────────────────────────────────────────────

base_events = {
    "Assassination":        [(5, [20,30,50,70,80])],
    "Containment":          [(3,[100,100,100,100,100]), (3,[100,100,70,60,50])],
    "Behind Enemy Lines":   [(3,[0,20,30,60,60]), (1,[0,0,20,50,60])],
    "Marked for Death":     [(5,[0,0,20,30,50])],
    "Bring it Down":        [(2,[0,50,60,70,80]), (2,[0,40,50,60,70])],
    "No Prisoners":         [(2,[20,80,90,90,90]), (2,[0,60,70,80,80])],
    "Defend Stronghold":    [(3,[0,100,100,100,100])],
    "Storm Hostile Objective": [(4,[0,60,70,80,60])],
    "Sabotage":             [(3,[100,90,80,70,60]), (3,[0,0,0,0,10])],
    "Cull the Horde":       [(5,[0,0,0,20,30])],
    "Overwhelming Force":   [(3,[10,70,70,80,80]), (2,[0,30,70,80,70])],
    "Extend Battlelines":   [(5,[100,100,100,90,90])],
    "Recover Assets":       [(3,[100,80,70,60,60]), (6,[0,0,20,30,30])],
    "Engage on All Fronts": [(2,[80,30,50,70,80]), (2,[0,30,40,50,60])],
    "Area Denial":          [(2,[100,80,80,80,80]), (3,[80,70,70,70,70])],
    "Secure No Man's Land": [(2,[100,100,100,100,100]), (3,[80,80,70,70,70])],
    "Cleanse":              [(2,[100,100,100,100,100]), (2,[70,70,70,70,70])],
    "Establish Locus":      [(2,[100,80,80,80,80]), (2,[0,0,40,50,70])],
}

# Build DataFrame: one row per card
columns = [
    "Active", "Card",
    "Initial VP", *(f"Initial VP R{i} (%)" for i in range(1,6)),
    "Additional VP", *(f"Additional VP R{i} (%)" for i in range(1,6)),
]
rows = []
for card, evs in base_events.items():
    row = {"Active": True, "Card": card}
    # Initial
    pts1, pr1 = evs[0]
    row["Initial VP"] = pts1
    for i in range(5):
        row[f"Initial VP R{i+1} (%)"] = pr1[i]
    # Additional
    if len(evs) > 1:
        pts2, pr2 = evs[1]
    else:
        pts2, pr2 = 0, [0]*5
    row["Additional VP"] = pts2
    for i in range(5):
        row[f"Additional VP R{i+1} (%)"] = pr2[i]
    rows.append(row)

df = pd.DataFrame(rows, columns=columns)

# ─────────────────────────────────────────────────────────────────────────────
# 3) Editable table: lock Card & VP columns, only (%) and Active editable
# ─────────────────────────────────────────────────────────────────────────────

col_config = {}
for col in df.columns:
    if col == "Active":
        col_config[col] = column_config.BooleanColumn(label="Include Card")
    elif col == "Card":
        col_config[col] = column_config.StringColumn(label="Card Name", disabled=True)
    elif col in ("Initial VP", "Additional VP"):
        col_config[col] = column_config.NumberColumn(label=col, disabled=True)
    elif col.endswith("(%)"):
        col_config[col] = column_config.NumberColumn(
            label=col, min_value=0, max_value=100, step=1
        )

edited = st.data_editor(
    df,
    use_container_width=True,
    column_config=col_config,
    hide_index=True,
    key="prob-table"
)
validate_probabilities(edited)

# Parse active cards back into events dict
card_events = {}
for _, r in edited[edited["Active"]].iterrows():
    evs = []
    # Initial
    pts1 = r["Initial VP"]
    probs1 = [r[f"Initial VP R{i} (%)"] for i in range(1,6)]
    evs.append((pts1, probs1))
    # Additional
    pts2 = r["Additional VP"]
    if pts2 > 0:
        probs2 = [r[f"Additional VP R{i} (%)"] for i in range(1,6)]
        evs.append((pts2, probs2))
    card_events[r["Card"]] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 4) Sidebar simulation settings
# ─────────────────────────────────────────────────────────────────────────────

st.sidebar.header("Simulation Settings")
n_trials      = st.sidebar.number_input("Monte Carlo Trials", 1000, 200000, 30000, 1000)
seed_in       = st.sidebar.text_input("Random Seed (optional)")
if seed_in.strip():
    s = int(seed_in); random.seed(s); np.random.seed(s)

reshuffle_r1  = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule", True)
allow_discard = st.sidebar.checkbox("Allow One-Card Discard/Redraw", True)
round_labels  = [f"Round {i+1}" for i in range(5)]
included      = st.sidebar.multiselect("Include Rounds", round_labels, default=round_labels)
included_idx  = [round_labels.index(r) for r in included]

forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 5) Precompute EVs for redraw logic
# ─────────────────────────────────────────────────────────────────────────────

card_ev = {c: compute_ev(events) for c, events in card_events.items()}

cards_to_redraw = {}
for r in included_idx:
    pool = [c for c in card_ev if not (r == 0 and reshuffle_r1 and c in forbidden_r1)]
    avg_ev = np.mean([card_ev[c][r] for c in pool]) if pool else 0
    cards_to_redraw[f"Round {r+1}"] = sorted(c for c in pool if card_ev[c][r] < avg_ev)

df_redraw = pd.DataFrame({
    "Round": list(cards_to_redraw),
    "Cards to Redraw": [", ".join(cards_to_redraw[r]) for r in cards_to_redraw]
})

# ─────────────────────────────────────────────────────────────────────────────
# 6) Monte Carlo simulation
# ─────────────────────────────────────────────────────────────────────────────

scores = np.zeros((n_trials, 5))
for t in range(n_trials):
    discards = set()
    for r in range(5):
        pool = [c for c in card_events if c not in discards]
        if r == 0 and reshuffle_r1:
            pool = [c for c in pool if c not in forbidden_r1]
        if not pool:
            continue
        hand = random.sample(pool, 2)

        if allow_discard:
            evs = [card_ev[c][r] for c in hand]
            rem = [c for c in pool if c not in hand]
            rep_ev = np.mean([card_ev[c][r] for c in rem]) if rem else 0
            if rep_ev > min(evs):
                idx = int(np.argmin(evs))
                discards.add(hand[idx])
                hand[idx] = random.choice(rem) if rem else hand[idx]

        scores[t, r] = sum(score_card(card_events[c], r) for c in hand)

# ─────────────────────────────────────────────────────────────────────────────
# 7) Display results
# ─────────────────────────────────────────────────────────────────────────────

exp_vp = np.round(scores.mean(axis=0), 4)

st.subheader("Expected VP by Round")
st.dataframe(pd.DataFrame({
    "Round":       [round_labels[i] for i in included_idx],
    "Expected VP": exp_vp[included_idx]
}), use_container_width=True)

st.subheader("Cards to Redraw by Round")
st.dataframe(df_redraw, use_container_width=True)

if allow_discard:
    # baseline without discard
    scores_nd = np.zeros_like(scores)
    for t in range(n_trials):
        for r in range(5):
            pool = list(card_events)
            if r == 0 and reshuffle_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            if not pool:
                continue
            hand = random.sample(pool, 2)
            scores_nd[t, r] = sum(score_card(card_events[c], r) for c in hand)
    nd = np.round(scores_nd.mean(axis=0), 4)

    st.subheader("With vs. Without Discard")
    st.dataframe(pd.DataFrame({
        "Round":           [round_labels[i] for i in included_idx],
        "With Discard":    exp_vp[included_idx],
        "Without Discard": nd[included_idx]
    }), use_container_width=True)
