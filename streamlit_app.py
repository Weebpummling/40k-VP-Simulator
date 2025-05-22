import streamlit as st
import pandas as pd
import numpy as np
import random
import io
import copy

# ─────────────────────────────────────────────────────────────────────────────
# Constants & Configuration
# ─────────────────────────────────────────────────────────────────────────────
MAX_ROUNDS = 5
START_VP   = 10
MAX_PRIMARY_SCORE = 50
MAX_SECONDARY_SCORE = 40


CATEGORIES = ["100%","80%","50%","30%","<10%"]
PCT_MAP    = {"100%":100,"80%":80,"50%":50,"30%":30,"<10%":10}

DEFAULT_PROBS = {
    "Assassination":        [(5, [20, 30, 50, 70, 80])],
    "Containment":          [(3, [100, 100, 100, 100, 100]), (3, [100, 100, 80, 50, 50])],
    "Behind Enemy Lines":   [(3, [0, 10, 30, 50, 80]), (1, [0, 0, 30, 50, 80])],
    "Marked for Death":     [(5, [0, 0, 20, 30, 50])],
    "Bring it Down":        [(2, [0, 50, 80, 80, 80]), (2, [0, 30, 50, 50, 50])],
    "No Prisoners":         [(2, [20, 80, 100, 100, 100]), (2, [0, 50, 80, 80, 80]), (1, [0, 50, 80, 80, 80])],
    "Defend Stronghold":    [(3, [0, 100, 100, 100, 100])],
    "Storm Hostile Objective": [(4, [0, 50, 80, 80, 50])],
    "Sabotage":             [(3, [100, 80, 80, 50, 50]), (3, [0, 0, 0, 0, 10])],
    "Cull the Horde":       [(5, [0, 0, 0, 10, 30])],
    "Overwhelming Force":   [(3, [10, 80, 80, 80, 80]), (2, [0, 30, 80, 80, 80])],
    "Extend Battlelines":   [(5, [100, 100, 100, 100, 100])],
    "Recover Assets":       [(3, [100, 80, 80, 50, 50]), (6, [0, 0, 30, 30, 30])],
    "Engage on All Fronts": [(2, [80, 30, 50, 80, 80]), (2, [0, 30, 30, 50, 50])], 
    "Area Denial":          [(2, [100, 80, 80, 80, 80]), (3, [80, 80, 80, 80, 80])],
    "Secure No Man's Land": [(2, [100, 100, 100, 100, 100]), (3, [80, 80, 80, 80, 80])],
    "Cleanse":              [(2, [100, 100, 100, 100, 100]), (2, [80, 80, 80, 80, 80])],
    "Establish Locus":      [(2, [100, 80, 80, 80, 80]), (2, [0, 0, 40, 50, 80])]
}
CARD_LIST = sorted(list(DEFAULT_PROBS.keys()))
MAX_EVENTS = max(len(evs) for evs in DEFAULT_PROBS.values()) if DEFAULT_PROBS else 1

COL_EVENT_PTS_TPL = "E{}_pts"
COL_EVENT_ROUND_PROB_TPL = "E{}_r{}"

# ─────────────────────────────────────────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────────────────────────────────────────
if 'PROB_EVENTS' not in st.session_state: # User's probabilities
    st.session_state.PROB_EVENTS = copy.deepcopy(DEFAULT_PROBS)
if 'OPPONENT_PROB_EVENTS' not in st.session_state: # Opponent's probabilities
    st.session_state.OPPONENT_PROB_EVENTS = copy.deepcopy(DEFAULT_PROBS)


default_round_data = {
    's1': 0, 's2': 0, 'p': 0, 'used': [],
    'opp_s1': 0, 'opp_s2': 0, 'opp_p': 0, 'opp_used': []
}
if 'scoreboard_data_list' not in st.session_state:
    st.session_state.scoreboard_data_list = [copy.deepcopy(default_round_data) for _ in range(MAX_ROUNDS)]
else:
    for i in range(len(st.session_state.scoreboard_data_list)):
        for key, default_value in default_round_data.items():
            if isinstance(default_value, list):
                 st.session_state.scoreboard_data_list[i].setdefault(key, list(default_value))
            else:
                 st.session_state.scoreboard_data_list[i].setdefault(key, default_value)
    
    while len(st.session_state.scoreboard_data_list) < MAX_ROUNDS:
        st.session_state.scoreboard_data_list.append(copy.deepcopy(default_round_data))
    if len(st.session_state.scoreboard_data_list) > MAX_ROUNDS:
        st.session_state.scoreboard_data_list = st.session_state.scoreboard_data_list[:MAX_ROUNDS]


if 'active_current' not in st.session_state:
    st.session_state.active_current = []
if 'manually_removed_cards' not in st.session_state:
    st.session_state.manually_removed_cards = set() 

if 'scoreboard_used_cards' not in st.session_state: 
    st.session_state.scoreboard_used_cards = set() 
if 'opponent_scoreboard_used_cards' not in st.session_state:
    st.session_state.opponent_scoreboard_used_cards = set() 

if 'active_mission_overrides' not in st.session_state:
    st.session_state.active_mission_overrides = {} 
if 'last_known_cur_round_for_overrides' not in st.session_state:
    st.session_state.last_known_cur_round_for_overrides = -1
if 'last_known_active_cards_for_overrides' not in st.session_state:
    st.session_state.last_known_active_cards_for_overrides = []

if 'include_start_vp' not in st.session_state:
    st.session_state.include_start_vp = True
if 'current_active_hand_ev' not in st.session_state:
    st.session_state.current_active_hand_ev = 0.0
