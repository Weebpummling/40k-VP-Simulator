import streamlit as st
import numpy as np
import random
import pandas as pd

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

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base card definitions (locked VPs, only default probabilities)
# ─────────────────────────────────────────────────────────────────────────────

BASE_CARDS = {
    "Assassination":        {"initial": (5, [20,30,50,70,80]),      "additional": None},
    "Containment":          {"initial": (3, [100,100,100,100,100]), "additional": (3,[100,100,70,60,50])},
    "Behind Enemy Lines":   {"initial": (3, [0,20,30,60,60]),       "additional": (1,[0,0,20,50,60])},
    "Marked for Death":     {"initial": (5, [0,0,20,30,50]),        "additional": None},
    "Bring it Down":        {"initial": (2, [0,50,60,70,80]),       "additional": (2,[0,40,50,60,70])},
    "No Prisoners":         {"initial": (2, [20,80,90,90,90]),      "additional": (2,[0,60,70,80,80])},
    "Defend Stronghold":    {"initial": (3, [0,100,100,100,100]),   "additional": None},
    "Storm Hostile Objective":{"initial": (4,[0,60,70,80,60]),     "additional": None},
    "Sabotage":             {"initial": (3, [100,90,80,70,60]),     "additional": (3,[0,0,0,0,10])},
    "Cull the Horde":       {"initial": (5, [0,0,0,20,30]),         "additional": None},
    "Overwhelming Force":   {"initial": (3, [10,70,70,80,80]),      "additional": (2,[0,30,70,80,70])},
    "Extend Battlelines":   {"initial": (5, [100,100,100,90,90]),    "additional": None},
    "Recover Assets":       {"initial": (3, [100,80,70,60,60]),     "additional": (6,[0,0,20,30,30])},
    "Engage on All Fronts": {"initial": (2, [80,30,50,70,80]),      "additional": (2,[0,30,40,50,60])},
    "Area Denial":          {"initial": (2, [100,80,80,80,80]),     "additional": (3,[80,70,70,70,70])},
    "Secure No Man's Land": {"initial": (2, [100,100,100,100,100]), "additional": (3,[80,80,70,70,70])},
    "Cleanse":              {"initial": (2, [100,100,100,100,100]), "additional": (2,[70,70,70,70,70])},
    "Establish Locus":      {"initial": (2, [100,80,80,80,80]),     "additional": (2,[0,0,40,50,70])},
}

# ─────────────────────────────────────────────────────────────────────────────
# 3) User Interface: card selection & probability inputs
# ─────────────────────────────────────────────────────────────────────────────

st.title("40K Mission VP Simulator")

st.markdown("""
**Step 1:** Select which mission cards to include and set their scoring chances.  
""")

selected = st.multiselect(
    "Select Cards to Include",
    options=list(BASE_CARDS.keys()),
    default=list(BASE_CARDS.keys())
)

# Build card_events from user inputs
card_events = {}
for card in selected:
    cfg = BASE_CARDS[card]
    evs = []

    # Initial VP inputs
    pts_init, default_init = cfg["initial"]
    st.markdown(f"**{card}** — Initial VP: {pts_init}")
    cols = st.columns(5)
    probs_init = []
    for i, col in enumerate(cols, start=1):
        probs_init.append(
            col.number_input(
                f"R{i} chance (%)",
                min_value=0, max_value=100,
                value=default_init[i-1],
                key=f"{card}_init_{i}"
            )
        )
    evs.append((pts_init, probs_init))

    # Additional VP inputs (if any)
    if cfg["additional"]:
        pts_add, default_add = cfg["additional"]
        st.markdown(f"{card} — Additional VP: {pts_add}")
        cols2 = st.columns(5)
        probs_add = []
        for i, col in enumerate(cols2, start=1):
            probs_add.append(
                col.number_input(
                    f"R{i} additional (%)",
                    min_value=0, max_value=100,
                    value=default_add[i-1],
                    key=f"{card}_add_{i}"
                )
            )
        evs.append((pts_add, probs_add))

    card_events[card] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 4) Simulation settings
# ─────────────────────────────────────────────────────────────────────────────

st.sidebar.header("Simulation Settings")
n_trials      = st.sidebar.number_input("Trials", 1000, 200_000, 30_000, 1000)
seed_str      = st.sidebar.text_input("Random Seed (optional)")
if seed_str:
    s = int(seed_str)
    random.seed(s)
    np.random.seed(s)

apply_r1      = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule", True)
allow_discard = st.sidebar.checkbox("Allow Discard/Redraw", True)
round_labels  = [f"Round {i+1}" for i in range(5)]
included      = st.sidebar.multiselect("Include Rounds", round_labels, default=round_labels)
inc_idx       = [round_labels.index(r) for r in included]

forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 5) Precompute EVs for redraw logic
# ─────────────────────────────────────────────────────────────────────────────

card_ev = {c: compute_ev(evs) for c, evs in card_events.items()}

cards_to_redraw = {}
for r in inc_idx:
    pool = [c for c in card_ev if not (r==0 and apply_r1 and c in forbidden_r1)]
    avg_ev = np.mean([card_ev[c][r] for c in pool]) if pool else 0
    cards_to_redraw[f"Round {r+1}"] = sorted([c for c in pool if card_ev[c][r] < avg_ev])

df_redraw = pd.DataFrame({
    "Round": list(cards_to_redraw),
    "Cards to Redraw": [", ".join(cards_to_redraw[r]) for r in cards_to_redraw]
})

# ─────────────────────────────────────────────────────────────────────────────
# 6) Run simulation button
# ─────────────────────────────────────────────────────────────────────────────

run = st.sidebar.button("Run Simulation")
if not run:
    st.info("Adjust card selections, probabilities, and settings, then click ▶️ ‘Run Simulation’.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 7) Monte Carlo Simulation
# ─────────────────────────────────────────────────────────────────────────────

scores = np.zeros((n_trials,5))
for t in range(n_trials):
    discards = set()
    for r in range(5):
        pool = [c for c in card_events if c not in discards]
        if r==0 and apply_r1:
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

        scores[t,r] = sum(score_card(card_events[c], r) for c in hand)

# ─────────────────────────────────────────────────────────────────────────────
# 8) Display Results
# ─────────────────────────────────────────────────────────────────────────────

exp_vp = np.round(scores.mean(axis=0),4)

st.header("Results")
st.subheader("Expected VP by Round")
st.table(pd.DataFrame({
    "Round":       [round_labels[i] for i in inc_idx],
    "Expected VP": exp_vp[inc_idx]
}))

st.subheader("Cards to Redraw by Round")
st.table(df_redraw)

if allow_discard:
    # baseline without discard
    scores_nd = np.zeros_like(scores)
    for t in range(n_trials):
        for r in range(5):
            pool = list(card_events)
            if r==0 and apply_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            if not pool:
                continue
            hand = random.sample(pool,2)
            scores_nd[t,r] = sum(score_card(card_events[c], r) for c in hand)
    nd = np.round(scores_nd.mean(axis=0),4)

    st.subheader("With vs. Without Discard")
    st.table(pd.DataFrame({
        "Round":           [round_labels[i] for i in inc_idx],
        "With Discard":    exp_vp[inc_idx],
        "Without Discard": nd[inc_idx]
    }))
