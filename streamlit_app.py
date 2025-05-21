{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import pandas as pd\
import numpy as np\
import random\
\
st.title("Mission Card VP Simulator")\
\
st.markdown("""\
Upload or edit your card probability data below.  \
**Format**: Each row is one scoring event:  \
- **Card**: card name  \
- **Points**: victory points for this event  \
- **P(R1)** \'85 **P(R5)**: probability to score this point value in each round  \
""")\
\
# Sample template\
template = \{\
    "Card": [\
        "Assassination", "Containment", "Containment", "Behind Enemy Lines", "Behind Enemy Lines"\
    ],\
    "Points": [5, 3, 6, 3, 4],\
    "P(R1)": [0.2, 1.0, 1.0, 0.0, 0.0],\
    "P(R2)": [0.3, 1.0, 1.0, 0.2, 0.0],\
    "P(R3)": [0.5, 1.0, 0.7, 0.3, 0.2],\
    "P(R4)": [0.7, 1.0, 0.6, 0.6, 0.5],\
    "P(R5)": [0.8, 1.0, 0.5, 0.6, 0.6],\
\}\
df = pd.DataFrame(template)\
\
# Let user edit or upload\
uploaded = st.file_uploader("Upload CSV", type="csv")\
if uploaded:\
    df = pd.read_csv(uploaded)\
\
edited = st.experimental_data_editor(df)\
\
# Parse events\
card_events = \{\}\
for _, row in edited.iterrows():\
    card = row["Card"]\
    pts = float(row["Points"])\
    probs = [float(row[f"P(R\{i\})"]) for i in range(1,6)]\
    card_events.setdefault(card, []).append((pts, probs))\
\
st.sidebar.header("Simulation Settings")\
n_trials = st.sidebar.number_input("Trials", value=30000, min_value=1000, step=1000)\
reshape_r1 = st.sidebar.checkbox("Apply Round-1 Reshuffle Rule", value=True)\
allow_discard = st.sidebar.checkbox("Allow One-Card Discard/Redraw", value=True)\
\
# Constants\
forbidden_r1 = \{"Storm Hostile Objective", "Defend Stronghold", "Behind Enemy Lines"\}\
\
# Precompute EV\
card_ev = \{\
    c: [sum(pts * probs[r] for pts, probs in evs) for r in range(5)]\
    for c, evs in card_events.items()\
\}\
\
# Simulation\
scores = np.zeros((n_trials, 5))\
for i in range(n_trials):\
    discards = set()\
    for r in range(5):\
        # available deck\
        pool = [c for c in card_events if c not in discards]\
        if r == 0 and reshape_r1:\
            pool = [c for c in pool if c not in forbidden_r1]\
        draw = random.sample(pool, 2)\
        \
        # optional discard\
        if allow_discard:\
            evs = [card_ev[c][r] for c in draw]\
            remainder = [c for c in pool if c not in draw]\
            rep_ev = np.mean([card_ev[c][r] for c in remainder])\
            if rep_ev > min(evs):\
                # discard lowest EV\
                discard = draw[evs.index(min(evs))]\
                discards.add(discard)\
                kept = draw[1 - evs.index(min(evs))]\
                new = random.choice(remainder)\
                hand = [kept, new]\
            else:\
                hand = draw\
        else:\
            hand = draw\
        \
        # scoring\
        pts = 0\
        for c in hand:\
            for p, probs in card_events[c]:\
                if random.random() < probs[r]:\
                    pts += p\
        scores[i, r] = pts\
\
# Results\
exp_vp = scores.mean(axis=0)\
df_result = pd.DataFrame(\{\
    "Round": [f"Round \{i+1\}" for i in range(5)],\
    "Expected VP": exp_vp\
\})\
st.subheader("Expected VP by Round")\
st.dataframe(df_result)\
\
# If with discard and without discard comparison\
if allow_discard:\
    # Rerun without discard\
    scores_no = np.zeros((n_trials, 5))\
    for i in range(n_trials):\
        for r in range(5):\
            pool = [c for c in card_events]\
            if r == 0 and reshape_r1:\
                pool = [c for c in pool if c not in forbidden_r1]\
            draw = random.sample(pool, 2)\
            pts = 0\
            for c in draw:\
                for p, probs in card_events[c]:\
                    if random.random() < probs[r]:\
                        pts += p\
            scores_no[i, r] = pts\
    exp_no = scores_no.mean(axis=0)\
    df_compare = pd.DataFrame(\{\
        "Round": [f"Round \{i+1\}" for i in range(5)],\
        "With Discard": exp_vp,\
        "No Discard": exp_no\
    \})\
    st.subheader("Comparison: With vs. Without Discard")\
    st.dataframe(df_compare)\
}