if 'total_sim_future_vp' not in st.session_state: 
    st.session_state.total_sim_future_vp = 0.0
if 'opponent_total_sim_future_vp' not in st.session_state: 
    st.session_state.opponent_total_sim_future_vp = 0.0


# ─────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ─────────────────────────────────────────────────────────────────────────────
def find_closest_category(prob_val, categories_list, pct_map):
    """Finds the string category in categories_list closest to prob_val."""
    if f"{prob_val}%" in categories_list: return f"{prob_val}%"
    min_diff, closest_cat_str = float('inf'), categories_list[-1]
    for cat_str in categories_list:
        cat_val = pct_map.get(cat_str, 0)
        diff = abs(prob_val - cat_val)
        if diff < min_diff: min_diff, closest_cat_str = diff, cat_str
        elif diff == min_diff and pct_map.get(cat_str,0) > pct_map.get(closest_cat_str,0): closest_cat_str = cat_str
    return closest_cat_str

def calculate_card_ev_for_round(card_name, round_idx, prob_events_data):
    """Calculates Expected Value for a single card for a specific round using baseline probabilities."""
    ev = 0
    if card_name in prob_events_data:
        for pts, prs_list in prob_events_data[card_name]:
            if 0 <= round_idx < len(prs_list):
                ev += pts * (prs_list[round_idx] / 100.0)
    return ev

def calculate_hand_ev_for_round(hand, round_idx, prob_events_data, overrides=None):
    """Calculates Expected Value for a hand for a specific round, considering overrides."""
    ev = 0
    if not hand or not prob_events_data: return 0
    for card_name in hand:
        if card_name in prob_events_data:
            for event_i, (pts, prs_list) in enumerate(prob_events_data[card_name]):
                if 0 <= round_idx < len(prs_list):
                    default_prob_pct = prs_list[round_idx]
                    override_key = f"override_{card_name}_E{event_i+1}_R{round_idx+1}" 
                    
                    current_prob_pct = default_prob_pct
                    if overrides and override_key in overrides:
                        current_prob_pct = overrides[override_key] 
                    
                    ev += pts * (current_prob_pct / 100.0)
    return ev

def calculate_opponent_future_secondary_vp(current_round_0_indexed, opponent_used_cards_set, opponent_prob_events_data, current_opponent_sec_score):
    """Calculates a projected future secondary VP for the opponent, respecting 40 VP cap."""
    projected_vp_raw = 0
    temp_opponent_used_cards = set(opponent_used_cards_set) 

    for r_idx in range(current_round_0_indexed + 1, MAX_ROUNDS):
        if current_opponent_sec_score + projected_vp_raw >= MAX_SECONDARY_SCORE:
            break # Stop if already at or over cap

        available_cards_for_opponent_this_round = [
            c for c in CARD_LIST if c not in temp_opponent_used_cards
        ]
        
        if not available_cards_for_opponent_this_round:
            continue

        card_evs_this_round = []
        for card in available_cards_for_opponent_this_round:
            ev = calculate_card_ev_for_round(card, r_idx, opponent_prob_events_data) # Use opponent's probs
            card_evs_this_round.append({"name": card, "ev": ev})
        
        card_evs_this_round.sort(key=lambda x: x["ev"], reverse=True)
        
        round_score_opponent = 0
        cards_chosen_this_round_opponent = []
        for i in range(min(2, len(card_evs_this_round))):
            chosen_card = card_evs_this_round[i]
            # Ensure adding this EV doesn't exceed the cap when combined with already scored and previously projected VPs for this function call
            if current_opponent_sec_score + projected_vp_raw + chosen_card["ev"] <= MAX_SECONDARY_SCORE:
                round_score_opponent += chosen_card["ev"]
            else: # Add only enough to reach the cap
                round_score_opponent += max(0, MAX_SECONDARY_SCORE - (current_opponent_sec_score + projected_vp_raw))
                cards_chosen_this_round_opponent.append(chosen_card["name"]) # Still "uses" the card
                projected_vp_raw += round_score_opponent
                break # Cap reached for this round's picks
            
            cards_chosen_this_round_opponent.append(chosen_card["name"])
            
        projected_vp_raw += round_score_opponent
        temp_opponent_used_cards.update(cards_chosen_this_round_opponent) 

    return min(projected_vp_raw, MAX_SECONDARY_SCORE - current_opponent_sec_score)


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar Settings
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.header("General Settings")
st.session_state.include_start_vp = st.sidebar.checkbox(
    "Include Starting VP (10 VP) in Totals", 
    value=st.session_state.include_start_vp,
    key="include_start_vp_checkbox"
)
st.sidebar.divider() 

