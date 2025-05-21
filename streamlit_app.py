import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="40K VP Simulator", layout="wide")
st.title("40K Mission Card VP Simulator")

# --- Helper Functions -------------------------------------------------------

def score_card(events, round_idx):
    """Return the single VP scored for this card in round round_idx."""
    # Try highest‐point events first
    for pts, probs in sorted(events, key=lambda ev: ev[0], reverse=True):
        if random.random() < probs[round_idx]:
            return pts
    return 0

def compute_ev(events):
    """
    Given a list of (pts, [p1..p5]) events for one card,
    return list of EVs for rounds 0–4 under the first‐hit model.
    """
    evs = []
    sorted_evs = sorted(events, key=lambda ev: ev[0], reverse=True)
    for r in range(5):
        rem, ev = 1.0, 0.0
        for pts, probs in sorted_evs:
            pr = probs[r]
            ev += pts * pr * rem
            rem *= (1 - pr)
        evs.append(ev)
    return evs

def should_redraw(evs, deck_avg_ev, replacement_ev):
    """
    Given EVs of the two drawn cards, the deck‐avg EV, and the expected
    replacement EV, return index (0 or 1) of drawn card to discard,
    or None if no discard.
    """
    # Only consider discard if replacement EV > card EV
    diffs = [replacement_ev - ev if replacement_ev > ev else 0 for ev in evs]
    if max(diffs) > 0:
        return int(np.argmax(diffs))
    return None

def validate_probabilities(df):
    """
    Ensure all P(R#) in [0,1] and that per-card sums <= 1 each round.
    Warn via st.warning if issues found.
    """
    # Check [0,1]
    for col in [f"P(R{i})" for i in range(1,6)]:
        bad = df[(df[col] < 0) | (df[col] > 1)]
        if not bad.empty:
            st.warning(f"Values in {col} must be between 0 and 1.")
            break

    # Check per-card sum
    grouped = df.groupby("Card")[[f"P(R{i})" for i in range(1,6)]].sum()
    for r in range(1,6):
        over = grouped[grouped[f"P(R{r})"] > 1]
        if not over.empty:
            st.warning(f"For Round {r}, some cards have total P > 1: {', '.join(over.index)}")
            break

# --- 1) Define Base Events -------------------------------------------------

base_events = {
    "Assassination":            [(5, [0.2,0.3,0.5,0.7,0.8])],
    "Containment":              [(3, [1,1,1,1,1]), (6, [1,1,0.7,0.6,0.5])],
    "Behind Enemy Lines":       [(3, [0,0.2,0.3,0.6,0.6]), (4, [0,0,0.2,0.5,0.6])],
    "Marked for Death":         [(5, [0,0,0.2,0.3,0.5])],
    "Bring it Down":            [(2, [0,0.5,0.6,0.7,0.8]),
                                 (4, [0,0.4,0.5,0.6,0.7]),
                                 (6, [0,0.1,0.1,0,0]),
                                 (8, [0,0.05,0.05,0,0])],
    "No Prisoners":             [(2, [0.2,0.8,0.9,0.9,0.9]),
                                 (4, [0,0.6,0.7,0.8,0.8]),
                                 (5, [0,0.6,0.7,0.8,0.75])],
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

# 2) Build DataFrame with Active flag
rows = []
for card, evs in base_events.items():
    for pts, probs in evs:
        rows.append({
            "Card": card, "Points": pts,
            "P(R1)": probs[0], "P(R2)": probs[1],
            "P(R3)": probs[2], "P(R4)": probs[3],
            "P(R5)": probs[4], "Active": True
        })
df = pd.DataFrame(rows)

# 3) Editable table
edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="prob-table")

# Validate probabilities
validate_probabilities(edited)

# 4) Extract active events
card_events = {}
for _, row in edited[edited["Active"]].iterrows():
    c = row["Card"]; p = float(row["Points"])
    probs = [row[f"P(R{i})"] for i in range(1,6)]
    card_events.setdefault(c, []).append((p, probs))

# 5) Sidebar controls
st.sidebar.header("Simulation Settings")
n_trials      = st.sidebar.number_input("Trials", 1000, 100000, 30000, 1000)
seed_input    = st.sidebar.text_input("Random Seed (optional)")
if seed_input.strip():
    seed = int(seed_input)
    random.seed(seed)
    np.random.seed(seed)
reshuffle_r1  = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule", True)
allow_discard = st.sidebar.checkbox("Allow Discard/Redraw", True)

# Select rounds
round_labels  = [f"Round {i+1}" for i in range(5)]
included      = st.sidebar.multiselect("Include Rounds", round_labels, default=round_labels)
included_idx  = sorted(round_labels.index(r) for r in included)

# Round-1 forbidden cards
forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# 6) Compute EV lookup for each card
card_ev = {c: compute_ev(evs) for c, evs in card_events.items()}

# 7) Determine cards to redraw
cards_to_redraw = {}
for r in included_idx:
    pool = [c for c in card_ev if not (r == 0 and reshuffle_r1 and c in forbidden_r1)]
    avg_ev = np.mean([card_ev[c][r] for c in pool]) if pool else 0
    cards_to_redraw[f"Round {r+1}"] = sorted(c for c in pool if card_ev[c][r] < avg_ev)
df_redraw = pd.DataFrame({
    "Round": list(cards_to_redraw.keys()),
    "Cards to Redraw": [", ".join(cards_to_redraw[r]) for r in cards_to_redraw]
})

# 8) Monte Carlo
scores = np.zeros((n_trials, 5))
for t in range(n_trials):
    discards = set()
    for r in range(5):
        pool = [c for c in card_events if c not in discards]
        if r == 0 and reshuffle_r1:
            pool = [c for c in pool if c not in forbidden_r1]
        if not pool:
            continue
        draw = random.sample(pool, 2)
        if allow_discard:
            evs = [card_ev[c][r] for c in draw]
            rem = [c for c in pool if c not in draw]
            replacement_ev = np.mean([card_ev[c][r] for c in rem]) if rem else 0
            idx = should_redraw(evs, np.mean(evs), replacement_ev)
            if idx is not None:
                discards.add(draw[idx])
                draw[idx] = random.choice(rem) if rem else draw[idx]

        # Score each card once
        total = sum(score_card(card_events[c], r) for c in draw)
        scores[t, r] = total

# 9) Display results
exp_vp = np.round(scores.mean(axis=0), 4)

df_result = pd.DataFrame({
    "Round":       [round_labels[i] for i in included_idx],
    "Expected VP": exp_vp[included_idx]
})
st.subheader("Expected VP by Round")
st.dataframe(df_result, use_container_width=True)

st.subheader("Cards to Redraw by Round based on Future Score Probabilities")
st.dataframe(df_redraw, use_container_width=True)

if allow_discard:
    # No-discard baseline
    scores_nd = np.zeros_like(scores)
    for t in range(n_trials):
        for r in range(5):
            pool = list(card_events)
            if r == 0 and reshuffle_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            if not pool:
                continue
            hand = random.sample(pool, 2)
            total = sum(score_card(card_events[c], r) for c in hand)
            scores_nd[t, r] = total
    nd = np.round(scores_nd.mean(axis=0), 4)
    df_cmp = pd.DataFrame({
        "Round":            [round_labels[i] for i in included_idx],
        "With Discard":     exp_vp[included_idx],
        "Without Discard":  nd[included_idx]
    })
    st.subheader("With vs. Without Discard")
    st.dataframe(df_cmp, use_container_width=True)
