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

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base card definitions
# ─────────────────────────────────────────────────────────────────────────────

BASE_CARDS = {
    "Assassination":         {"initial": (5, [20,30,50,70,80]),      "additional": None},
    "Containment":           {"initial": (3, [100,100,100,100,100]), "additional": (3,[100,100,70,60,50])},
    "Behind Enemy Lines":    {"initial": (3, [0,20,30,60,60]),       "additional": (1,[0,0,20,50,60])},
    "Marked for Death":      {"initial": (5, [0,0,20,30,50]),        "additional": None},
    "Bring it Down":         {"initial": (2, [0,50,60,70,80]),       "additional": (2,[0,40,50,60,70])},
    "No Prisoners":          {"initial": (2, [20,80,90,90,90]),      "additional": (2,[0,60,70,80,80])},
    "Defend Stronghold":     {"initial": (3, [0,100,100,100,100]),   "additional": None},
    "Storm Hostile Objective":{"initial": (4, [0,60,70,80,60]),     "additional": None},
    "Sabotage":              {"initial": (3, [100,90,80,70,60]),     "additional": (3,[0,0,0,0,10])},
    "Cull the Horde":        {"initial": (5, [0,0,0,20,30]),         "additional": None},
    "Overwhelming Force":    {"initial": (3, [10,70,70,80,80]),      "additional": (2,[0,30,70,80,70])},
    "Extend Battlelines":    {"initial": (5, [100,100,100,90,90]),    "additional": None},
    "Recover Assets":        {"initial": (3, [100,80,70,60,60]),     "additional": (6,[0,0,20,30,30])},
    "Engage on All Fronts":  {"initial": (2, [80,30,50,70,80]),      "additional": (2,[0,30,40,50,60])},
    "Area Denial":           {"initial": (2, [100,80,80,80,80]),     "additional": (3,[80,70,70,70,70])},
    "Secure No Man's Land":  {"initial": (2, [100,100,100,100,100]), "additional": (3,[80,80,70,70,70])},
    "Cleanse":               {"initial": (2, [100,100,100,100,100]), "additional": (2,[70,70,70,70,70])},
    "Establish Locus":       {"initial": (2, [100,80,80,80,80]),     "additional": (2,[0,0,40,50,70])},
}

round_labels = [f"Round {i+1}" for i in range(5)]
forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 3) Scoreboard & used‐cards input per round
# ─────────────────────────────────────────────────────────────────────────────

st.header("Scoreboard & Cards Used")

# Probability categories mapping
categories = [
    "Guaranteed (100%)",
    "Highly Likely (80%)",
    "Likely (70%)",
    "Maybe (50%)",
    "Unlikely (30%)",
    "Highly Unlikely (10%)"
]
mapping = {
    "Guaranteed (100%)": 100,
    "Highly Likely (80%)": 80,
    "Likely (70%)": 70,
    "Maybe (50%)": 50,
    "Unlikely (30%)": 30,
    "Highly Unlikely (10%)": 10
}

secondary_scores = {}
removed_cards_all = set()

for i in range(1, 6):
    st.subheader(f"Round {i}")
    c1, c2 = st.columns([2,4])
    choice = c1.selectbox(
        f"Secondary Score R{i}",
        options=categories,
        index=3,  # default "Maybe"
        key=f"sec_{i}"
    )
    secondary_scores[i] = mapping[choice]
    used = c2.multiselect(
        f"Cards used in R{i} (remove from pool)",
        options=list(BASE_CARDS.keys()),
        key=f"used_{i}"
    )
    removed_cards_all.update(used)

# ─────────────────────────────────────────────────────────────────────────────
# 4) Your mission‐cards input
# ─────────────────────────────────────────────────────────────────────────────

st.header("Your Mission Cards")

available_cards = [c for c in BASE_CARDS if c not in removed_cards_all]
selected = st.multiselect(
    "Choose your cards",
    options=available_cards,
    default=available_cards
)