st.sidebar.header("Probability Profiles")
upload = st.sidebar.file_uploader("Import settings CSV", type="csv")
if upload:
    try:
        df_up = pd.read_csv(upload, index_col=0)
        imported, malformed_entries = {}, []
        for card_name, row in df_up.iterrows():
            evs, valid_card, num_events_csv = [], True, 0
            for i in range(1, MAX_EVENTS + 1):
                pts_col, pts = COL_EVENT_PTS_TPL.format(i), row.get(COL_EVENT_PTS_TPL.format(i))
                if pd.notna(pts) and pts > 0:
                    num_events_csv += 1; round_cols = [COL_EVENT_ROUND_PROB_TPL.format(i, r + 1) for r in range(MAX_ROUNDS)]
                    missing_round_cols = [rc for rc in round_cols if rc not in row.index or pd.isna(row[rc])]
                    if missing_round_cols: malformed_entries.append(f"'{card_name}' E{i}: missing {missing_round_cols}"); valid_card = False; break
                    prs = [int(row.get(rc, 0)) for rc in round_cols]; evs.append((int(pts), prs))
            if valid_card and evs:
                imported[card_name] = evs
                if card_name in DEFAULT_PROBS and len(evs) != len(DEFAULT_PROBS[card_name]): st.sidebar.warning(f"'{card_name}': imported {len(evs)} vs default {len(DEFAULT_PROBS[card_name])} events.")
            elif not evs and valid_card and card_name in df_up.index: malformed_entries.append(f"'{card_name}': No valid events.")
        if malformed_entries: st.sidebar.error("CSV malformed. Not fully loaded. Errors:\n- " + "\n- ".join(malformed_entries))
        if imported: 
            st.session_state.PROB_EVENTS = imported
            st.sidebar.success("Profile imported!")
            st.rerun() 
        elif not malformed_entries : st.sidebar.warning("CSV empty or no valid data.")
    except Exception as e: st.sidebar.error(f"Error processing CSV: {e}")

out_export = {}
for card, evs in st.session_state.PROB_EVENTS.items():
    rec = {};
    for idx, (pts, prs) in enumerate(evs, start=1):
        rec[COL_EVENT_PTS_TPL.format(idx)] = pts
        for r_loop_idx, p_val in enumerate(prs, start=1): rec[COL_EVENT_ROUND_PROB_TPL.format(idx, r_loop_idx)] = p_val 
    out_export[card] = rec
df_out = pd.DataFrame(out_export).T.fillna(0).astype(int); csv_buffer = io.StringIO(); df_out.to_csv(csv_buffer)
st.sidebar.download_button("Export Current Profile as CSV", csv_buffer.getvalue(), "probs.csv", "text/csv")
st.sidebar.divider()

# ─────────────────────────────────────────────────────────────────────────────
# UI: Edit per-round probabilities
# ─────────────────────────────────────────────────────────────────────────────
st.header("⚙️ Edit Mission Probabilities (Baseline)")
with st.expander("Show/hide probability table"):
    updated_probs_edit = copy.deepcopy(st.session_state.PROB_EVENTS)
    
    temp_calculated_cur_round_for_edit = 0
    for i_edit_cur_round, round_data_edit_cur_round in enumerate(st.session_state.scoreboard_data_list):
        if round_data_edit_cur_round['s1'] > 0 or round_data_edit_cur_round['s2'] > 0 or round_data_edit_cur_round['used']:
            if i_edit_cur_round < MAX_ROUNDS - 1: temp_calculated_cur_round_for_edit = i_edit_cur_round + 1
            else: temp_calculated_cur_round_for_edit = MAX_ROUNDS - 1
        else: break
    cur_round_for_edit_display = temp_calculated_cur_round_for_edit


    for card, evs in st.session_state.PROB_EVENTS.items():
        st.markdown(f"**{card}**"); new_evs_for_card = []
        for event_idx, (pts, prs_list) in enumerate(evs, start=1):
            num_future_rounds = MAX_ROUNDS - cur_round_for_edit_display
            num_cols_to_create = 1 + num_future_rounds if num_future_rounds > 0 else 1
            
            cols = st.columns(num_cols_to_create)
            cols[0].markdown(f"*VP: {pts}*")
            new_prs_for_event = list(prs_list) 

            if num_future_rounds > 0:
                col_idx_offset = 1 
                for r_game_round_0_indexed in range(cur_round_for_edit_display, MAX_ROUNDS):
                    r_game_round_1_indexed = r_game_round_0_indexed + 1
                    
                    prob_val = prs_list[r_game_round_0_indexed]
                    key = f"edit_{card}_E{event_idx}_r{r_game_round_1_indexed}"
                    default_cat_str = find_closest_category(prob_val, CATEGORIES, PCT_MAP)
                    
                    choice = cols[col_idx_offset].selectbox(
                        f"R{r_game_round_1_indexed}", 
                        CATEGORIES, 
                        index=CATEGORIES.index(default_cat_str), 
                        key=key, 
                        label_visibility="visible" 
                    )
                    new_prs_for_event[r_game_round_0_indexed] = PCT_MAP.get(choice, 10) 
                    col_idx_offset += 1
            
            new_evs_for_card.append((pts, new_prs_for_event))
        updated_probs_edit[card] = new_evs_for_card
        
    if st.button("Apply Baseline Probability Changes"):
        st.session_state.PROB_EVENTS = updated_probs_edit
        st.success("Baseline Probabilities updated!")
        st.rerun() 

# ─────────────────────────────────────────────────────────────────────────────
# Live Scoreboard & Round Detection
# ─────────────────────────────────────────────────────────────────────────────
st.header("📋 Live Scoreboard & Current Round")

current_scoreboard_used_cards_set = set()
for round_data_sb_init in st.session_state.scoreboard_data_list: 
    current_scoreboard_used_cards_set.update(round_data_sb_init.get('used', []))
if current_scoreboard_used_cards_set != st.session_state.scoreboard_used_cards:
    st.session_state.scoreboard_used_cards = current_scoreboard_used_cards_set

current_opponent_scoreboard_used_cards_set = set()
for round_data_sb_init_opp in st.session_state.scoreboard_data_list:
    current_opponent_scoreboard_used_cards_set.update(round_data_sb_init_opp.get('opp_used', []))
if current_opponent_scoreboard_used_cards_set != st.session_state.opponent_scoreboard_used_cards:
    st.session_state.opponent_scoreboard_used_cards = current_opponent_scoreboard_used_cards_set


