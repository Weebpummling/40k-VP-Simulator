import streamlit as st
import pandas as pd
import numpy as np
import random

st.set_page_config(page_title="40K VP Simulator", layout="wide")
st.title("40K Mission Card VP Simulator")

st.markdown("""
**Instructions:**  
- Each row is a mission card.  
- Enter **two** possible scoring events per card.  
- For each event, specify the VP value and the **chance to score in Rounds 1–5** as **percentages** (0–100).  
- Use the **Active** checkbox to include/exclude a card.  
""")

# ─────────────────────────────────────────────────────────────────────────────
# 1) Helpers
# ─────────────────────────────────────────────────────────────────────────────

def compute_ev(events):
    """EV per round = sum(points * probability)"""
    return [sum(pts * (pr/100) for pts, pr in events) for _ in range(5) for pr in []][0:5]  # placeholder

def compute_ev(events):
    return [sum(pts * (pr/100) for pts, pr in events) for r in range(5)]

def score_card(events, r):
    """Score each event independently in round r."""
    total = 0
    for pts, pr in events:
        if random.random() < pr/100:
            total += pts
    return total

# ─────────────────────────────────────────────────────────────────────────────
# 2) Base events
# ─────────────────────────────────────────────────────────────────────────────

base_events = {
    "Assassination":        [(5,[20,30,50,70,80])],
    "Containment":          [(3,[100,100,100,100,100]), (3,[100,100,70,60,50])],
    "Behind Enemy Lines":   [(3,[0,20,30,60,60]), (1,[0,0,20,50,60])],
    "Marked for Death":     [(5,[0,0,20,30,50])],
    "Bring it Down":        [(2,[0,50,60,70,80]), (2,[0,40,50,60,70])],
    "No Prisoners":         [(2,[20,80,90,90,90]), (2,[0,60,70,80,80])],
    "Defend Stronghold":    [(3,[0,100,100,100,100])],
    "Storm Hostile Obj.":   [(4,[0,60,70,80,60])],
    "Sabotage":             [(3,[100,90,80,70,60]), (3,[0,0,0,0,10])],
    "Cull the Horde":       [(5,[0,0,0,20,30])],
    "Overwhelming Force":   [(3,[10,70,70,80,80]), (2,[0,30,70,80,70])],
    "Extend Battlelines":   [(5,[100,100,100,90,90])],
    "Recover Assets":       [(3,[100,80,70,60,60]), (6,[0,0,20,30,30])],
    "Engage on All Fronts": [(2,[80,30,50,70,80]), (2,[0,30,40,50,60])],
    "Area Denial":          [(2,[100,80,80,80,80]), (3,[80,70,70,70,70])],
    "Secure No Man's Land": [(2,[100,100,100,100,100]), (3,[80,80,70,70,70])],
    "Cleanse":              [(2,[100,100,100,100,100]), (2,[70,70,70,70,70])],
    "Establish Locus":      [(2,[100,80,80,80,80]), (2,[0,0,40,50,70])]
}

# find how many cards
cards = list(base_events.keys())

# ─────────────────────────────────────────────────────────────────────────────
# 3) Build editable table: one row per card, two events
# ─────────────────────────────────────────────────────────────────────────────

cols = ["Active", "Card",
        "Initial VP",  "Initial VP R1 (%)", "Initial VP R2 (%)", "Initial VP R3 (%)", "Initial VP R4 (%)", "Initial VP R5 (%)",
        "Additional VP (Simplify to 4 VP max for Bring it Down)",  "Additional VP R1 (%)", "Additional VP R2 (%)", "Additional VP R3 (%)", "Additional VP R4 (%)", "Additional VP R5 (%)"]

rows = []
for card in cards:
    evs = base_events[card]
    row = {"Active": True, "Card": card}
    # fill event 1
    pts1, pr1 = evs[0]
    row["Event 1 VP"]       = pts1
    for i in range(5):
        row[f"Event 1 R{i+1} (%)"] = pr1[i]
    # fill event 2 if exists, else zeros
    if len(evs) > 1:
        pts2, pr2 = evs[1]
    else:
        pts2, pr2 = 0, [0]*5
    row["Event 2 VP"]       = pts2
    for i in range(5):
        row[f"Event 2 R{i+1} (%)"] = pr2[i]
    rows.append(row)

