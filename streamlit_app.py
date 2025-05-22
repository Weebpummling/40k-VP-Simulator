import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="40K VP Simulator", layout="wide")
st.title("40K Mission Card VP Simulator")

# ─────────────────────────────────────────────────────────────────────────────
# 1) Helpers
# ─────────────────────────────────────────────────────────────────────────────

def compute_ev_independent(events):
    return [sum(pts * probs[r] for pts, probs in events) for r in range(5)]

def score_card_independent(events, round_idx):
    return sum(pts for pts, probs in events if random.random() < probs[round_idx])

def validate_probabilities(df):
    for col in [f"E{i}_P(R{r})" for i in range(1,MAX_EVENTS+1) for r in range(1,6)]:
        if col in df:
            bad = df[(df[col] < 0) | (df[col] > 1)]
            if not bad.empty:
                st.warning(f"Values in column {col} must be between 0 and 1.")
                return

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base event template
# ─────────────────────────────────────────────────────────────────────────────

base_events = {
    "Assassination":            [(5, [0.20,0.30,0.50,0.70,0.80])],
    "Containment":              [(3, [1,1,1,1,1]), (3, [1,1,0.7,0.6,0.5])],
    "Behind Enemy Lines":       [(3, [0,0.2,0.3,0.6,0.6]), (1, [0,0,0.2,0.5,0.6])],
    "Marked for Death":         [(5, [0,0,0.2,0.3,0.5])],
    "Bring it Down":            [(2, [0,0.5,0.6,0.7,0.8]),
                                 (2, [0,0.4,0.5,0.6,0.7]),
                                 (2, [0,0.1,0.1,0,0]),
                                 (2, [0,0.05,0.05,0,0])],
    "No Prisoners":             [(2, [0.2,0.8,0.9,0.9,0.9]),
                                 (2, [0,0.6,0.7,0.8,0.8]),
                                 (1, [0,0.6,0.7,0.8,0.75])],
    "Defend Stronghold":        [(3, [0,1,1,1,1])],
    "Storm Hostile Objective":  [(4, [0,0.6,0.7,0.8,0.6])],
    "Sabotage":                 [(3, [1,0.9,0.8,0.7,0.6]), (3, [0,0,0,0,0.1])],
    "Cull the Horde":           [(5, [0,0,0,0.2,0.3])],
    "Overwhelming Force":       [(3, [0.1,0.7,0.7,0.8,0.8]), (2, [0,0.3,0.7,0.8,0.7])],
    "Extend Battlelines":       [(5, [1,1,1,0.9,0.9])],
    "Recover Assets":           [(3, [1,0.8,0.7,0.6,0.6]), (6, [0,0,0.2,0.3,0.3])],
    "Engage on All Fronts":     [(2, [0.8,0.3,0.5,0.7,0.8]), (2, [0,0.3,0.4,0.5,0.6])],
    "Area Denial":              [(2, [1,0.8,0.8,0.8,0.8]), (3, [0.8,0.7,0.7,0.7,0.7])],
    "Secure No Man's Land":     [(2, [1,1,1,1,1]), (3, [0.8,0.8,0.7,0.7,0.7])],
    "Cleanse":                  [(2, [1,1,1,1,1]), (2, [0.7,0.7,0.7,0.7,0.7])],
    "Establish Locus":          [(2, [1,0.8,0.8,0.8,0.8]), (2, [0,0,0.4,0.5,0.7])]
}

# determine max events across cards
MAX_EVENTS = max(len(evs) for evs in base_events.values())

# ─────────────────────────────────────────────────────────────────────────────
# 3) Build single-row‐per‐card DataFrame
# ─────────────────────────────────────────────────────────────────────────────

columns = ["Active", "Card"]
for i in range(1, MAX_EVENTS+1):
    columns += [f"E{i}_Points"] + [f"E{i}_P(R{r})" for r in range(1,6)]