calculated_cur_round = 0 
for i_sb_round, round_data_sb_cur in enumerate(st.session_state.scoreboard_data_list): 
    if round_data_sb_cur['s1'] > 0 or round_data_sb_cur['s2'] > 0 or round_data_sb_cur['used']:
        if i_sb_round < MAX_ROUNDS - 1: 
            calculated_cur_round = i_sb_round + 1
        else: 
            calculated_cur_round = MAX_ROUNDS - 1 
    else: 
        break 
cur_round = calculated_cur_round 

total_s1, total_s2, total_p_raw = 0, 0, 0 # Renamed total_p to total_p_raw
opp_total_s1, opp_total_s2, opp_total_p_raw = 0, 0, 0 # Renamed opp_total_p

for i_sb_form in range(MAX_ROUNDS): 
    with st.container(border=True): 
        st.subheader(f"Round {i_sb_form+1}")
        
        st.markdown("**Your Scores**")
        user_cols = st.columns([1,1,1,2])
        round_data_form = st.session_state.scoreboard_data_list[i_sb_form] 

        round_data_form['s1'] = user_cols[0].number_input(f"Your Sec 1 VP (R{i_sb_form+1})", min_value=0, max_value=15, value=round_data_form.get('s1',0), key=f"s1_r{i_sb_form}", label_visibility="collapsed", help="Your Secondary 1 VPs for this round")
        round_data_form['s2'] = user_cols[1].number_input(f"Your Sec 2 VP (R{i_sb_form+1})", min_value=0, max_value=15, value=round_data_form.get('s2',0), key=f"s2_r{i_sb_form}", label_visibility="collapsed", help="Your Secondary 2 VPs for this round")
        round_data_form['p'] = user_cols[2].number_input(f"Your Primary VP (R{i_sb_form+1})", min_value=0, max_value=20, value=round_data_form.get('p',0), key=f"p_r{i_sb_form}", label_visibility="collapsed", help="Your Primary VPs for this round")
        
        other_rounds_used_cards = set()
        for r_idx_sb_options, r_data_sb_options in enumerate(st.session_state.scoreboard_data_list): 
            if r_idx_sb_options != i_sb_form: other_rounds_used_cards.update(r_data_sb_options.get('used',[]))
        
        card_options_for_this_round_user = [c for c in CARD_LIST if c not in other_rounds_used_cards]
        card_options_for_this_round_user = sorted(list(set(card_options_for_this_round_user + round_data_form.get('used',[]))))

        round_data_form['used'] = user_cols[3].multiselect(f"Your Cards Used (R{i_sb_form+1})", options=card_options_for_this_round_user, default=round_data_form.get('used',[]), key=f"used_r{i_sb_form}", placeholder="Select your scored cards", label_visibility="collapsed", help="Your Secondary cards scored/revealed this round")
        
        total_s1 += round_data_form.get('s1',0); total_s2 += round_data_form.get('s2',0); total_p_raw += round_data_form.get('p',0)
        
        st.markdown("---") 
        st.markdown("**Opponent's Scores**")
        opp_cols = st.columns([1,1,1,2])
        round_data_form['opp_s1'] = opp_cols[0].number_input(f"Opp Sec 1 VP (R{i_sb_form+1})", min_value=0, max_value=15, value=round_data_form.get('opp_s1',0), key=f"opp_s1_r{i_sb_form}", label_visibility="collapsed", help="Opponent's Secondary 1 VPs")
        round_data_form['opp_s2'] = opp_cols[1].number_input(f"Opp Sec 2 VP (R{i_sb_form+1})", min_value=0, max_value=15, value=round_data_form.get('opp_s2',0), key=f"opp_s2_r{i_sb_form}", label_visibility="collapsed", help="Opponent's Secondary 2 VPs")
        round_data_form['opp_p'] = opp_cols[2].number_input(f"Opp Primary VP (R{i_sb_form+1})", min_value=0, max_value=20, value=round_data_form.get('opp_p',0), key=f"opp_p_r{i_sb_form}", label_visibility="collapsed", help="Opponent's Primary VPs")

        opp_other_rounds_used_cards = set()
        for r_idx_opp_options, r_data_opp_options in enumerate(st.session_state.scoreboard_data_list):
            if r_idx_opp_options != i_sb_form: opp_other_rounds_used_cards.update(r_data_opp_options.get('opp_used',[]))
        
        card_options_for_opp_this_round = [c for c in CARD_LIST if c not in opp_other_rounds_used_cards]
        card_options_for_opp_this_round = sorted(list(set(card_options_for_opp_this_round + round_data_form.get('opp_used',[]))))

        round_data_form['opp_used'] = opp_cols[3].multiselect(f"Opp Cards Used (R{i_sb_form+1})", options=card_options_for_opp_this_round, default=round_data_form.get('opp_used',[]), key=f"opp_used_r{i_sb_form}", placeholder="Select opponent's cards", label_visibility="collapsed", help="Opponent's Secondary cards scored/revealed")

        opp_total_s1 += round_data_form.get('opp_s1',0); opp_total_s2 += round_data_form.get('opp_s2',0); opp_total_p_raw += round_data_form.get('opp_p',0)
        
        st.session_state.scoreboard_data_list[i_sb_form] = round_data_form

st.write(f"**Current Game Round (for active play):** {cur_round+1} (Internal 0-indexed: {cur_round})")

# Apply VP Caps
sec_total = min(total_s1 + total_s2, MAX_SECONDARY_SCORE)
pri_total = min(total_p_raw, MAX_PRIMARY_SCORE)
opp_sec_total = min(opp_total_s1 + opp_total_s2, MAX_SECONDARY_SCORE)
opp_pri_total = min(opp_total_p_raw, MAX_PRIMARY_SCORE)

