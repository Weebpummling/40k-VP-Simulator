import streamlit as st
import numpy as np
import random
import pandas as pd

# ─────────────────────────────────────────────────────────────────────────────
# 0) Starting Bonus
# ─────────────────────────────────────────────────────────────────────────────
START_VP = 10

# ─────────────────────────────────────────────────────────────────────────────
# 1) Probability Categories & Mapping
# ─────────────────────────────────────────────────────────────────────────────
categories = [
    "Guaranteed (100%)",
    "Highly Likely (80%)",
    "Likely (70%)",
    "Maybe (50%)",
    "Unlikely (30%)",
    "Highly Unlikely (10%)"
]
mapping = {c: int(c.split("(")[1].strip("%)")) for c in categories}

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base-card Definitions
# ─────────────────────────────────────────────────────────────────────────────
BASE_CARDS = {
    "Assassination":           {"initial": (5,  [20,30,50,70,80]),       "additional": None},
    "Containment":             {"initial": (3,  [100,100,100,100,100]), "additional": (3,  [100,100,70,60,50])},
    "Behind Enemy Lines":      {"initial": (3,  [0,20,30,60,60]),       "additional": (1,  [0,0,20,50,60])},
    "Marked for Death":        {"initial": (5,  [0,0,20,30,50]),        "additional": None},
    "Bring it Down":           {"initial": (2,  [0,50,60,70,80]),       "additional": (2,  [0,40,50,60,70])},
    "No Prisoners":            {"initial": (2,  [20,80,90,90,90]),      "additional": (2,  [0,60,70,80,80])},
    "Defend Stronghold":       {"initial": (3,  [0,100,100,100,100]),  "additional": None},
    "Storm Hostile Objective": {"initial": (4,  [0,60,70,80,60]),       "additional": None},
    "Sabotage":                {"initial": (3,  [100,90,80,70,60]),     "additional": (3,  [0,0,0,0,10])},
    "Cull the Horde":          {"initial": (5,  [0,0,0,20,30]),         "additional": None},
    "Overwhelming Force":      {"initial": (3,  [10,70,70,80,80]),      "additional": (2,  [0,30,70,80,70])},
    "Extend Battlelines":      {"initial": (5,  [100,100,100,90,90]),    "additional": None},
    "Recover Assets":          {"initial": (3,  [100,80,70,60,60]),     "additional": (6,  [0,0,20,30,30])},
    "Engage on All Fronts":    {"initial": (2,  [80,30,50,70,80]),      "additional": (2,  [0,30,40,50,60])},
    "Area Denial":             {"initial": (2,  [100,80,80,80,80]),     "additional": (3,  [80,70,70,70,70])},
    "Secure No Man's Land":    {"initial": (2,  [100,100,100,100,100]),"additional": (3,  [80,80,70,70,70])},
    "Cleanse":                 {"initial": (2,  [100,100,100,100,100]),"additional": (2,  [70,70,70,70,70])},
    "Establish Locus":         {"initial": (2,  [100,80,80,80,80]),    "additional": (2,  [0,0,40,50,70])},
}
round_labels = [f"Round {i+1}" for i in range(5)]
forbidden_r1 = {"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 3) Prefill session_state Defaults
# ─────────────────────────────────────────────────────────────────────────────
for card, cfg in BASE_CARDS.items():
    # initial
    for j, pct in enumerate(cfg["initial"][1]):
        key = f"{card}_init_{j}"
        if key not in st.session_state:
            st.session_state[key] = min(categories, key=lambda c: abs(mapping[c] - pct))
    # additional
    if cfg["additional"]:
        for j, pct in enumerate(cfg["additional"][1]):
            key = f"{card}_add_{j}"
            if key not in st.session_state:
                st.session_state[key] = min(categories, key=lambda c: abs(mapping[c] - pct))

# ─────────────────────────────────────────────────────────────────────────────
# 4) Helpers
# ─────────────────────────────────────────────────────────────────────────────
def compute_ev(events):
    return [sum(pts * (probs[r] / 100) for pts, probs in events) for r in range(5)]

def score_card(events, r):
    return sum(pts for pts, probs in events if random.random() < probs[r] / 100)

# ─────────────────────────────────────────────────────────────────────────────
# 5) Round Tracker
# ─────────────────────────────────────────────────────────────────────────────
if "current_round" not in st.session_state:
    st.session_state.current_round = 1

c_prev, c_next = st.columns(2)
with c_prev:
    if st.button("Previous Round") and st.session_state.current_round > 1:
        st.session_state.current_round -= 1
with c_next:
    if st.button("Next Round") and st.session_state.current_round < 5:
        st.session_state.current_round += 1

r_idx = st.session_state.current_round - 1
st.markdown(f"## 🕒 Current Round: {st.session_state.current_round}")

# ─────────────────────────────────────────────────────────────────────────────
# 6) Active Missions + Current‐Round Probabilities
# ─────────────────────────────────────────────────────────────────────────────
st.header("🎯 Your Active Missions")
active_current = st.multiselect(
    "Select up to two active missions",
    options=list(BASE_CARDS.keys()),
    default=[],
    key="active_current"
)
if len(active_current) > 2:
    st.error("Please select at most two active missions.")

# these cards get scored now, but excluded later
removed_cards = set(active_current)

for card in active_current:
    cfg = BASE_CARDS[card]
    c1, c2 = st.columns(2)
    key0 = f"{card}_init_{r_idx}"
    c1.selectbox(
        f"{card}: chance to score {cfg['initial'][0]} VP",
        categories,
        index=categories.index(st.session_state[key0]),
        key=key0,
    )
    if cfg["additional"]:
        key1 = f"{card}_add_{r_idx}"
        c2.selectbox(
            f"+{cfg['additional'][0]} VP",
            categories,
            index=categories.index(st.session_state[key1]),
            key=key1,
        )

# ─────────────────────────────────────────────────────────────────────────────
# 7) Discard Recommendation
# ─────────────────────────────────────────────────────────────────────────────
if len(active_current) == 2:
    ev_act = {}
    for c in active_current:
        e = BASE_CARDS[c]["initial"][0] * (mapping[st.session_state[f"{c}_init_{r_idx}"]] / 100)
        if BASE_CARDS[c]["additional"]:
            e += BASE_CARDS[c]["additional"][0] * (mapping[st.session_state[f"{c}_add_{r_idx}"]] / 100)
        ev_act[c] = e

    pool = [c for c in BASE_CARDS if c not in removed_cards]
    ev_pool = []
    for c in pool:
        e0 = BASE_CARDS[c]["initial"][0] * (mapping[st.session_state[f"{c}_init_{r_idx}"]] / 100)
        if BASE_CARDS[c]["additional"]:
            e0 += BASE_CARDS[c]["additional"][0] * (mapping[st.session_state[f"{c}_add_{r_idx}"]] / 100)
        ev_pool.append(e0)
    avg_pool = float(np.mean(ev_pool)) if ev_pool else 0.0

    st.subheader("📣 Discard Recommendation")
    for c, e in ev_act.items():
        action = "DISCARD" if avg_pool > e else "KEEP"
        st.write(f"{c}: EV={e:.2f}, pool avg={avg_pool:.2f} → **{action}**")

# ─────────────────────────────────────────────────────────────────────────────
# 8) Command Points Tracker
# ─────────────────────────────────────────────────────────────────────────────
st.header("🛡️ Command Points")
g_col, s_col = st.columns(2)
cp_gained = g_col.number_input("CP Gained", min_value=0, value=0, step=1)
cp_spent  = s_col.number_input("CP Spent",  min_value=0, value=0, step=1)
st.metric("Net CP", cp_gained - cp_spent)

proj_placeholder = st.container()

# ─────────────────────────────────────────────────────────────────────────────
# 9) Live Scoreboard & Used Cards
# ─────────────────────────────────────────────────────────────────────────────
st.header("📋 Live Scoreboard & Used Cards")
st.markdown("Rounds with Secondary >0 are excluded; Primary is reference only.")

secondary_scores = {}
primary_scores   = {}

# build used-card menus that exclude previously chosen cards
for i in range(1, 6):
    secondary_scores[i] = st.number_input(
        f"Secondary Score R{i}", min_value=0, value=0, step=1, key=f"sec_{i}"
    )
    primary_scores[i]   = st.number_input(
        f"Primary Score   R{i}",   min_value=0, value=0, step=1, key=f"pri_{i}"
    )
    opts = [c for c in BASE_CARDS if c not in removed_cards]
    used = st.multiselect(
        f"Used cards R{i}",
        options=opts,
        key=f"used_{i}"
    )
    removed_cards.update(used)

# scoreboard totals
sec_total = sum(secondary_scores.values())
pri_total = sum(primary_scores.values())

st.markdown("---")
col1, col2, col3 = st.columns(3)
col1.metric("Starting Bonus VP", START_VP)
col2.metric("Secondary Total VP", sec_total)
col3.metric("Primary Total VP",   pri_total)

# simulate rounds strictly after current
future_rounds = [r for r in range(r_idx+1, 5) if secondary_scores[r+1] == 0]

# ─────────────────────────────────────────────────────────────────────────────
# 10) Mission-Probabilities UI for Future Rounds
# ─────────────────────────────────────────────────────────────────────────────
st.header("📈 Mission Card Probabilities (Future Rounds)")

available = [c for c in BASE_CARDS if c not in removed_cards]
selected = st.multiselect(
    "Include in simulation",
    options=available,
    default=available
)

card_events = {}
for card in selected:
    cfg = BASE_CARDS[card]
    evs = []
    st.markdown(f"**{card}** (Initial {cfg['initial'][0]} VP)")
    cols = st.columns(len(future_rounds))
    for idx, r in enumerate(future_rounds):
        key = f"{card}_init_{r}"
        cols[idx].selectbox(
            f"R{r+1}",
            categories,
            index=categories.index(st.session_state[key]),
            key=key
        )
    probs0 = [mapping[st.session_state[f"{card}_init_{j}"]] for j in range(5)]
    evs.append((cfg["initial"][0], probs0))

    if cfg["additional"]:
        st.markdown(f"(+{cfg['additional'][0]} VP)")
        cols2 = st.columns(len(future_rounds))
        for idx, r in enumerate(future_rounds):
            key = f"{card}_add_{r}"
            cols2[idx].selectbox(
                f"R{r+1}+",
                categories,
                index=categories.index(st.session_state[key]),
                key=key
            )
        probs1 = [mapping[st.session_state[f"{card}_add_{j}"]] for j in range(5)]
        evs.append((cfg["additional"][0], probs1))

    card_events[card] = evs

# add active_current to events (for current round only)
for card in active_current:
    cfg = BASE_CARDS[card]
    evs = []
    probs0 = [mapping[st.session_state[f"{card}_init_{j}"]] for j in range(5)]
    evs.append((cfg["initial"][0], probs0))
    if cfg["additional"]:
        probs1 = [mapping[st.session_state[f"{card}_add_{j}"]] for j in range(5)]
        evs.append((cfg["additional"][0], probs1))
    card_events[card] = evs

# ─────────────────────────────────────────────────────────────────────────────
# 11) Sidebar: Simulation Settings & Run
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar.form("settings_form"):
    st.header("Simulation Settings")
    n_trials      = st.number_input("Trials", 1000, 200_000, 30_000, 1000)
    seed_str      = st.text_input("Random Seed (optional)")
    apply_r1      = st.checkbox("Apply R1 Reshuffle", True)
    allow_discard = st.checkbox("Allow Discard/Redraw", True)
    run_sim       = st.form_submit_button("Run Simulation ▶️")

if not run_sim:
    st.stop()

if seed_str:
    random.seed(int(seed_str))
    np.random.seed(int(seed_str))

# ─────────────────────────────────────────────────────────────────────────────
# 12) Monte Carlo Simulation
# ─────────────────────────────────────────────────────────────────────────────
def run_simulation(events):
    ev_lookup = {c: compute_ev(evs) for c, evs in events.items()}

    # redraw suggestions
    redraw = {}
    for r in future_rounds:
        pool = [c for c in ev_lookup if not (r == 0 and apply_r1 and c in forbidden_r1)]
        avg = np.mean([ev_lookup[c][r] for c in pool]) if pool else 0
        redraw[f"Round {r+1}"] = sorted(c for c in pool if ev_lookup[c][r] < avg)

    df_redraw = pd.DataFrame({
        "Round": list(redraw),
        "Cards to Redraw": [", ".join(redraw[r]) for r in redraw]
    })

    # simulate
    scores = np.zeros((n_trials, len(future_rounds)))
    for t in range(n_trials):
        disc = set()
        for i, r in enumerate(future_rounds):
            pool = [c for c in events if c not in disc and c not in active_current]
            if r == 0 and apply_r1:
                pool = [c for c in pool if c not in forbidden_r1]
            if not pool:
                continue
            hand = random.sample(pool, 2)
            if allow_discard:
                evs_list = [ev_lookup[c][r] for c in hand]
                rem      = [c for c in pool if c not in hand]
                rep      = np.mean([ev_lookup[c][r] for c in rem]) if rem else 0
                if rep > min(evs_list):
                    j = int(np.argmin(evs_list))
                    disc.add(hand[j])
                    hand[j] = random.choice(rem) if rem else hand[j]
            scores[t, i] = sum(score_card(events[c], r) for c in hand)
    return scores.mean(axis=0), df_redraw

future_ev, redraw_df = run_simulation(card_events)

# EV of active missions this round
ev_active = sum(
    BASE_CARDS[c]["initial"][0] * (mapping[st.session_state[f"{c}_init_{r_idx}"]] / 100)
    + (BASE_CARDS[c]["additional"][0] * (mapping[st.session_state[f"{c}_add_{r_idx}"]] / 100)
       if BASE_CARDS[c]["additional"] else 0)
    for c in active_current
)

# ─────────────────────────────────────────────────────────────────────────────
# 13) Projection Panel
# ─────────────────────────────────────────────────────────────────────────────
projected_secondary = ev_active + future_ev.sum()
current_vp          = START_VP + sec_total + pri_total
projected_total     = current_vp + projected_secondary

with proj_placeholder:
    st.markdown("## 📊 Projected Victory Points")
    a, b, c = st.columns(3)
    a.metric("Current VP",             f"{current_vp:.0f}")
    b.metric("EV Active Missions",     f"{ev_active:.2f}")
    c.metric("Projected Total VP",     f"{projected_total:.2f}")
    st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# 14) Detailed Results
# ─────────────────────────────────────────────────────────────────────────────
st.header("🎯 Mission VP by Future Rounds")
st.table(pd.DataFrame({
    "Round":       [round_labels[r] for r in future_rounds],
    "Expected VP": np.round(future_ev, 4)
}))
st.subheader("Cards to Redraw by Round")
st.table(redraw_df)