rows = []
for card, evs in base_events.items():
    row = {"Active": True, "Card": card}
    for i in range(MAX_EVENTS):
        if i < len(evs):
            pts, probs = evs[i]
        else:
            pts, probs = 0, [0]*5
        row[f"E{i+1}_Points"] = pts
        for r in range(1,6):
            row[f"E{i+1}_P(R{r})"] = probs[r-1]
    rows.append(row)

df = pd.DataFrame(rows, columns=columns)

# show editable table
edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="prob-table")
validate_probabilities(edited)

# parse back into card_events
card_events = {}
for _, r in edited[edited["Active"]].iterrows():
    evs = []
    for i in range(1, MAX_EVENTS+1):
        pts = r[f"E{i}_Points"]
        if pts > 0:
            probs = [r[f"E{i}_P(R{j})"] for j in range(1,6)]
            evs.append((pts, probs))
    card_events[r["Card"]] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 4) Sidebar controls
# ─────────────────────────────────────────────────────────────────────────────

st.sidebar.header("Simulation Settings")
n_trials      = st.sidebar.number_input("Trials",  1000, 200000, 30000, 1000)
seed_in       = st.sidebar.text_input("Random Seed")
if seed_in.strip():
    seed = int(seed_in); random.seed(seed); np.random.seed(seed)

reshuffle_r1  = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule", True)
allow_discard = st.sidebar.checkbox("Allow Discard/Redraw", True)
round_labels  = [f"Round {i+1}" for i in range(5)]
included      = st.sidebar.multiselect("Include Rounds", round_labels, default=round_labels)
included_idx  = sorted(round_labels.index(r) for r in included)

forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 5) Precompute EVs
# ─────────────────────────────────────────────────────────────────────────────

card_ev = {c: compute_ev_independent(evs) for c, evs in card_events.items()}

# compute redraw candidates
cards_to_redraw = {}
for r in included_idx:
    pool = [c for c in card_ev if not (r==0 and reshuffle_r1 and c in forbidden_r1)]
    avg_ev = np.mean([card_ev[c][r] for c in pool]) if pool else 0
    cards_to_redraw[f"Round {r+1}"] = sorted(c for c in pool if card_ev[c][r] < avg_ev)
df_redraw = pd.DataFrame({
    "Round": list(cards_to_redraw.keys()),
    "Cards to Redraw": [", ".join(v) for v in cards_to_redraw.values()]
})

# ─────────────────────────────────────────────────────────────────────────────
# 6) Monte Carlo
# ─────────────────────────────────────────────────────────────────────────────

scores = np.zeros((n_trials, 5))
for t in range(n_trials):
    discards = set()
    for r in range(5):
        pool = [c for c in card_events if c not in discards]
        if r==0 and reshuffle_r1:
            pool = [c for c in pool if c not in forbidden_r1]
        if not pool: continue
        hand = random.sample(pool, 2)

        if allow_discard:
            evs = [card_ev[c][r] for c in hand]
            rem = [c for c in pool if c not in hand]
            rep_ev = np.mean([card_ev[c][r] for c in rem]) if rem else 0
            if rep_ev > min(evs):
                idx = int(np.argmin(evs))
                discards.add(hand[idx])
                hand[idx] = random.choice(rem) if rem else hand[idx]

        scores[t,r] = sum(score_card_independent(card_events[c], r) for c in hand)

# ─────────────────────────────────────────────────────────────────────────────
# 7) Display
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
    # baseline
    scores_nd = np.zeros_like(scores)
    for t in range(n_trials):
        for r in range(5):
            pool = list(card_events)
            if r==0 and reshuffle_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            if not pool: continue
            hand = random.sample(pool, 2)
            scores_nd[t,r] = sum(score_card_independent(card_events[c], r) for c in hand)
    nd = np.round(scores_nd.mean(axis=0), 4)
    st.subheader("With vs. Without Discard")
    st.dataframe(pd.DataFrame({
        "Round":           [round_labels[i] for i in included_idx],
        "With Discard":    exp_vp[included_idx],
        "Without Discard": nd[included_idx]
    }), use_container_width=True)