st.session_state.opponent_total_sim_future_vp = calculate_opponent_future_secondary_vp(
    cur_round, st.session_state.opponent_scoreboard_used_cards, st.session_state.OPPONENT_PROB_EVENTS, opp_sec_total
)

# ─────────────────────────────────────────────────────────────────────────────
# Card Pool Management
# ─────────────────────────────────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.header("Card Deck Management (Your Deck)")
st.sidebar.write("**Your Scoreboard Used Cards:**")
if st.session_state.scoreboard_used_cards: st.sidebar.write(", ".join(sorted(list(st.session_state.scoreboard_used_cards))))
else: st.sidebar.write("*None yet*")

potential_cards_for_manual_removal = [c for c in CARD_LIST if c not in st.session_state.scoreboard_used_cards]
valid_defaults_for_manual_removal = [
    card for card in st.session_state.manually_removed_cards 
    if card in potential_cards_for_manual_removal
]
selected_manual_removals = st.sidebar.multiselect(
    "Manually Remove Cards from Your Deck:", 
    options=sorted(potential_cards_for_manual_removal), 
    default=valid_defaults_for_manual_removal, 
    help="Select cards to remove from your draw pool."
)
if set(selected_manual_removals) != st.session_state.manually_removed_cards:
    st.session_state.manually_removed_cards = set(selected_manual_removals)
    st.rerun() 

AVAILABLE_DRAW_POOL = [c for c in CARD_LIST if c not in st.session_state.scoreboard_used_cards and c not in st.session_state.manually_removed_cards]
st.sidebar.write("**Your Available Draw Pool Size:** " + str(len(AVAILABLE_DRAW_POOL)))
with st.sidebar.expander("View Your Available Draw Pool"): st.write(", ".join(sorted(AVAILABLE_DRAW_POOL)) if AVAILABLE_DRAW_POOL else "*Empty*")
st.sidebar.divider()

# ─────────────────────────────────────────────────────────────────────────────
# Active Missions & Discard Recommendation
# ─────────────────────────────────────────────────────────────────────────────
st.header(f"🎯 Your Active Missions & EV for Round {cur_round+1}")

if cur_round != st.session_state.last_known_cur_round_for_overrides or \
   set(st.session_state.active_current) != set(st.session_state.last_known_active_cards_for_overrides):
    st.session_state.active_mission_overrides = {}
    st.session_state.last_known_cur_round_for_overrides = cur_round
    st.session_state.last_known_active_cards_for_overrides = list(st.session_state.active_current)
    st.session_state.current_active_hand_ev = 0.0 

active_opts_for_selection = [c for c in AVAILABLE_DRAW_POOL if c not in st.session_state.active_current] 
active_opts_for_selection = sorted(list(set(active_opts_for_selection + st.session_state.active_current)))

active_current_selection = st.multiselect(f"Select up to 2 active missions for Round {cur_round+1}", options=active_opts_for_selection, default=st.session_state.active_current, key="active_current_multiselect")
if set(active_current_selection) != set(st.session_state.active_current): 
    st.session_state.active_current = active_current_selection
    st.session_state.active_mission_overrides = {} 
    st.session_state.last_known_active_cards_for_overrides = list(st.session_state.active_current) 
    st.rerun() 

if len(st.session_state.active_current) > 2: st.error("Max 2 active missions. Please deselect some.")

ev_current_hand_for_active_section = 0.0 
if cur_round < MAX_ROUNDS and st.session_state.active_current:
    st.subheader(f"⚡ Adjust Probabilities & See EV for Your Hand in Round {cur_round+1}")
    current_hand_for_ev_calc = st.session_state.active_current 
    
    for card_name_active in current_hand_for_ev_calc: 
        if card_name_active in st.session_state.PROB_EVENTS:
            st.markdown(f"**{card_name_active}**")
            card_events_data = st.session_state.PROB_EVENTS[card_name_active]
            for i_event_override, (pts, prs_list) in enumerate(card_events_data): 
                prob_for_cur_round_default = prs_list[cur_round] 
                override_key = f"override_{card_name_active}_E{i_event_override+1}_R{cur_round+1}"
                
                current_display_prob = st.session_state.active_mission_overrides.get(override_key, prob_for_cur_round_default)
                default_cat_str = find_closest_category(current_display_prob, CATEGORIES, PCT_MAP)
                
                choice_cat = st.selectbox(f"Event {i_event_override+1} ({pts} VP) - Chance for R{cur_round+1}", CATEGORIES,
                                       index=CATEGORIES.index(default_cat_str),
                                       key=override_key + "_sb") 
                
                chosen_pct_value = PCT_MAP.get(choice_cat, 10)
                if override_key not in st.session_state.active_mission_overrides or \
                   st.session_state.active_mission_overrides[override_key] != chosen_pct_value:
                    st.session_state.active_mission_overrides[override_key] = chosen_pct_value
    
    ev_current_hand_for_active_section = calculate_hand_ev_for_round(current_hand_for_ev_calc, cur_round, st.session_state.PROB_EVENTS, st.session_state.active_mission_overrides)
    st.session_state.current_active_hand_ev = ev_current_hand_for_active_section 

    if len(current_hand_for_ev_calc) > 0 :
        best_discard_option = {"card_to_discard": None, "avg_ev_if_redrawn": ev_current_hand_for_active_section, "improvement": 0}
        deck_for_redraw = [c for c in AVAILABLE_DRAW_POOL if c not in current_hand_for_ev_calc] 

        if not deck_for_redraw: st.write("*No cards available in your deck to redraw.*")
        else:
            for card_in_hand_to_discard in current_hand_for_ev_calc:
                temp_hand_after_discard = [c for c in current_hand_for_ev_calc if c != card_in_hand_to_discard]
                sum_ev_of_potential_new_hands = 0
                for replacement_card_from_deck in deck_for_redraw:
                    hypothetical_hand = temp_hand_after_discard + [replacement_card_from_deck]
                    temp_overrides_for_kept_cards = {}
                    for kept_card in temp_hand_after_discard:
                        if kept_card in st.session_state.PROB_EVENTS: 
                            for event_j, (_, _) in enumerate(st.session_state.PROB_EVENTS[kept_card]):
                                kept_override_key = f"override_{kept_card}_E{event_j+1}_R{cur_round+1}"
                                if kept_override_key in st.session_state.active_mission_overrides:
                                    temp_overrides_for_kept_cards[kept_override_key] = st.session_state.active_mission_overrides[kept_override_key]
                    sum_ev_of_potential_new_hands += calculate_hand_ev_for_round(hypothetical_hand, cur_round, st.session_state.PROB_EVENTS, temp_overrides_for_kept_cards)
                
                avg_ev_this_discard_path = sum_ev_of_potential_new_hands / len(deck_for_redraw)
                improvement = avg_ev_this_discard_path - ev_current_hand_for_active_section
                st.write(f"- If '{card_in_hand_to_discard}' is discarded, average EV with redraw: {avg_ev_this_discard_path:.2f} VP (Improvement: {improvement:.2f} VP)")
                if improvement > best_discard_option["improvement"]: best_discard_option = {"card_to_discard": card_in_hand_to_discard, "avg_ev_if_redrawn": avg_ev_this_discard_path, "improvement": improvement}
            
            if best_discard_option["card_to_discard"] and best_discard_option["improvement"] > 0.05: st.success(f"**Recommendation: Discard '{best_discard_option['card_to_discard']}'.** Expected EV gain: {best_discard_option['improvement']:.2f} VP.")
            else: st.info("**Recommendation: Keep current hand.** No discard option offers significant EV improvement.")
