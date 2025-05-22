import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="40K VP Simulator", layout="wide")
st.title("40K Mission Card VP Simulator")

st.markdown("""
- **Edit** or **activate/deactivate** any card’s events below.  
- Cards now score *all* of their events independently (so “Additional VPs” truly add on top).  
- You can **include/exclude** rounds, apply the **round-1 reshuffle**, and toggle **discard/redraw**.
""")

# ─────────────────────────────────────────────────────────────────────────────
# 1) Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def compute_ev_independent(events):
    """Return EV for rounds 0–4 by summing pts*pr for each independent event."""
    return [sum(pts * probs[r] for pts, probs in events) for r in range(5)]

def score_card_independent(events, round_idx):
    """Return total VP for this card in round round_idx by sampling each event once."""
    total = 0
    for pts, probs in events:
        if random.random() < probs[round_idx]:
            total += pts
    return total

def validate_probabilities(df):
    # Ensure 0 <= P <= 1
    for c in [f"P(R{i})" for i in range(1,6)]:
        bad = df[(df[c] < 0) | (df[c] > 1)]
        if not bad.empty:
            st.warning(f"Values in column {c} must be between 0 and 1.")
            break

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base template for all cards & events
# ─────────────────────────────────────────────────────────────────────────────

base_events = {
    "Assassination":            [(5, [0.20,0.30,0.50,0.70,0.80])],
    "Containment":              [(3, [1.00,1.00,1.00,1.00,1.00]),
                                 (3, [1.00,1.00,0.70,0.60,0.50])],
    "Behind Enemy Lines":       [(3, [0.00,0.20,0.30,0.60,0.60]),
                                 (1, [0.00,0.00,0.20,0.50,0.60])],
    "Marked for Death":         [(5, [0.00,0.00,0.20,0.30,0.50])],
    "Bring it Down":            [(2, [0.00,0.50,0.60,0.70,0.80]),
                                 (2, [0.00,0.40,0.50,0.60,0.70]),
                                 (2, [0.00,0.10,0.10,0.00,0.00]),
                                 (2, [0.00,0.05,0.05,0.00,0.00])],
    "No Prisoners":             [(2, [0.20,0.80,0.90,0.90,0.90]),
                                 (2, [0.00,0.60,0.70,0.80,0.80]),
                                 (1, [0.00,0.60,0.70,0.80,0.75])],
    "Defend Stronghold":        [(3, [0.00,1.00,1.00,1.00,1.00])],
    "Storm Hostile Objective":  [(4, [0.00,0.60,0.70,0.80,0.60])],
    "Sabotage":                 [(3, [1.00,0.90,0.80,0.70,0.60]),
                                 (3, [0.00,0.00,0.00,0.00,0.10])],
    "Cull the Horde":           [(5, [0.00,0.00,0.00,0.20,0.30])],
    "Overwhelming Force":       [(3, [0.10,0.70,0.70,0.80,0.80]),
                                 (2, [0.00,0.30,0.70,0.80,0.70])],
    "Extend Battlelines":       [(5, [1.00,1.00,1.00,0.90,0.90])],
    "Recover Assets":           [(3, [1.00,0.80,0.70,0.60,0.60]),
                                 (6, [0.00,0.00,0.20,0.30,0.30])],
    "Engage on All Fronts":     [(2, [0.80,0.30,0.50,0.70,0.80]),
                                 (2, [0.00,0.30,0.40,0.50,0.60])],
    "Area Denial":              [(2, [1.00,0.80,0.80,0.80,0.80]),
                                 (3, [0.80,0.70,0.70,0.70,0.70])],
    "Secure No Man's Land":     [(2, [1.00,1.00,1.00,1.00,1.00]),
                                 (3, [0.80,0.80,0.70,0.70,0.70])],
    "Cleanse":                  [(2, [1.00,1.00,1.00,1.00,1.00]),
                                 (2, [0.70,0.70,0.70,0.70,0.70])],
    "Establish Locus":          [(2, [1.00,0.80,0.80,0.80,0.80]),
                                 (2, [0.00,0.00,0.40,0.50,0.70])],
}

# ─────────────────────────────────────────────────────────────────────────────
# 3) Build and edit DataFrame with Active toggle
# ─────────────────────────────────────────────────────────────────────────────

rows = []
for card, evs in base_events.items():
    for pts, probs in evs:
        rows.append({
            "Card": card,
            "Points": pts,
            **{f"P(R{i})": probs[i-1] for i in range(1,6)},
            "Active": True
        })
df = pd.DataFrame(rows)

edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="prob-table")
validate_probabilities(edited)

# Extract only Active rows
card_events = {}
for _, r in edited[edited["Active"]].iterrows():
    card_events.setdefault(r["Card"], []).append(
        (r["Points"], [r[f"P(R{i})"] for i in range(1,6)])
    )

# ─────────────────────────────────────────────────────────────────────────────
# 4) Sidebar controls
# ─────────────────────────────────────────────────────────────────────────────

st.sidebar.header("Simulation Settings")
n_trials      = st.sidebar.number_input("Trials",  1000, 200_000, 30_000, 1000)
seed_in       = st.sidebar.text_input("Random Seed (optional)")
if seed_in.strip():
    seed = int(seed_in)
    random.seed(seed)
    np.random.seed(seed)

reshuffle_r1  = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule",  True)
allow_discard = st.sidebar.checkbox("Allow One‐Card Discard/Redraw", True)
round_labels  = [f"Round {i+1}" for i in range(5)]
included      = st.sidebar.multiselect("Include Rounds", round_labels, default=round_labels)
included_idx  = sorted(round_labels.index(r) for r in included)

forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 5) Precompute EVs (independent model)
# ─────────────────────────────────────────────────────────────────────────────

card_ev = {c: compute_ev_independent(evs) for c, evs in card_events.items()}

# Determine redraw candidates per round
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
# 6) Monte Carlo
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
        # discard/redraw logic
        if allow_discard:
            evs = [card_ev[c][r] for c in hand]
            replacement_ev = np.mean([card_ev[c][r] for c in pool if c not in hand]) if len(pool)>2 else 0
            # if beneficial, swap out lowest-EV card
            idx = int(np.argmin(evs)) if replacement_ev > min(evs) else None
            if idx is not None:
                discards.add(hand[idx])
                hand[idx] = random.choice([c for c in pool if c not in hand])
        # score each card’s independent events
        scores[t, r] = sum(score_card_independent(card_events[c], r) for c in hand)

# ─────────────────────────────────────────────────────────────────────────────
# 7) Display Results
# ─────────────────────────────────────────────────────────────────────────────

exp_vp = np.round(scores.mean(axis=0), 4)

st.subheader("Expected VP by Round")
st.dataframe(
    pd.DataFrame({
        "Round":       [round_labels[i] for i in included_idx],
        "Expected VP": exp_vp[included_idx]
    }),
    use_container_width=True
)

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
            scores_nd[t, r] = sum(score_card_independent(card_events[c], r) for c in hand)
    nd = np.round(scores_nd.mean(axis=0), 4)
    st.subheader("With vs. Without Discard")
    st.dataframe(
        pd.DataFrame({
            "Round":            [round_labels[i] for i in included_idx],
            "With Discard":     exp_vp[included_idx],
            "Without Discard":  nd[included_idx]
        }),
        use_container_width=True
    )