df = pd.DataFrame(rows, columns=cols)
edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="prob-table")
validate_probabilities(edited)

# parse back
card_events = {}
for _, r in edited[edited["Active"]].iterrows():
    ev_list = []
    for e in (1,2):
        pts = r[f"Event {e} VP"]
        if pts > 0:
            probs = [r[f"Event {e} R{i} (%)"] for i in range(1,6)]
            ev_list.append((pts, probs))
    card_events[r["Card"]] = ev_list

# ─────────────────────────────────────────────────────────────────────────────
# 4) Simulation settings
# ─────────────────────────────────────────────────────────────────────────────

st.sidebar.header("Settings")
n_trials      = st.sidebar.number_input("Trials",  1000, 200_000, 30_000, 1000)
seed_in       = st.sidebar.text_input("Random Seed (opt.)")
if seed_in.strip():
    s = int(seed_in); random.seed(s); np.random.seed(s)
reshuffle_r1  = st.sidebar.checkbox("Reshuffle R1 Exclusions", True)
allow_discard = st.sidebar.checkbox("Allow Discard/Redraw", True)
round_labels  = [f"Round {i+1}" for i in range(5)]
included      = st.sidebar.multiselect("Include Rounds", round_labels, default=round_labels)
included_idx  = [round_labels.index(r) for r in included]

forbidden_r1 = {"Storm Hostile Obj.", "Defend Stronghold", "Behind Enemy Lines"}

# ─────────────────────────────────────────────────────────────────────────────
# 5) Precompute EVs (independent model)
# ─────────────────────────────────────────────────────────────────────────────

card_ev = {c: compute_ev(events) for c, events in card_events.items()}

# find redraw candidates
cards_to_redraw = {}
for r in included_idx:
    pool = [c for c in card_ev if not (r==0 and reshuffle_r1 and c in forbidden_r1)]
    avg_ev = np.mean([card_ev[c][r] for c in pool]) if pool else 0
    cards_to_redraw[f"Round {r+1}"] = sorted(c for c in pool if card_ev[c][r] < avg_ev)
df_redraw = pd.DataFrame({
    "Round": list(cards_to_redraw),
    "Cards to Redraw": [", ".join(v) for v in cards_to_redraw.values()]
})

# ─────────────────────────────────────────────────────────────────────────────
# 6) Monte Carlo
# ─────────────────────────────────────────────────────────────────────────────

scores = np.zeros((n_trials,5))
for t in range(n_trials):
    discards = set()
    for r in range(5):
        pool = [c for c in card_events if c not in discards]
        if r==0 and reshuffle_r1:
            pool = [c for c in pool if c not in forbidden_r1]
        if not pool: continue
        hand = random.sample(pool,2)
        if allow_discard:
            evs = [card_ev[c][r] for c in hand]
            rem = [c for c in pool if c not in hand]
            rep_ev = np.mean([card_ev[c][r] for c in rem]) if len(rem)>0 else 0
            if rep_ev > min(evs):
                idx = int(np.argmin(evs))
                discards.add(hand[idx])
                hand[idx] = random.choice(rem) if rem else hand[idx]
        scores[t,r] = sum(score_card(card_events[c], r) for c in hand)

# ─────────────────────────────────────────────────────────────────────────────
# 7) Results
# ─────────────────────────────────────────────────────────────────────────────

exp_vp = np.round(scores.mean(axis=0),4)

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
            hand = random.sample(pool,2)
            scores_nd[t,r] = sum(score_card(card_events[c], r) for c in hand)
    nd = np.round(scores_nd.mean(axis=0),4)
    st.subheader("With vs. Without Discard")
    st.dataframe(pd.DataFrame({
        "Round":           [round_labels[i] for i in included_idx],
        "With Discard":    exp_vp[included_idx],
        "Without Discard": nd[included_idx]
    }), use_container_width=True)