else:
    st.write("Select your active missions to see EV and discard recommendations for the current round.")
    st.session_state.current_active_hand_ev = 0.0 

# ─────────────────────────────────────────────────────────────────────────────
# VP Summary & Projections
# ─────────────────────────────────────────────────────────────────────────────
st.header("📊 VP Summary & Projections")

# User Scores
st.subheader("Your Score")
user_summary_cols = st.columns(3)
user_current_grand_total_calc = sec_total + pri_total 
user_start_vp_label = ""
if st.session_state.get('include_start_vp', True):
    user_current_grand_total_calc += START_VP
    user_start_vp_label = " (incl. Start VP)"

user_summary_cols[0].metric("Your Scored Secondary VP", f"{int(sec_total)} VP")
user_summary_cols[1].metric("Your Entered Primary VP", f"{int(pri_total)} VP") 
user_summary_cols[2].metric(f"Your Current Grand Total{user_start_vp_label}", f"{int(user_current_grand_total_calc)} VP")

active_hand_ev_display_val = st.session_state.get('current_active_hand_ev', 0.0)
if st.session_state.active_current and cur_round < MAX_ROUNDS: 
    st.metric(f"EV of Your Active Hand (R{cur_round+1})", f"{active_hand_ev_display_val:.2f} VP",
              help="Expected VPs from your currently selected active missions for this round, considering any probability adjustments you've made above.")

user_sim_future_vp_val = st.session_state.get('total_sim_future_vp', 0.0) 
sim_has_run_indicator = 'run_sim_button_main' in st.session_state and st.session_state.run_sim_button_main

if user_sim_future_vp_val > 0 or sim_has_run_indicator : 
    st.metric("Your Simulated Future Secondary VP", f"{user_sim_future_vp_val:.2f} VP",
              help="Average VPs expected from your secondary missions in future rounds, based on the last simulation run. This does NOT include the EV of your current active hand. Capped at 40 total secondary VPs.")
    
    user_projected_total_vp_calc = sec_total + pri_total + user_sim_future_vp_val # sec_total and pri_total are already capped
    if st.session_state.get('include_start_vp', True): user_projected_total_vp_calc += START_VP
    
    st.metric(f"Your Projected Game End Total VP{user_start_vp_label}", f"{user_projected_total_vp_calc:.2f} VP",
              help="Sum of your current VPs and your simulated future secondary VPs. Primary capped at 50, Secondary at 40.")
else:
    st.info("Run a 'Future Rounds Simulation' (in sidebar) to see your projected VPs.")

st.divider()

# Opponent Scores - SIMPLIFIED DISPLAY
st.subheader("Opponent's Score")
opp_current_grand_total_calc = opp_sec_total + opp_pri_total
opp_start_vp_label = ""
if st.session_state.get('include_start_vp', True):
    opp_current_grand_total_calc += START_VP
    opp_start_vp_label = " (incl. Start VP)"

st.metric(f"Opponent's Current Grand Total{opp_start_vp_label}", f"{int(opp_current_grand_total_calc)} VP",
          help="Sum of opponent's entered secondary and primary VPs, plus starting VP if selected. Primary capped at 50, Secondary at 40.")

opp_sim_future_vp_val = st.session_state.get('opponent_total_sim_future_vp', 0.0)
opp_projected_total_vp_calc = opp_sec_total + opp_pri_total + opp_sim_future_vp_val # opp_sec_total and opp_pri_total are already capped
if st.session_state.get('include_start_vp', True): opp_projected_total_vp_calc += START_VP