card_events = {}
for card in selected:
    cfg = BASE_CARDS[card]
    evs = []
    st.markdown(f"**{card}** — Initial VP: {cfg['initial'][0]}")
    cols = st.columns(5)
    probs = [
        mapping[cols[j].selectbox(
            f"R{j+1} chance",
            options=categories,
            index=categories.index("Guaranteed (100%)" if cfg['initial'][1][j]==100 else
                                     "Highly Likely (80%)" if cfg['initial'][1][j]==80 else
                                     "Likely (70%)" if cfg['initial'][1][j]==70 else
                                     "Maybe (50%)" if cfg['initial'][1][j]==50 else
                                     "Unlikely (30%)"),
            key=f"{card}_init_{j}"
        )]
        for j in range(5)
    ]
    evs.append((cfg['initial'][0], probs))
    if cfg['additional']:
        st.markdown(f"{card} — Additional VP: {cfg['additional'][0]}")
        cols2 = st.columns(5)
        probs2 = [
            mapping[cols2[j].selectbox(
                f"R{j+1} additional",
                options=categories,
                index=categories.index("Guaranteed (100%)" if cfg['additional'][1][j]==100 else
                                         "Highly Likely (80%)" if cfg['additional'][1][j]==80 else
                                         "Likely (70%)" if cfg['additional'][1][j]==70 else
                                         "Maybe (50%)" if cfg['additional'][1][j]==50 else
                                         "Unlikely (30%)"),
                key=f"{card}_add_{j}"
            )]
            for j in range(5)
        ]
        evs.append((cfg['additional'][0], probs2))
    card_events[card] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 5) Sidebar form: settings + run guard
# ─────────────────────────────────────────────────────────────────────────────

with st.sidebar.form("settings_form"):
    st.header("Simulation Settings")
    n_trials      = st.number_input("Trials", 1000, 200_000, 30_000, 1000)
    seed_str      = st.text_input("Random Seed (optional)")
    apply_r1      = st.checkbox("Apply Round-1 Reshuffle Rule", True)
    allow_discard = st.checkbox("Allow Discard/Redraw", True)
    included      = st.multiselect("Include Rounds", round_labels, default=round_labels)
    run_sim       = st.form_submit_button("Run Simulation ▶️")

if not run_sim:
    st.info("Configure inputs above, then click ▶️ Run Simulation.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# 6) Parse settings & prepare
# ─────────────────────────────────────────────────────────────────────────────

if seed_str:
    random.seed(int(seed_str)); np.random.seed(int(seed_str))

included_idx = [round_labels.index(r) for r in included]

# ─────────────────────────────────────────────────────────────────────────────
# 7) Simulation helper
# ─────────────────────────────────────────────────────────────────────────────

def run_simulation(card_events):
    ev_lookup = {c: compute_ev(evs) for c, evs in card_events.items()}
    # Cards to redraw
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

mission_ev, redraw_df = run_simulation(card_events)

# ─────────────────────────────────────────────────────────────────────────────
# 8) Display results
# ─────────────────────────────────────────────────────────────────────────────

st.header("Results — Your Side")
st.subheader("Mission VP by Round")
st.table(pd.DataFrame({
    "Round":       [f"Round {i+1}" for i in included_idx],
    "Expected VP": np.round(mission_ev[included_idx], 4)
}))

st.subheader("Cards to Redraw by Round")
st.table(redraw_df)

# ─────────────────────────────────────────────────────────────────────────────
# 9) Total Expected VP (including scoreboard)
# ─────────────────────────────────────────────────────────────────────────────

mission_total      = mission_ev[included_idx].sum()
secondary_total    = sum(secondary_scores.values())
combined_total     = mission_total + secondary_total

st.markdown("---")
c1, c2, c3 = st.columns(3)
c1.metric("Mission VP Total",   f"{mission_total:.2f}")
c2.metric("Secondary Score Total", f"{secondary_total:.2f}")
c3.metric("Overall Combined VP",   f"{combined_total:.2f}")