st.metric(f"Opponent's Projected Game End Total VP{opp_start_vp_label}", f"{opp_projected_total_vp_calc:.2f} VP",
            help="Sum of opponent's current VPs and their projected future secondary VPs (based on optimal play). Primary capped at 50, Secondary at 40.")


# ─────────────────────────────────────────────────────────────────────────────
# Future simulation (User's Simulation)
# ─────────────────────────────────────────────────────────────────────────────
def simulate_future(initial_deck_for_sim, current_app_round_sim, allow_discard_in_sim, num_trials, prob_events_data_sim, current_user_sec_score): 
    """Simulates future rounds for the user: draw 2, optional discard/redraw (optimal for round), score. Respects 40 VP Secondary Cap."""
    round_total_vps_sim = {r_sim_loop: 0.0 for r_sim_loop in range(current_app_round_sim + 1, MAX_ROUNDS)} 
    
    total_future_vp_across_trials = 0

    for _ in range(num_trials):
        trial_deck_sim = list(initial_deck_for_sim); random.shuffle(trial_deck_sim) 
        trial_future_secondary_vp = 0 # VP scored in this specific trial for future rounds

        for r_idx_sim, r_val_sim in enumerate(range(current_app_round_sim + 1, MAX_ROUNDS), start=current_app_round_sim + 1): 
            if current_user_sec_score + trial_future_secondary_vp >= MAX_SECONDARY_SCORE:
                break # Stop this trial's future rounds if cap already met/exceeded by prior rounds in this trial

            current_sim_hand_trial = []; 
            if len(trial_deck_sim) >= 2: current_sim_hand_trial = [trial_deck_sim.pop(0), trial_deck_sim.pop(0)]
            elif len(trial_deck_sim) == 1: current_sim_hand_trial = [trial_deck_sim.pop(0)]
            if not current_sim_hand_trial: continue
            
            final_hand_for_scoring_this_round_sim = list(current_sim_hand_trial) 
            if allow_discard_in_sim and current_sim_hand_trial and trial_deck_sim: 
                ev_current_sim_hand_this_round_sim = calculate_hand_ev_for_round(current_sim_hand_trial, r_val_sim, prob_events_data_sim, None) 
                best_ev_after_discard_sim, card_to_discard_for_sim_trial = ev_current_sim_hand_this_round_sim, None 
                
                for card_to_try_discarding_sim in current_sim_hand_trial: 
                    temp_hand_after_discard_sim = [c for c in current_sim_hand_trial if c != card_to_try_discarding_sim] 
                    if trial_deck_sim: 
                        potential_redraw_card_sim = trial_deck_sim[0]  
                        hypothetical_hand_for_ev_sim = temp_hand_after_discard_sim + [potential_redraw_card_sim] 
                        ev_hypothetical_sim = calculate_hand_ev_for_round(hypothetical_hand_for_ev_sim, r_val_sim, prob_events_data_sim, None) 
                        if ev_hypothetical_sim > best_ev_after_discard_sim: best_ev_after_discard_sim, card_to_discard_for_sim_trial = ev_hypothetical_sim, card_to_try_discarding_sim
                
                if card_to_discard_for_sim_trial and trial_deck_sim: 
                    final_hand_for_scoring_this_round_sim = [c for c in current_sim_hand_trial if c != card_to_discard_for_sim_trial]
                    final_hand_for_scoring_this_round_sim.append(trial_deck_sim.pop(0))
            
            round_score_for_trial_sim_this_round = 0 
            for card_name_in_scoring_hand_sim in final_hand_for_scoring_this_round_sim: 
                if card_name_in_scoring_hand_sim in prob_events_data_sim:
                    for pts, prs_list in prob_events_data_sim[card_name_in_scoring_hand_sim]:
                        if 0 <= r_val_sim < len(prs_list) and random.random() < prs_list[r_val_sim] / 100.0: 
                            # Check cap before adding
                            if current_user_sec_score + trial_future_secondary_vp + pts <= MAX_SECONDARY_SCORE:
                                round_score_for_trial_sim_this_round += pts
                            else:
                                round_score_for_trial_sim_this_round += max(0, MAX_SECONDARY_SCORE - (current_user_sec_score + trial_future_secondary_vp))
                                trial_future_secondary_vp += round_score_for_trial_sim_this_round
                                break # Stop adding points from this card if cap hit
                    if current_user_sec_score + trial_future_secondary_vp >= MAX_SECONDARY_SCORE:
                        break # Stop adding points from other cards if cap hit
            
            trial_future_secondary_vp += round_score_for_trial_sim_this_round
            # Accumulate per-round average for display, but total is capped
            round_total_vps_sim[r_val_sim] += round_score_for_trial_sim_this_round # This is for per-round display, not the final capped total

        total_future_vp_across_trials += min(trial_future_secondary_vp, MAX_SECONDARY_SCORE - current_user_sec_score)


    avg_total_future_vp = total_future_vp_across_trials / num_trials
    # For per-round display (not strictly capped for this display, but sum will be)
    avg_vps_per_round_display = {r_avg: total_vp / num_trials for r_avg, total_vp in round_total_vps_sim.items()} 
    
    return avg_total_future_vp, avg_vps_per_round_display

st.sidebar.header("Your Future Rounds Simulation") 
if cur_round < MAX_ROUNDS - 1:
    n_trials_sim_widget = st.sidebar.number_input("Number of Trials ", min_value=100, max_value=100000, value=5000, step=100, key="n_trials_sim_main") 
    allow_disc_sim_widget = st.sidebar.checkbox("Allow Discard/Redraw in Sim Rounds ", True, key="allow_disc_sim_main") 
    
    run_simulation_button = st.sidebar.button("Run Your Future Rounds Simulation ▶️ ", key="run_sim_button_main")
    if run_simulation_button: 
        if not AVAILABLE_DRAW_POOL or len(AVAILABLE_DRAW_POOL) < 1 : 
             st.sidebar.warning("Not enough cards in Your Available Draw Pool for a typical simulation.")
             st.session_state.total_sim_future_vp = 0.0 
        else:
            with st.spinner(f"Simulating {n_trials_sim_widget} trials for your future rounds..."):
                # Pass current user secondary score to the simulation for capping
                avg_total_future_vp_result, avg_vps_per_round_display_result = simulate_future(
                    list(AVAILABLE_DRAW_POOL), 
                    cur_round, 
                    allow_disc_sim_widget, 
                    n_trials_sim_widget, 
                    st.session_state.PROB_EVENTS,
                    sec_total # User's current secondary score
                )
            
            st.session_state.total_sim_future_vp = avg_total_future_vp_result

            if avg_vps_per_round_display_result:
                df_res_list = [{"Sim. Round": r_num_res + 1, "Avg Future VP": round(vp_val_res, 2)} 
                               for r_num_res, vp_val_res in avg_vps_per_round_display_result.items() 
                               if vp_val_res > 0 or r_num_res >= cur_round +1] 
                
                if df_res_list: 
                    st.sidebar.subheader("Your Simulation Results (Avg VP Per Round - Display Only)")
                    st.sidebar.table(pd.DataFrame(df_res_list))
                else: 
                    st.sidebar.info("Your simulation ran but produced no VPs for future rounds (display).")
            else: 
                st.sidebar.info("Your simulation did not return per-round results for display.")
        st.rerun() 
else:
    st.sidebar.info("Your simulation available only before the last round.")

# ─────────────────────────────────────────────────────────────────────────────
# Edit Opponent's Probabilities (NEW SECTION - Minimized by default)
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
with st.expander("Edit Opponent's Mission Probabilities (Baseline)", expanded=False):
    updated_opponent_probs_edit = copy.deepcopy(st.session_state.OPPONENT_PROB_EVENTS)
    
    # Use the same cur_round_for_edit_display as the user's section for consistency
    temp_calculated_cur_round_for_opp_edit = 0
    for i_opp_edit_cur_round, round_data_opp_edit_cur_round in enumerate(st.session_state.scoreboard_data_list):
        # Based on user's progress to determine "past" rounds for opponent's probability editing
        if round_data_opp_edit_cur_round['s1'] > 0 or round_data_opp_edit_cur_round['s2'] > 0 or round_data_opp_edit_cur_round['used']:
            if i_opp_edit_cur_round < MAX_ROUNDS - 1: temp_calculated_cur_round_for_opp_edit = i_opp_edit_cur_round + 1
            else: temp_calculated_cur_round_for_opp_edit = MAX_ROUNDS - 1
        else: break
    cur_round_for_opp_edit_display = temp_calculated_cur_round_for_opp_edit

    for card_opp, evs_opp in st.session_state.OPPONENT_PROB_EVENTS.items():
        st.markdown(f"**{card_opp} (Opponent)**"); new_evs_for_card_opp = []
        for event_idx_opp, (pts_opp, prs_list_opp) in enumerate(evs_opp, start=1):
            num_future_rounds_opp = MAX_ROUNDS - cur_round_for_opp_edit_display
            num_cols_to_create_opp = 1 + num_future_rounds_opp if num_future_rounds_opp > 0 else 1
            
            cols_opp = st.columns(num_cols_to_create_opp)
            cols_opp[0].markdown(f"*VP: {pts_opp}*")
            new_prs_for_event_opp = list(prs_list_opp) 

            if num_future_rounds_opp > 0:
                col_idx_offset_opp = 1 
                for r_game_round_0_indexed_opp in range(cur_round_for_opp_edit_display, MAX_ROUNDS):
                    r_game_round_1_indexed_opp = r_game_round_0_indexed_opp + 1
                    
                    prob_val_opp = prs_list_opp[r_game_round_0_indexed_opp]
                    key_opp = f"edit_opp_{card_opp}_E{event_idx_opp}_r{r_game_round_1_indexed_opp}"
                    default_cat_str_opp = find_closest_category(prob_val_opp, CATEGORIES, PCT_MAP)
                    
                    choice_opp = cols_opp[col_idx_offset_opp].selectbox(
                        f"R{r_game_round_1_indexed_opp}", 
                        CATEGORIES, 
                        index=CATEGORIES.index(default_cat_str_opp), 
                        key=key_opp, 
                        label_visibility="visible" 
                    )
                    new_prs_for_event_opp[r_game_round_0_indexed_opp] = PCT_MAP.get(choice_opp, 10) 
                    col_idx_offset_opp += 1
            
            new_evs_for_card_opp.append((pts_opp, new_prs_for_event_opp))
        updated_opponent_probs_edit[card_opp] = new_evs_for_card_opp
        
    if st.button("Apply Opponent's Baseline Probability Changes"):
        st.session_state.OPPONENT_PROB_EVENTS = updated_opponent_probs_edit
        st.success("Opponent's Baseline Probabilities updated!")
        # Recalculate opponent's future VP based on new probabilities
        st.session_state.opponent_total_sim_future_vp = calculate_opponent_future_secondary_vp(
            cur_round, st.session_state.opponent_scoreboard_used_cards, st.session_state.OPPONENT_PROB_EVENTS, opp_sec_total
        )
        st.rerun()

