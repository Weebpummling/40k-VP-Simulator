{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red111\green14\blue195;\red236\green241\blue247;\red0\green0\blue0;
\red77\green80\blue85;\red164\green69\blue11;\red24\green112\blue43;}
{\*\expandedcolortbl;;\cssrgb\c51765\c18824\c80784;\cssrgb\c94118\c95686\c97647;\cssrgb\c0\c0\c0;
\cssrgb\c37255\c38824\c40784;\cssrgb\c70980\c34902\c3137;\cssrgb\c9412\c50196\c21961;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\deftab720
\pard\pardeftab720\partightenfactor0

\f0\fs28 \cf2 \cb3 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 import\cf0 \strokec4  streamlit \cf2 \strokec2 as\cf0 \strokec4  st\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  pandas \cf2 \strokec2 as\cf0 \strokec4  pd\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  numpy \cf2 \strokec2 as\cf0 \strokec4  np\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  random\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  io\cb1 \
\cf2 \cb3 \strokec2 import\cf0 \strokec4  copy\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Constants & Configuration\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 MAX_ROUNDS = \cf6 \strokec6 5\cf0 \cb1 \strokec4 \
\cb3 START_VP   = \cf6 \strokec6 10\cf0 \cb1 \strokec4 \
\cb3 MAX_PRIMARY_SCORE = \cf6 \strokec6 50\cf0 \cb1 \strokec4 \
\cb3 MAX_SECONDARY_SCORE = \cf6 \strokec6 40\cf0 \cb1 \strokec4 \
\
\
\cb3 CATEGORIES = [\cf7 \strokec7 "100%"\cf0 \strokec4 ,\cf7 \strokec7 "80%"\cf0 \strokec4 ,\cf7 \strokec7 "50%"\cf0 \strokec4 ,\cf7 \strokec7 "30%"\cf0 \strokec4 ,\cf7 \strokec7 "<10%"\cf0 \strokec4 ]\cb1 \
\cb3 PCT_MAP    = \{\cf7 \strokec7 "100%"\cf0 \strokec4 :\cf6 \strokec6 100\cf0 \strokec4 ,\cf7 \strokec7 "80%"\cf0 \strokec4 :\cf6 \strokec6 80\cf0 \strokec4 ,\cf7 \strokec7 "50%"\cf0 \strokec4 :\cf6 \strokec6 50\cf0 \strokec4 ,\cf7 \strokec7 "30%"\cf0 \strokec4 :\cf6 \strokec6 30\cf0 \strokec4 ,\cf7 \strokec7 "<10%"\cf0 \strokec4 :\cf6 \strokec6 10\cf0 \strokec4 \}\cb1 \
\
\cb3 DEFAULT_PROBS = \{\cb1 \
\cb3     \cf7 \strokec7 "Assassination"\cf0 \strokec4 :        [(\cf6 \strokec6 5\cf0 \strokec4 , [\cf6 \strokec6 20\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 70\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Containment"\cf0 \strokec4 :          [(\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 ]), (\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Behind Enemy Lines"\cf0 \strokec4 :   [(\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 10\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ]), (\cf6 \strokec6 1\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Marked for Death"\cf0 \strokec4 :     [(\cf6 \strokec6 5\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 20\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Bring it Down"\cf0 \strokec4 :        [(\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ]), (\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "No Prisoners"\cf0 \strokec4 :         [(\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 20\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 ]), (\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ]), (\cf6 \strokec6 1\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Defend Stronghold"\cf0 \strokec4 :    [(\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Storm Hostile Objective"\cf0 \strokec4 : [(\cf6 \strokec6 4\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Sabotage"\cf0 \strokec4 :             [(\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 ]), (\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 10\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Cull the Horde"\cf0 \strokec4 :       [(\cf6 \strokec6 5\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 10\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Overwhelming Force"\cf0 \strokec4 :   [(\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 10\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ]), (\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Extend Battlelines"\cf0 \strokec4 :   [(\cf6 \strokec6 5\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Recover Assets"\cf0 \strokec4 :       [(\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 ]), (\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 ])], \cb1 \
\cb3     \cf7 \strokec7 "Engage on All Fronts"\cf0 \strokec4 : [(\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ]), (\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 30\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 ])], \cb1 \
\cb3     \cf7 \strokec7 "Area Denial"\cf0 \strokec4 :          [(\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ]), (\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Secure No Man's Land"\cf0 \strokec4 : [(\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 ]), (\cf6 \strokec6 3\cf0 \strokec4 , [\cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Cleanse"\cf0 \strokec4 :              [(\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 100\cf0 \strokec4 ]), (\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])],\cb1 \
\cb3     \cf7 \strokec7 "Establish Locus"\cf0 \strokec4 :      [(\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 100\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ]), (\cf6 \strokec6 2\cf0 \strokec4 , [\cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 40\cf0 \strokec4 , \cf6 \strokec6 50\cf0 \strokec4 , \cf6 \strokec6 80\cf0 \strokec4 ])]\cb1 \
\cb3 \}\cb1 \
\cb3 CARD_LIST = \cf2 \strokec2 sorted\cf0 \strokec4 (\cf2 \strokec2 list\cf0 \strokec4 (DEFAULT_PROBS.keys()))\cb1 \
\cb3 MAX_EVENTS = \cf2 \strokec2 max\cf0 \strokec4 (\cf2 \strokec2 len\cf0 \strokec4 (evs) \cf2 \strokec2 for\cf0 \strokec4  evs \cf2 \strokec2 in\cf0 \strokec4  DEFAULT_PROBS.values()) \cf2 \strokec2 if\cf0 \strokec4  DEFAULT_PROBS \cf2 \strokec2 else\cf0 \strokec4  \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\
\cb3 COL_EVENT_PTS_TPL = \cf7 \strokec7 "E\{\}_pts"\cf0 \cb1 \strokec4 \
\cb3 COL_EVENT_ROUND_PROB_TPL = \cf7 \strokec7 "E\{\}_r\{\}"\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Session State Initialization\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'PROB_EVENTS'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.PROB_EVENTS = copy.deepcopy(DEFAULT_PROBS)\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'OPPONENT_PROB_EVENTS'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.OPPONENT_PROB_EVENTS = copy.deepcopy(DEFAULT_PROBS)\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'player_order'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.player_order = \cf7 \strokec7 "Going First"\cf0 \cb1 \strokec4 \
\
\
\cb3 default_round_data = \{\cb1 \
\cb3     \cf7 \strokec7 's1'\cf0 \strokec4 : \cf6 \strokec6 0\cf0 \strokec4 , \cf7 \strokec7 's2'\cf0 \strokec4 : \cf6 \strokec6 0\cf0 \strokec4 , \cf7 \strokec7 'p'\cf0 \strokec4 : \cf6 \strokec6 0\cf0 \strokec4 , \cf7 \strokec7 'used'\cf0 \strokec4 : [],\cb1 \
\cb3     \cf7 \strokec7 'opp_s1'\cf0 \strokec4 : \cf6 \strokec6 0\cf0 \strokec4 , \cf7 \strokec7 'opp_s2'\cf0 \strokec4 : \cf6 \strokec6 0\cf0 \strokec4 , \cf7 \strokec7 'opp_p'\cf0 \strokec4 : \cf6 \strokec6 0\cf0 \strokec4 , \cf7 \strokec7 'opp_used'\cf0 \strokec4 : []\cb1 \
\cb3 \}\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'scoreboard_data_list'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.scoreboard_data_list = [copy.deepcopy(default_round_data) \cf2 \strokec2 for\cf0 \strokec4  \cf2 \strokec2 _\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (MAX_ROUNDS)]\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 else\cf0 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf2 \strokec2 for\cf0 \strokec4  i \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (\cf2 \strokec2 len\cf0 \strokec4 (st.session_state.scoreboard_data_list)):\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  key, default_value \cf2 \strokec2 in\cf0 \strokec4  default_round_data.items():\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 isinstance\cf0 \strokec4 (default_value, \cf2 \strokec2 list\cf0 \strokec4 ):\cb1 \
\cb3                  st.session_state.scoreboard_data_list[i].setdefault(key, \cf2 \strokec2 list\cf0 \strokec4 (default_value))\cb1 \
\cb3             \cf2 \strokec2 else\cf0 \strokec4 :\cb1 \
\cb3                  st.session_state.scoreboard_data_list[i].setdefault(key, default_value)\cb1 \
\cb3     \cb1 \
\cb3     \cf2 \strokec2 while\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (st.session_state.scoreboard_data_list) < MAX_ROUNDS:\cb1 \
\cb3         st.session_state.scoreboard_data_list.append(copy.deepcopy(default_round_data))\cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (st.session_state.scoreboard_data_list) > MAX_ROUNDS:\cb1 \
\cb3         st.session_state.scoreboard_data_list = st.session_state.scoreboard_data_list[:MAX_ROUNDS]\cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'active_current'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.active_current = []\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'manually_removed_cards'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.manually_removed_cards = \cf2 \strokec2 set\cf0 \strokec4 () \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'opponent_manually_removed_cards'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.opponent_manually_removed_cards = \cf2 \strokec2 set\cf0 \strokec4 ()\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'scoreboard_used_cards'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.scoreboard_used_cards = \cf2 \strokec2 set\cf0 \strokec4 () \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'opponent_scoreboard_used_cards'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.opponent_scoreboard_used_cards = \cf2 \strokec2 set\cf0 \strokec4 () \cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'active_mission_overrides'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.active_mission_overrides = \{\} \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'last_known_cur_round_for_overrides'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.last_known_cur_round_for_overrides = \cf6 \strokec6 -1\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'last_known_active_cards_for_overrides'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.last_known_active_cards_for_overrides = []\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'include_start_vp'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.include_start_vp = \cf2 \strokec2 True\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'current_active_hand_ev'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.current_active_hand_ev = \cf6 \strokec6 0.0\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'total_sim_future_vp'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.total_sim_future_vp = \cf6 \strokec6 0.0\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 'opponent_total_sim_future_vp'\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.opponent_total_sim_future_vp = \cf6 \strokec6 0.0\cf0 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Helper Functions\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  find_closest_category(prob_val, categories_list, pct_map):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf7 \strokec7 """Finds the string category in categories_list closest to prob_val."""\cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf7 \strokec7 f"\cf0 \strokec4 \{prob_val\}\cf7 \strokec7 %"\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  categories_list: \cf2 \strokec2 return\cf0 \strokec4  \cf7 \strokec7 f"\cf0 \strokec4 \{prob_val\}\cf7 \strokec7 %"\cf0 \cb1 \strokec4 \
\cb3     min_diff, closest_cat_str = \cf2 \strokec2 float\cf0 \strokec4 (\cf7 \strokec7 'inf'\cf0 \strokec4 ), categories_list[\cf6 \strokec6 -1\cf0 \strokec4 ]\cb1 \
\cb3     \cf2 \strokec2 for\cf0 \strokec4  cat_str \cf2 \strokec2 in\cf0 \strokec4  categories_list:\cb1 \
\cb3         cat_val = pct_map.get(cat_str, \cf6 \strokec6 0\cf0 \strokec4 )\cb1 \
\cb3         diff = \cf2 \strokec2 abs\cf0 \strokec4 (prob_val - cat_val)\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  diff < min_diff: min_diff, closest_cat_str = diff, cat_str\cb1 \
\cb3         \cf2 \strokec2 elif\cf0 \strokec4  diff == min_diff \cf2 \strokec2 and\cf0 \strokec4  pct_map.get(cat_str,\cf6 \strokec6 0\cf0 \strokec4 ) > pct_map.get(closest_cat_str,\cf6 \strokec6 0\cf0 \strokec4 ): closest_cat_str = cat_str\cb1 \
\cb3     \cf2 \strokec2 return\cf0 \strokec4  closest_cat_str\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  calculate_card_ev_for_round(card_name, round_idx, prob_events_data):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf7 \strokec7 """Calculates Expected Value for a single card for a specific round using baseline probabilities."""\cf0 \cb1 \strokec4 \
\cb3     ev = \cf6 \strokec6 0\cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  card_name \cf2 \strokec2 in\cf0 \strokec4  prob_events_data:\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  pts, prs_list \cf2 \strokec2 in\cf0 \strokec4  prob_events_data[card_name]:\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 0\cf0 \strokec4  <= round_idx < \cf2 \strokec2 len\cf0 \strokec4 (prs_list):\cb1 \
\cb3                 ev += pts * (prs_list[round_idx] / \cf6 \strokec6 100.0\cf0 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 return\cf0 \strokec4  ev\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  calculate_hand_ev_for_round(hand, round_idx, prob_events_data, overrides=\cf2 \strokec2 None\cf0 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf7 \strokec7 """Calculates Expected Value for a hand for a specific round, considering overrides."""\cf0 \cb1 \strokec4 \
\cb3     ev = \cf6 \strokec6 0\cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  hand \cf2 \strokec2 or\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  prob_events_data: \cf2 \strokec2 return\cf0 \strokec4  \cf6 \strokec6 0\cf0 \cb1 \strokec4 \
\cb3     \cf2 \strokec2 for\cf0 \strokec4  card_name \cf2 \strokec2 in\cf0 \strokec4  hand:\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  card_name \cf2 \strokec2 in\cf0 \strokec4  prob_events_data:\cb1 \
\cb3             \cf2 \strokec2 for\cf0 \strokec4  event_i, (pts, prs_list) \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (prob_events_data[card_name]):\cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 0\cf0 \strokec4  <= round_idx < \cf2 \strokec2 len\cf0 \strokec4 (prs_list):\cb1 \
\cb3                     default_prob_pct = prs_list[round_idx]\cb1 \
\cb3                     override_key = \cf7 \strokec7 f"override_\cf0 \strokec4 \{card_name\}\cf7 \strokec7 _E\cf0 \strokec4 \{event_i+1\}\cf7 \strokec7 _R\cf0 \strokec4 \{round_idx+1\}\cf7 \strokec7 "\cf0 \strokec4  \cb1 \
\cb3                     \cb1 \
\cb3                     current_prob_pct = default_prob_pct\cb1 \
\cb3                     \cf2 \strokec2 if\cf0 \strokec4  overrides \cf2 \strokec2 and\cf0 \strokec4  override_key \cf2 \strokec2 in\cf0 \strokec4  overrides:\cb1 \
\cb3                         current_prob_pct = overrides[override_key] \cb1 \
\cb3                     \cb1 \
\cb3                     ev += pts * (current_prob_pct / \cf6 \strokec6 100.0\cf0 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 return\cf0 \strokec4  ev\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  calculate_opponent_future_secondary_vp(current_round_0_indexed, opponent_used_cards_set, opponent_manually_removed_set, opponent_prob_events_data, current_opponent_sec_score):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf7 \strokec7 """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf7 \cb3 \strokec7     Calculates a projected future secondary VP for the opponent.\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     Assumes opponent picks the top 2 EV cards available to them each future round.\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     Respects the MAX_SECONDARY_SCORE (40 VP) cap.\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     Considers opponent's manually removed cards.\cf0 \cb1 \strokec4 \
\cf7 \cb3 \strokec7     """\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     projected_vp_for_future_rounds = \cf6 \strokec6 0.0\cf0 \strokec4  \cb1 \
\cb3     combined_opponent_unavailable_cards = \cf2 \strokec2 set\cf0 \strokec4 (opponent_used_cards_set).union(opponent_manually_removed_set)\cb1 \
\cb3     temp_opponent_unavailable_cards_for_sim = \cf2 \strokec2 set\cf0 \strokec4 (combined_opponent_unavailable_cards) \cb1 \
\
\
\cb3     \cf2 \strokec2 for\cf0 \strokec4  r_idx \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (current_round_0_indexed + \cf6 \strokec6 1\cf0 \strokec4 , MAX_ROUNDS):\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  current_opponent_sec_score + projected_vp_for_future_rounds >= MAX_SECONDARY_SCORE:\cb1 \
\cb3             \cf2 \strokec2 break\cf0 \strokec4  \cb1 \
\
\cb3         available_cards_for_opponent_this_round = [\cb1 \
\cb3             c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  CARD_LIST \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  temp_opponent_unavailable_cards_for_sim\cb1 \
\cb3         ]\cb1 \
\cb3         \cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  available_cards_for_opponent_this_round:\cb1 \
\cb3             \cf2 \strokec2 continue\cf0 \cb1 \strokec4 \
\
\cb3         card_evs_this_round = []\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  card \cf2 \strokec2 in\cf0 \strokec4  available_cards_for_opponent_this_round:\cb1 \
\cb3             ev = calculate_card_ev_for_round(card, r_idx, opponent_prob_events_data) \cb1 \
\cb3             card_evs_this_round.append(\{\cf7 \strokec7 "name"\cf0 \strokec4 : card, \cf7 \strokec7 "ev"\cf0 \strokec4 : ev\})\cb1 \
\cb3         \cb1 \
\cb3         card_evs_this_round.sort(key=\cf2 \strokec2 lambda\cf0 \strokec4  x: x[\cf7 \strokec7 "ev"\cf0 \strokec4 ], reverse=\cf2 \strokec2 True\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         cards_chosen_this_round_opponent = []\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  i \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (\cf2 \strokec2 min\cf0 \strokec4 (\cf6 \strokec6 2\cf0 \strokec4 , \cf2 \strokec2 len\cf0 \strokec4 (card_evs_this_round))):\cb1 \
\cb3             chosen_card = card_evs_this_round[i]\cb1 \
\cb3             \cb1 \
\cb3             potential_score_from_card = chosen_card[\cf7 \strokec7 "ev"\cf0 \strokec4 ]\cb1 \
\cb3             remaining_cap_space = MAX_SECONDARY_SCORE - (current_opponent_sec_score + projected_vp_for_future_rounds)\cb1 \
\cb3             \cb1 \
\cb3             score_to_add_this_card = \cf2 \strokec2 min\cf0 \strokec4 (potential_score_from_card, remaining_cap_space)\cb1 \
\cb3             \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  score_to_add_this_card <= \cf6 \strokec6 0\cf0 \strokec4 : \cb1 \
\cb3                 \cf2 \strokec2 break\cf0 \strokec4  \cb1 \
\
\cb3             projected_vp_for_future_rounds += score_to_add_this_card \cb1 \
\cb3             cards_chosen_this_round_opponent.append(chosen_card[\cf7 \strokec7 "name"\cf0 \strokec4 ])\cb1 \
\cb3             \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  current_opponent_sec_score + projected_vp_for_future_rounds >= MAX_SECONDARY_SCORE:\cb1 \
\cb3                 \cf2 \strokec2 break\cf0 \strokec4  \cb1 \
\cb3             \cb1 \
\cb3         temp_opponent_unavailable_cards_for_sim.update(cards_chosen_this_round_opponent) \cb1 \
\
\cb3     \cf2 \strokec2 return\cf0 \strokec4  projected_vp_for_future_rounds \cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Calculate Current Round Globally (MOVED UP)\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 calculated_cur_round_val = \cf6 \strokec6 0\cf0 \strokec4  \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 for\cf0 \strokec4  i_sb_round_global_cur \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (MAX_ROUNDS): \cf5 \strokec5 # Renamed i_sb_round for clarity\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     round_data_global_cur = st.session_state.scoreboard_data_list[i_sb_round_global_cur] \cf5 \strokec5 # Renamed round_data for clarity\cf0 \cb1 \strokec4 \
\cb3     user_played_this_round_global_cur = round_data_global_cur[\cf7 \strokec7 's1'\cf0 \strokec4 ] > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 or\cf0 \strokec4  round_data_global_cur[\cf7 \strokec7 's2'\cf0 \strokec4 ] > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 or\cf0 \strokec4  round_data_global_cur[\cf7 \strokec7 'used'\cf0 \strokec4 ]\cb1 \
\cb3     opponent_played_this_round_global_cur = round_data_global_cur[\cf7 \strokec7 'opp_s1'\cf0 \strokec4 ] > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 or\cf0 \strokec4  round_data_global_cur[\cf7 \strokec7 'opp_s2'\cf0 \strokec4 ] > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 or\cf0 \strokec4  round_data_global_cur[\cf7 \strokec7 'opp_used'\cf0 \strokec4 ]\cb1 \
\
\cb3     \cf2 \strokec2 if\cf0 \strokec4  st.session_state.player_order == \cf7 \strokec7 "Going First"\cf0 \strokec4 :\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  user_played_this_round_global_cur \cf2 \strokec2 and\cf0 \strokec4  opponent_played_this_round_global_cur: \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  i_sb_round_global_cur < MAX_ROUNDS - \cf6 \strokec6 1\cf0 \strokec4 :\cb1 \
\cb3                 calculated_cur_round_val = i_sb_round_global_cur + \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 else\cf0 \strokec4 : \cb1 \
\cb3                 calculated_cur_round_val = MAX_ROUNDS \cf6 \strokec6 -1\cf0 \strokec4  \cb1 \
\cb3         \cf2 \strokec2 else\cf0 \strokec4 : \cb1 \
\cb3             calculated_cur_round_val = i_sb_round_global_cur \cb1 \
\cb3             \cf2 \strokec2 break\cf0 \strokec4  \cb1 \
\cb3     \cf2 \strokec2 else\cf0 \strokec4 : \cf5 \strokec5 # Player is Going Second\cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  user_played_this_round_global_cur: \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  i_sb_round_global_cur < MAX_ROUNDS - \cf6 \strokec6 1\cf0 \strokec4 :\cb1 \
\cb3                 calculated_cur_round_val = i_sb_round_global_cur + \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 else\cf0 \strokec4 : \cb1 \
\cb3                 calculated_cur_round_val = MAX_ROUNDS - \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 else\cf0 \strokec4 : \cb1 \
\cb3             calculated_cur_round_val = i_sb_round_global_cur\cb1 \
\cb3             \cf2 \strokec2 break\cf0 \cb1 \strokec4 \
\cb3 cur_round = \cf2 \strokec2 min\cf0 \strokec4 (calculated_cur_round_val, MAX_ROUNDS - \cf6 \strokec6 1\cf0 \strokec4 ) \cf5 \strokec5 # Global cur_round (0-indexed)\cf0 \cb1 \strokec4 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Sidebar Settings\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.sidebar.header(\cf7 \strokec7 "General Settings"\cf0 \strokec4 )\cb1 \
\cb3 player_order_options = [\cf7 \strokec7 "Going First"\cf0 \strokec4 , \cf7 \strokec7 "Going Second"\cf0 \strokec4 ]\cb1 \
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # Get current index for radio button to ensure it reflects session state\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 current_player_order_index = player_order_options.index(st.session_state.player_order) \cf2 \strokec2 if\cf0 \strokec4  st.session_state.player_order \cf2 \strokec2 in\cf0 \strokec4  player_order_options \cf2 \strokec2 else\cf0 \strokec4  \cf6 \strokec6 0\cf0 \cb1 \strokec4 \
\
\cb3 selected_player_order = st.sidebar.radio(\cb1 \
\cb3     \cf7 \strokec7 "Select Your Player Order:"\cf0 \strokec4 ,\cb1 \
\cb3     options=player_order_options,\cb1 \
\cb3     index=current_player_order_index, \cb1 \
\cb3     key=\cf7 \strokec7 "player_order_radio_widget"\cf0 \strokec4  \cf5 \strokec5 # Use a distinct key for the widget itself\cf0 \cb1 \strokec4 \
\cb3 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # Update session state only if the widget's value has changed, to prevent unnecessary reruns if a manual rerun is triggered elsewhere\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  selected_player_order != st.session_state.player_order:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.player_order = selected_player_order\cb1 \
\cb3     st.rerun() \cf5 \strokec5 # Rerun if player order changes as it affects cur_round\cf0 \cb1 \strokec4 \
\
\cb3 st.session_state.include_start_vp = st.sidebar.checkbox(\cb1 \
\cb3     \cf7 \strokec7 "Include Starting VP (10 VP) in Totals"\cf0 \strokec4 , \cb1 \
\cb3     value=st.session_state.include_start_vp,\cb1 \
\cb3     key=\cf7 \strokec7 "include_start_vp_checkbox"\cf0 \cb1 \strokec4 \
\cb3 )\cb1 \
\cb3 st.sidebar.divider() \cb1 \
\
\cb3 st.sidebar.header(\cf7 \strokec7 "Probability Profiles"\cf0 \strokec4 )\cb1 \
\cb3 upload = st.sidebar.file_uploader(\cf7 \strokec7 "Import settings CSV"\cf0 \strokec4 , \cf2 \strokec2 type\cf0 \strokec4 =\cf7 \strokec7 "csv"\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  upload:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf2 \strokec2 try\cf0 \strokec4 :\cb1 \
\cb3         df_up = pd.read_csv(upload, index_col=\cf6 \strokec6 0\cf0 \strokec4 )\cb1 \
\cb3         imported, malformed_entries = \{\}, []\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  card_name, row \cf2 \strokec2 in\cf0 \strokec4  df_up.iterrows():\cb1 \
\cb3             evs, valid_card, num_events_csv = [], \cf2 \strokec2 True\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 for\cf0 \strokec4  i \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (\cf6 \strokec6 1\cf0 \strokec4 , MAX_EVENTS + \cf6 \strokec6 1\cf0 \strokec4 ):\cb1 \
\cb3                 pts_col, pts = COL_EVENT_PTS_TPL.\cf2 \strokec2 format\cf0 \strokec4 (i), row.get(COL_EVENT_PTS_TPL.\cf2 \strokec2 format\cf0 \strokec4 (i))\cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  pd.notna(pts) \cf2 \strokec2 and\cf0 \strokec4  pts > \cf6 \strokec6 0\cf0 \strokec4 :\cb1 \
\cb3                     num_events_csv += \cf6 \strokec6 1\cf0 \strokec4 ; round_cols = [COL_EVENT_ROUND_PROB_TPL.\cf2 \strokec2 format\cf0 \strokec4 (i, r + \cf6 \strokec6 1\cf0 \strokec4 ) \cf2 \strokec2 for\cf0 \strokec4  r \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (MAX_ROUNDS)]\cb1 \
\cb3                     missing_round_cols = [rc \cf2 \strokec2 for\cf0 \strokec4  rc \cf2 \strokec2 in\cf0 \strokec4  round_cols \cf2 \strokec2 if\cf0 \strokec4  rc \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  row.index \cf2 \strokec2 or\cf0 \strokec4  pd.isna(row[rc])]\cb1 \
\cb3                     \cf2 \strokec2 if\cf0 \strokec4  missing_round_cols: malformed_entries.append(\cf7 \strokec7 f"'\cf0 \strokec4 \{card_name\}\cf7 \strokec7 ' E\cf0 \strokec4 \{i\}\cf7 \strokec7 : missing \cf0 \strokec4 \{missing_round_cols\}\cf7 \strokec7 "\cf0 \strokec4 ); valid_card = \cf2 \strokec2 False\cf0 \strokec4 ; \cf2 \strokec2 break\cf0 \cb1 \strokec4 \
\cb3                     prs = [\cf2 \strokec2 int\cf0 \strokec4 (row.get(rc, \cf6 \strokec6 0\cf0 \strokec4 )) \cf2 \strokec2 for\cf0 \strokec4  rc \cf2 \strokec2 in\cf0 \strokec4  round_cols]; evs.append((\cf2 \strokec2 int\cf0 \strokec4 (pts), prs))\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  valid_card \cf2 \strokec2 and\cf0 \strokec4  evs:\cb1 \
\cb3                 imported[card_name] = evs\cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  card_name \cf2 \strokec2 in\cf0 \strokec4  DEFAULT_PROBS \cf2 \strokec2 and\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (evs) != \cf2 \strokec2 len\cf0 \strokec4 (DEFAULT_PROBS[card_name]): st.sidebar.warning(\cf7 \strokec7 f"'\cf0 \strokec4 \{card_name\}\cf7 \strokec7 ': imported \cf0 \strokec4 \{len(evs)\}\cf7 \strokec7  vs default \cf0 \strokec4 \{len(DEFAULT_PROBS[card_name])\}\cf7 \strokec7  events."\cf0 \strokec4 )\cb1 \
\cb3             \cf2 \strokec2 elif\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  evs \cf2 \strokec2 and\cf0 \strokec4  valid_card \cf2 \strokec2 and\cf0 \strokec4  card_name \cf2 \strokec2 in\cf0 \strokec4  df_up.index: malformed_entries.append(\cf7 \strokec7 f"'\cf0 \strokec4 \{card_name\}\cf7 \strokec7 ': No valid events."\cf0 \strokec4 )\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  malformed_entries: st.sidebar.error(\cf7 \strokec7 "CSV malformed. Not fully loaded. Errors:\\n- "\cf0 \strokec4  + \cf7 \strokec7 "\\n- "\cf0 \strokec4 .join(malformed_entries))\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  imported: \cb1 \
\cb3             st.session_state.PROB_EVENTS = imported\cb1 \
\cb3             st.sidebar.success(\cf7 \strokec7 "Profile imported!"\cf0 \strokec4 )\cb1 \
\cb3             st.rerun() \cb1 \
\cb3         \cf2 \strokec2 elif\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  malformed_entries : st.sidebar.warning(\cf7 \strokec7 "CSV empty or no valid data."\cf0 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 except\cf0 \strokec4  Exception \cf2 \strokec2 as\cf0 \strokec4  e: st.sidebar.error(\cf7 \strokec7 f"Error processing CSV: \cf0 \strokec4 \{e\}\cf7 \strokec7 "\cf0 \strokec4 )\cb1 \
\
\cb3 out_export = \{\}\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 for\cf0 \strokec4  card, evs \cf2 \strokec2 in\cf0 \strokec4  st.session_state.PROB_EVENTS.items():\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     rec = \{\};\cb1 \
\cb3     \cf2 \strokec2 for\cf0 \strokec4  idx, (pts, prs) \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (evs, start=\cf6 \strokec6 1\cf0 \strokec4 ):\cb1 \
\cb3         rec[COL_EVENT_PTS_TPL.\cf2 \strokec2 format\cf0 \strokec4 (idx)] = pts\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  r_loop_idx, p_val \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (prs, start=\cf6 \strokec6 1\cf0 \strokec4 ): rec[COL_EVENT_ROUND_PROB_TPL.\cf2 \strokec2 format\cf0 \strokec4 (idx, r_loop_idx)] = p_val \cb1 \
\cb3     out_export[card] = rec\cb1 \
\cb3 df_out = pd.DataFrame(out_export).T.fillna(\cf6 \strokec6 0\cf0 \strokec4 ).astype(\cf2 \strokec2 int\cf0 \strokec4 ); csv_buffer = io.StringIO(); df_out.to_csv(csv_buffer)\cb1 \
\cb3 st.sidebar.download_button(\cf7 \strokec7 "Export Current Profile as CSV"\cf0 \strokec4 , csv_buffer.getvalue(), \cf7 \strokec7 "probs.csv"\cf0 \strokec4 , \cf7 \strokec7 "text/csv"\cf0 \strokec4 )\cb1 \
\cb3 st.sidebar.divider()\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # UI: Edit per-round probabilities\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.header(\cf7 \strokec7 "\uc0\u9881 \u65039  Edit Mission Probabilities (Baseline)"\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 with\cf0 \strokec4  st.expander(\cf7 \strokec7 "Show/hide probability table"\cf0 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     updated_probs_edit = copy.deepcopy(st.session_state.PROB_EVENTS)\cb1 \
\cb3     \cb1 \
\cb3     cur_round_for_edit_display = cur_round \cf5 \strokec5 # Use the globally calculated cur_round\cf0 \cb1 \strokec4 \
\
\cb3     editable_user_cards = \{\cb1 \
\cb3         card_name: events \cf2 \strokec2 for\cf0 \strokec4  card_name, events \cf2 \strokec2 in\cf0 \strokec4  st.session_state.PROB_EVENTS.items()\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  card_name \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.scoreboard_used_cards \cf2 \strokec2 and\cf0 \strokec4  \\\cb1 \
\cb3            card_name \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.manually_removed_cards\cb1 \
\cb3     \}\cb1 \
\
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  editable_user_cards:\cb1 \
\cb3         st.info(\cf7 \strokec7 "All cards have been used or manually removed. No probabilities to edit for your deck."\cf0 \strokec4 )\cb1 \
\cb3     \cb1 \
\cb3     \cf2 \strokec2 for\cf0 \strokec4  card, evs \cf2 \strokec2 in\cf0 \strokec4  editable_user_cards.items(): \cb1 \
\cb3         st.markdown(\cf7 \strokec7 f"**\cf0 \strokec4 \{card\}\cf7 \strokec7 **"\cf0 \strokec4 ); new_evs_for_card = []\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  event_idx, (pts, prs_list) \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (evs, start=\cf6 \strokec6 1\cf0 \strokec4 ):\cb1 \
\cb3             num_future_rounds = MAX_ROUNDS - cur_round_for_edit_display\cb1 \
\cb3             num_cols_to_create = \cf6 \strokec6 1\cf0 \strokec4  + num_future_rounds \cf2 \strokec2 if\cf0 \strokec4  num_future_rounds > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 else\cf0 \strokec4  \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3             \cb1 \
\cb3             cols = st.columns(num_cols_to_create)\cb1 \
\cb3             cols[\cf6 \strokec6 0\cf0 \strokec4 ].markdown(\cf7 \strokec7 f"*VP: \cf0 \strokec4 \{pts\}\cf7 \strokec7 *"\cf0 \strokec4 )\cb1 \
\cb3             new_prs_for_event = \cf2 \strokec2 list\cf0 \strokec4 (prs_list) \cb1 \
\
\cb3             \cf2 \strokec2 if\cf0 \strokec4  num_future_rounds > \cf6 \strokec6 0\cf0 \strokec4 :\cb1 \
\cb3                 col_idx_offset = \cf6 \strokec6 1\cf0 \strokec4  \cb1 \
\cb3                 \cf2 \strokec2 for\cf0 \strokec4  r_game_round_0_indexed \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (cur_round_for_edit_display, MAX_ROUNDS):\cb1 \
\cb3                     r_game_round_1_indexed = r_game_round_0_indexed + \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3                     \cb1 \
\cb3                     prob_val = prs_list[r_game_round_0_indexed]\cb1 \
\cb3                     key = \cf7 \strokec7 f"edit_\cf0 \strokec4 \{card\}\cf7 \strokec7 _E\cf0 \strokec4 \{event_idx\}\cf7 \strokec7 _r\cf0 \strokec4 \{r_game_round_1_indexed\}\cf7 \strokec7 "\cf0 \cb1 \strokec4 \
\cb3                     default_cat_str = find_closest_category(prob_val, CATEGORIES, PCT_MAP)\cb1 \
\cb3                     \cb1 \
\cb3                     choice = cols[col_idx_offset].selectbox(\cb1 \
\cb3                         \cf7 \strokec7 f"R\cf0 \strokec4 \{r_game_round_1_indexed\}\cf7 \strokec7 "\cf0 \strokec4 , \cb1 \
\cb3                         CATEGORIES, \cb1 \
\cb3                         index=CATEGORIES.index(default_cat_str), \cb1 \
\cb3                         key=key, \cb1 \
\cb3                         label_visibility=\cf7 \strokec7 "visible"\cf0 \strokec4  \cb1 \
\cb3                     )\cb1 \
\cb3                     new_prs_for_event[r_game_round_0_indexed] = PCT_MAP.get(choice, \cf6 \strokec6 10\cf0 \strokec4 ) \cb1 \
\cb3                     col_idx_offset += \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3             \cb1 \
\cb3             new_evs_for_card.append((pts, new_prs_for_event))\cb1 \
\cb3         updated_probs_edit[card] = new_evs_for_card \cb1 \
\cb3         \cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  st.button(\cf7 \strokec7 "Apply Baseline Probability Changes"\cf0 \strokec4 ):\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  card_key \cf2 \strokec2 in\cf0 \strokec4  editable_user_cards.keys():\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  card_key \cf2 \strokec2 in\cf0 \strokec4  updated_probs_edit:\cb1 \
\cb3                  st.session_state.PROB_EVENTS[card_key] = updated_probs_edit[card_key]\cb1 \
\cb3         st.success(\cf7 \strokec7 "Baseline Probabilities updated for available cards!"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Live Scoreboard & Round Detection\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.header(\cf7 \strokec7 "\uc0\u55357 \u56523  Live Scoreboard & Current Round"\cf0 \strokec4 )\cb1 \
\
\cb3 current_scoreboard_used_cards_set = \cf2 \strokec2 set\cf0 \strokec4 ()\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 for\cf0 \strokec4  round_data_sb_init \cf2 \strokec2 in\cf0 \strokec4  st.session_state.scoreboard_data_list: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     current_scoreboard_used_cards_set.update(round_data_sb_init.get(\cf7 \strokec7 'used'\cf0 \strokec4 , []))\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  current_scoreboard_used_cards_set != st.session_state.scoreboard_used_cards:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.scoreboard_used_cards = current_scoreboard_used_cards_set\cb1 \
\
\cb3 current_opponent_scoreboard_used_cards_set = \cf2 \strokec2 set\cf0 \strokec4 ()\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 for\cf0 \strokec4  round_data_sb_init_opp \cf2 \strokec2 in\cf0 \strokec4  st.session_state.scoreboard_data_list:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     current_opponent_scoreboard_used_cards_set.update(round_data_sb_init_opp.get(\cf7 \strokec7 'opp_used'\cf0 \strokec4 , []))\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  current_opponent_scoreboard_used_cards_set != st.session_state.opponent_scoreboard_used_cards:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.opponent_scoreboard_used_cards = current_opponent_scoreboard_used_cards_set\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # cur_round is already calculated globally above\cf0 \cb1 \strokec4 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 total_s1, total_s2, total_p_raw = \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4  \cb1 \
\cb3 opp_total_s1, opp_total_s2, opp_total_p_raw = \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4 , \cf6 \strokec6 0\cf0 \strokec4  \cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 for\cf0 \strokec4  i_sb_form \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (MAX_ROUNDS): \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf2 \strokec2 with\cf0 \strokec4  st.container(border=\cf2 \strokec2 True\cf0 \strokec4 ): \cb1 \
\cb3         st.subheader(\cf7 \strokec7 f"Round \cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 "\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         st.markdown(\cf7 \strokec7 "**Your Scores**"\cf0 \strokec4 )\cb1 \
\cb3         user_cols = st.columns([\cf6 \strokec6 1\cf0 \strokec4 ,\cf6 \strokec6 1\cf0 \strokec4 ,\cf6 \strokec6 1\cf0 \strokec4 ,\cf6 \strokec6 2\cf0 \strokec4 ])\cb1 \
\cb3         round_data_form = st.session_state.scoreboard_data_list[i_sb_form] \cb1 \
\
\cb3         round_data_form[\cf7 \strokec7 's1'\cf0 \strokec4 ] = user_cols[\cf6 \strokec6 0\cf0 \strokec4 ].number_input(\cf7 \strokec7 f"Your Sec 1 VP (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , min_value=\cf6 \strokec6 0\cf0 \strokec4 , max_value=\cf6 \strokec6 15\cf0 \strokec4 , value=round_data_form.get(\cf7 \strokec7 's1'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ), key=\cf7 \strokec7 f"s1_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Your Secondary 1 VPs for this round"\cf0 \strokec4 )\cb1 \
\cb3         round_data_form[\cf7 \strokec7 's2'\cf0 \strokec4 ] = user_cols[\cf6 \strokec6 1\cf0 \strokec4 ].number_input(\cf7 \strokec7 f"Your Sec 2 VP (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , min_value=\cf6 \strokec6 0\cf0 \strokec4 , max_value=\cf6 \strokec6 15\cf0 \strokec4 , value=round_data_form.get(\cf7 \strokec7 's2'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ), key=\cf7 \strokec7 f"s2_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Your Secondary 2 VPs for this round"\cf0 \strokec4 )\cb1 \
\cb3         round_data_form[\cf7 \strokec7 'p'\cf0 \strokec4 ] = user_cols[\cf6 \strokec6 2\cf0 \strokec4 ].number_input(\cf7 \strokec7 f"Your Primary VP (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , min_value=\cf6 \strokec6 0\cf0 \strokec4 , max_value=\cf6 \strokec6 20\cf0 \strokec4 , value=round_data_form.get(\cf7 \strokec7 'p'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ), key=\cf7 \strokec7 f"p_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Your Primary VPs for this round"\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         other_rounds_used_cards = \cf2 \strokec2 set\cf0 \strokec4 ()\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  r_idx_sb_options, r_data_sb_options \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (st.session_state.scoreboard_data_list): \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  r_idx_sb_options != i_sb_form: other_rounds_used_cards.update(r_data_sb_options.get(\cf7 \strokec7 'used'\cf0 \strokec4 ,[]))\cb1 \
\cb3         \cb1 \
\cb3         card_options_for_this_round_user = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  CARD_LIST \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  other_rounds_used_cards]\cb1 \
\cb3         card_options_for_this_round_user = \cf2 \strokec2 sorted\cf0 \strokec4 (\cf2 \strokec2 list\cf0 \strokec4 (\cf2 \strokec2 set\cf0 \strokec4 (card_options_for_this_round_user + round_data_form.get(\cf7 \strokec7 'used'\cf0 \strokec4 ,[]))))\cb1 \
\
\cb3         round_data_form[\cf7 \strokec7 'used'\cf0 \strokec4 ] = user_cols[\cf6 \strokec6 3\cf0 \strokec4 ].multiselect(\cf7 \strokec7 f"Your Cards Used (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , options=card_options_for_this_round_user, default=round_data_form.get(\cf7 \strokec7 'used'\cf0 \strokec4 ,[]), key=\cf7 \strokec7 f"used_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , placeholder=\cf7 \strokec7 "Select your scored cards"\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Your Secondary cards scored/revealed this round"\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         total_s1 += round_data_form.get(\cf7 \strokec7 's1'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ); total_s2 += round_data_form.get(\cf7 \strokec7 's2'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ); total_p_raw += round_data_form.get(\cf7 \strokec7 'p'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         st.markdown(\cf7 \strokec7 "---"\cf0 \strokec4 ) \cb1 \
\cb3         st.markdown(\cf7 \strokec7 "**Opponent's Scores**"\cf0 \strokec4 )\cb1 \
\cb3         opp_cols = st.columns([\cf6 \strokec6 1\cf0 \strokec4 ,\cf6 \strokec6 1\cf0 \strokec4 ,\cf6 \strokec6 1\cf0 \strokec4 ,\cf6 \strokec6 2\cf0 \strokec4 ])\cb1 \
\cb3         round_data_form[\cf7 \strokec7 'opp_s1'\cf0 \strokec4 ] = opp_cols[\cf6 \strokec6 0\cf0 \strokec4 ].number_input(\cf7 \strokec7 f"Opp Sec 1 VP (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , min_value=\cf6 \strokec6 0\cf0 \strokec4 , max_value=\cf6 \strokec6 15\cf0 \strokec4 , value=round_data_form.get(\cf7 \strokec7 'opp_s1'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ), key=\cf7 \strokec7 f"opp_s1_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Opponent's Secondary 1 VPs"\cf0 \strokec4 )\cb1 \
\cb3         round_data_form[\cf7 \strokec7 'opp_s2'\cf0 \strokec4 ] = opp_cols[\cf6 \strokec6 1\cf0 \strokec4 ].number_input(\cf7 \strokec7 f"Opp Sec 2 VP (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , min_value=\cf6 \strokec6 0\cf0 \strokec4 , max_value=\cf6 \strokec6 15\cf0 \strokec4 , value=round_data_form.get(\cf7 \strokec7 'opp_s2'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ), key=\cf7 \strokec7 f"opp_s2_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Opponent's Secondary 2 VPs"\cf0 \strokec4 )\cb1 \
\cb3         round_data_form[\cf7 \strokec7 'opp_p'\cf0 \strokec4 ] = opp_cols[\cf6 \strokec6 2\cf0 \strokec4 ].number_input(\cf7 \strokec7 f"Opp Primary VP (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , min_value=\cf6 \strokec6 0\cf0 \strokec4 , max_value=\cf6 \strokec6 20\cf0 \strokec4 , value=round_data_form.get(\cf7 \strokec7 'opp_p'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ), key=\cf7 \strokec7 f"opp_p_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Opponent's Primary VPs"\cf0 \strokec4 )\cb1 \
\
\cb3         opp_other_rounds_used_cards = \cf2 \strokec2 set\cf0 \strokec4 ()\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  r_idx_opp_options, r_data_opp_options \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (st.session_state.scoreboard_data_list):\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  r_idx_opp_options != i_sb_form: opp_other_rounds_used_cards.update(r_data_opp_options.get(\cf7 \strokec7 'opp_used'\cf0 \strokec4 ,[]))\cb1 \
\cb3         \cb1 \
\cb3         card_options_for_opp_this_round = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  CARD_LIST \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  opp_other_rounds_used_cards]\cb1 \
\cb3         card_options_for_opp_this_round = \cf2 \strokec2 sorted\cf0 \strokec4 (\cf2 \strokec2 list\cf0 \strokec4 (\cf2 \strokec2 set\cf0 \strokec4 (card_options_for_opp_this_round + round_data_form.get(\cf7 \strokec7 'opp_used'\cf0 \strokec4 ,[]))))\cb1 \
\
\cb3         round_data_form[\cf7 \strokec7 'opp_used'\cf0 \strokec4 ] = opp_cols[\cf6 \strokec6 3\cf0 \strokec4 ].multiselect(\cf7 \strokec7 f"Opp Cards Used (R\cf0 \strokec4 \{i_sb_form+1\}\cf7 \strokec7 )"\cf0 \strokec4 , options=card_options_for_opp_this_round, default=round_data_form.get(\cf7 \strokec7 'opp_used'\cf0 \strokec4 ,[]), key=\cf7 \strokec7 f"opp_used_r\cf0 \strokec4 \{i_sb_form\}\cf7 \strokec7 "\cf0 \strokec4 , placeholder=\cf7 \strokec7 "Select opponent's cards"\cf0 \strokec4 , label_visibility=\cf7 \strokec7 "collapsed"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Opponent's Secondary cards scored/revealed"\cf0 \strokec4 )\cb1 \
\
\cb3         opp_total_s1 += round_data_form.get(\cf7 \strokec7 'opp_s1'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ); opp_total_s2 += round_data_form.get(\cf7 \strokec7 'opp_s2'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 ); opp_total_p_raw += round_data_form.get(\cf7 \strokec7 'opp_p'\cf0 \strokec4 ,\cf6 \strokec6 0\cf0 \strokec4 )\cb1 \
\cb3         \cb1 \
\cb3         st.session_state.scoreboard_data_list[i_sb_form] = round_data_form\cb1 \
\
\cb3 st.write(\cf7 \strokec7 f"**Current Game Round (for active play):** \cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7  (Internal 0-indexed: \cf0 \strokec4 \{cur_round\}\cf7 \strokec7 )"\cf0 \strokec4 )\cb1 \
\
\cb3 sec_total = \cf2 \strokec2 min\cf0 \strokec4 (total_s1 + total_s2, MAX_SECONDARY_SCORE)\cb1 \
\cb3 pri_total = \cf2 \strokec2 min\cf0 \strokec4 (total_p_raw, MAX_PRIMARY_SCORE)\cb1 \
\cb3 opp_sec_total = \cf2 \strokec2 min\cf0 \strokec4 (opp_total_s1 + opp_total_s2, MAX_SECONDARY_SCORE)\cb1 \
\cb3 opp_pri_total = \cf2 \strokec2 min\cf0 \strokec4 (opp_total_p_raw, MAX_PRIMARY_SCORE)\cb1 \
\
\cb3 st.session_state.opponent_total_sim_future_vp = calculate_opponent_future_secondary_vp(\cb1 \
\cb3     cur_round, \cb1 \
\cb3     st.session_state.opponent_scoreboard_used_cards, \cb1 \
\cb3     st.session_state.opponent_manually_removed_cards, \cb1 \
\cb3     st.session_state.OPPONENT_PROB_EVENTS, \cb1 \
\cb3     opp_sec_total\cb1 \
\cb3 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Card Pool Management\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.sidebar.divider()\cb1 \
\cb3 st.sidebar.header(\cf7 \strokec7 "Card Deck Management (Your Deck)"\cf0 \strokec4 )\cb1 \
\cb3 st.sidebar.write(\cf7 \strokec7 "**Your Scoreboard Used Cards:**"\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  st.session_state.scoreboard_used_cards: st.sidebar.write(\cf7 \strokec7 ", "\cf0 \strokec4 .join(\cf2 \strokec2 sorted\cf0 \strokec4 (\cf2 \strokec2 list\cf0 \strokec4 (st.session_state.scoreboard_used_cards))))\cb1 \
\cf2 \cb3 \strokec2 else\cf0 \strokec4 : st.sidebar.write(\cf7 \strokec7 "*None yet*"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 potential_cards_for_manual_removal = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  CARD_LIST \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.scoreboard_used_cards]\cb1 \
\cb3 valid_defaults_for_manual_removal = [\cb1 \
\cb3     card \cf2 \strokec2 for\cf0 \strokec4  card \cf2 \strokec2 in\cf0 \strokec4  st.session_state.manually_removed_cards \cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  card \cf2 \strokec2 in\cf0 \strokec4  potential_cards_for_manual_removal\cb1 \
\cb3 ]\cb1 \
\cb3 selected_manual_removals = st.sidebar.multiselect(\cb1 \
\cb3     \cf7 \strokec7 "Manually Remove Cards from Your Deck:"\cf0 \strokec4 , \cb1 \
\cb3     options=\cf2 \strokec2 sorted\cf0 \strokec4 (potential_cards_for_manual_removal), \cb1 \
\cb3     default=valid_defaults_for_manual_removal, \cb1 \
\cb3     \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Select cards to remove from your draw pool."\cf0 \cb1 \strokec4 \
\cb3 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 set\cf0 \strokec4 (selected_manual_removals) != st.session_state.manually_removed_cards:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.manually_removed_cards = \cf2 \strokec2 set\cf0 \strokec4 (selected_manual_removals)\cb1 \
\cb3     st.rerun() \cb1 \
\
\cb3 AVAILABLE_DRAW_POOL = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  CARD_LIST \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.scoreboard_used_cards \cf2 \strokec2 and\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.manually_removed_cards]\cb1 \
\cb3 st.sidebar.write(\cf7 \strokec7 "**Your Available Draw Pool Size:** "\cf0 \strokec4  + \cf2 \strokec2 str\cf0 \strokec4 (\cf2 \strokec2 len\cf0 \strokec4 (AVAILABLE_DRAW_POOL)))\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 with\cf0 \strokec4  st.sidebar.expander(\cf7 \strokec7 "View Your Available Draw Pool"\cf0 \strokec4 ): st.write(\cf7 \strokec7 ", "\cf0 \strokec4 .join(\cf2 \strokec2 sorted\cf0 \strokec4 (AVAILABLE_DRAW_POOL)) \cf2 \strokec2 if\cf0 \strokec4  AVAILABLE_DRAW_POOL \cf2 \strokec2 else\cf0 \strokec4  \cf7 \strokec7 "*Empty*"\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.sidebar.divider()\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # Opponent Card Pool Management \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.sidebar.header(\cf7 \strokec7 "Card Deck Management (Opponent's Deck)"\cf0 \strokec4 )\cb1 \
\cb3 st.sidebar.write(\cf7 \strokec7 "**Opponent's Scoreboard Used Cards:**"\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  st.session_state.opponent_scoreboard_used_cards: st.sidebar.write(\cf7 \strokec7 ", "\cf0 \strokec4 .join(\cf2 \strokec2 sorted\cf0 \strokec4 (\cf2 \strokec2 list\cf0 \strokec4 (st.session_state.opponent_scoreboard_used_cards))))\cb1 \
\cf2 \cb3 \strokec2 else\cf0 \strokec4 : st.sidebar.write(\cf7 \strokec7 "*None yet*"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 potential_cards_for_opp_manual_removal = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  CARD_LIST \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.opponent_scoreboard_used_cards]\cb1 \
\cb3 valid_defaults_for_opp_manual_removal = [\cb1 \
\cb3     card \cf2 \strokec2 for\cf0 \strokec4  card \cf2 \strokec2 in\cf0 \strokec4  st.session_state.opponent_manually_removed_cards\cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  card \cf2 \strokec2 in\cf0 \strokec4  potential_cards_for_opp_manual_removal\cb1 \
\cb3 ]\cb1 \
\cb3 selected_opp_manual_removals = st.sidebar.multiselect(\cb1 \
\cb3     \cf7 \strokec7 "Manually Remove Cards from Opponent's Deck:"\cf0 \strokec4 ,\cb1 \
\cb3     options=\cf2 \strokec2 sorted\cf0 \strokec4 (potential_cards_for_opp_manual_removal),\cb1 \
\cb3     default=valid_defaults_for_opp_manual_removal,\cb1 \
\cb3     \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Select cards to remove from the opponent's draw pool (e.g., you know they discarded it)."\cf0 \strokec4 ,\cb1 \
\cb3     key=\cf7 \strokec7 "opp_manual_remove"\cf0 \cb1 \strokec4 \
\cb3 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 set\cf0 \strokec4 (selected_opp_manual_removals) != st.session_state.opponent_manually_removed_cards:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.opponent_manually_removed_cards = \cf2 \strokec2 set\cf0 \strokec4 (selected_opp_manual_removals)\cb1 \
\cb3     st.rerun()\cb1 \
\
\cb3 OPPONENT_AVAILABLE_DRAW_POOL = [\cb1 \
\cb3     c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  CARD_LIST \cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.opponent_scoreboard_used_cards \cb1 \
\cb3     \cf2 \strokec2 and\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.opponent_manually_removed_cards\cb1 \
\cb3 ]\cb1 \
\cb3 st.sidebar.write(\cf7 \strokec7 "**Opponent's Available Draw Pool Size:** "\cf0 \strokec4  + \cf2 \strokec2 str\cf0 \strokec4 (\cf2 \strokec2 len\cf0 \strokec4 (OPPONENT_AVAILABLE_DRAW_POOL)))\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 with\cf0 \strokec4  st.sidebar.expander(\cf7 \strokec7 "View Opponent's Available Draw Pool"\cf0 \strokec4 ): st.write(\cf7 \strokec7 ", "\cf0 \strokec4 .join(\cf2 \strokec2 sorted\cf0 \strokec4 (OPPONENT_AVAILABLE_DRAW_POOL)) \cf2 \strokec2 if\cf0 \strokec4  OPPONENT_AVAILABLE_DRAW_POOL \cf2 \strokec2 else\cf0 \strokec4  \cf7 \strokec7 "*Empty*"\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.sidebar.divider()\cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Active Missions & Discard Recommendation\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.header(\cf7 \strokec7 f"\uc0\u55356 \u57263  Your Active Missions & EV for Round \cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7 "\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  cur_round != st.session_state.last_known_cur_round_for_overrides \cf2 \strokec2 or\cf0 \strokec4  \\\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3    \cf2 \strokec2 set\cf0 \strokec4 (st.session_state.active_current) != \cf2 \strokec2 set\cf0 \strokec4 (st.session_state.last_known_active_cards_for_overrides):\cb1 \
\cb3     st.session_state.active_mission_overrides = \{\}\cb1 \
\cb3     st.session_state.last_known_cur_round_for_overrides = cur_round\cb1 \
\cb3     st.session_state.last_known_active_cards_for_overrides = \cf2 \strokec2 list\cf0 \strokec4 (st.session_state.active_current)\cb1 \
\cb3     st.session_state.current_active_hand_ev = \cf6 \strokec6 0.0\cf0 \strokec4  \cb1 \
\
\cb3 active_opts_for_selection = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  AVAILABLE_DRAW_POOL \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.active_current] \cb1 \
\cb3 active_opts_for_selection = \cf2 \strokec2 sorted\cf0 \strokec4 (\cf2 \strokec2 list\cf0 \strokec4 (\cf2 \strokec2 set\cf0 \strokec4 (active_opts_for_selection + st.session_state.active_current)))\cb1 \
\
\cb3 active_current_selection = st.multiselect(\cf7 \strokec7 f"Select up to 2 active missions for Round \cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7 "\cf0 \strokec4 , options=active_opts_for_selection, default=st.session_state.active_current, key=\cf7 \strokec7 "active_current_multiselect"\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 set\cf0 \strokec4 (active_current_selection) != \cf2 \strokec2 set\cf0 \strokec4 (st.session_state.active_current): \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.session_state.active_current = active_current_selection\cb1 \
\cb3     st.session_state.active_mission_overrides = \{\} \cb1 \
\cb3     st.session_state.last_known_active_cards_for_overrides = \cf2 \strokec2 list\cf0 \strokec4 (st.session_state.active_current) \cb1 \
\cb3     st.rerun() \cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (st.session_state.active_current) > \cf6 \strokec6 2\cf0 \strokec4 : st.error(\cf7 \strokec7 "Max 2 active missions. Please deselect some."\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 ev_current_hand_for_active_section = \cf6 \strokec6 0.0\cf0 \strokec4  \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  cur_round < MAX_ROUNDS \cf2 \strokec2 and\cf0 \strokec4  st.session_state.active_current:\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.subheader(\cf7 \strokec7 f"\uc0\u9889  Adjust Probabilities & See EV for Your Hand in Round \cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7 "\cf0 \strokec4 )\cb1 \
\cb3     current_hand_for_ev_calc = st.session_state.active_current \cb1 \
\cb3     \cb1 \
\cb3     \cf2 \strokec2 for\cf0 \strokec4  card_name_active \cf2 \strokec2 in\cf0 \strokec4  current_hand_for_ev_calc: \cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  card_name_active \cf2 \strokec2 in\cf0 \strokec4  st.session_state.PROB_EVENTS:\cb1 \
\cb3             st.markdown(\cf7 \strokec7 f"**\cf0 \strokec4 \{card_name_active\}\cf7 \strokec7 **"\cf0 \strokec4 )\cb1 \
\cb3             card_events_data = st.session_state.PROB_EVENTS[card_name_active]\cb1 \
\cb3             \cf2 \strokec2 for\cf0 \strokec4  i_event_override, (pts, prs_list) \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (card_events_data): \cb1 \
\cb3                 prob_for_cur_round_default = prs_list[cur_round] \cb1 \
\cb3                 override_key = \cf7 \strokec7 f"override_\cf0 \strokec4 \{card_name_active\}\cf7 \strokec7 _E\cf0 \strokec4 \{i_event_override+1\}\cf7 \strokec7 _R\cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7 "\cf0 \cb1 \strokec4 \
\cb3                 \cb1 \
\cb3                 current_display_prob = st.session_state.active_mission_overrides.get(override_key, prob_for_cur_round_default)\cb1 \
\cb3                 default_cat_str = find_closest_category(current_display_prob, CATEGORIES, PCT_MAP)\cb1 \
\cb3                 \cb1 \
\cb3                 choice_cat = st.selectbox(\cf7 \strokec7 f"Event \cf0 \strokec4 \{i_event_override+1\}\cf7 \strokec7  (\cf0 \strokec4 \{pts\}\cf7 \strokec7  VP) - Chance for R\cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7 "\cf0 \strokec4 , CATEGORIES,\cb1 \
\cb3                                        index=CATEGORIES.index(default_cat_str),\cb1 \
\cb3                                        key=override_key + \cf7 \strokec7 "_sb"\cf0 \strokec4 ) \cb1 \
\cb3                 \cb1 \
\cb3                 chosen_pct_value = PCT_MAP.get(choice_cat, \cf6 \strokec6 10\cf0 \strokec4 )\cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  override_key \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.active_mission_overrides \cf2 \strokec2 or\cf0 \strokec4  \\\cb1 \
\cb3                    st.session_state.active_mission_overrides[override_key] != chosen_pct_value:\cb1 \
\cb3                     st.session_state.active_mission_overrides[override_key] = chosen_pct_value\cb1 \
\cb3     \cb1 \
\cb3     ev_current_hand_for_active_section = calculate_hand_ev_for_round(current_hand_for_ev_calc, cur_round, st.session_state.PROB_EVENTS, st.session_state.active_mission_overrides)\cb1 \
\cb3     st.session_state.current_active_hand_ev = ev_current_hand_for_active_section \cb1 \
\
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (current_hand_for_ev_calc) > \cf6 \strokec6 0\cf0 \strokec4  :\cb1 \
\cb3         best_discard_option = \{\cf7 \strokec7 "card_to_discard"\cf0 \strokec4 : \cf2 \strokec2 None\cf0 \strokec4 , \cf7 \strokec7 "avg_ev_if_redrawn"\cf0 \strokec4 : ev_current_hand_for_active_section, \cf7 \strokec7 "improvement"\cf0 \strokec4 : \cf6 \strokec6 0\cf0 \strokec4 \}\cb1 \
\cb3         deck_for_redraw = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  AVAILABLE_DRAW_POOL \cf2 \strokec2 if\cf0 \strokec4  c \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  current_hand_for_ev_calc] \cb1 \
\
\cb3         \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  deck_for_redraw: st.write(\cf7 \strokec7 "*No cards available in your deck to redraw.*"\cf0 \strokec4 )\cb1 \
\cb3         \cf2 \strokec2 else\cf0 \strokec4 :\cb1 \
\cb3             \cf2 \strokec2 for\cf0 \strokec4  card_in_hand_to_discard \cf2 \strokec2 in\cf0 \strokec4  current_hand_for_ev_calc:\cb1 \
\cb3                 temp_hand_after_discard = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  current_hand_for_ev_calc \cf2 \strokec2 if\cf0 \strokec4  c != card_in_hand_to_discard]\cb1 \
\cb3                 sum_ev_of_potential_new_hands = \cf6 \strokec6 0\cf0 \cb1 \strokec4 \
\cb3                 \cf2 \strokec2 for\cf0 \strokec4  replacement_card_from_deck \cf2 \strokec2 in\cf0 \strokec4  deck_for_redraw:\cb1 \
\cb3                     hypothetical_hand = temp_hand_after_discard + [replacement_card_from_deck]\cb1 \
\cb3                     temp_overrides_for_kept_cards = \{\}\cb1 \
\cb3                     \cf2 \strokec2 for\cf0 \strokec4  kept_card \cf2 \strokec2 in\cf0 \strokec4  temp_hand_after_discard:\cb1 \
\cb3                         \cf2 \strokec2 if\cf0 \strokec4  kept_card \cf2 \strokec2 in\cf0 \strokec4  st.session_state.PROB_EVENTS: \cb1 \
\cb3                             \cf2 \strokec2 for\cf0 \strokec4  event_j, (\cf2 \strokec2 _\cf0 \strokec4 , \cf2 \strokec2 _\cf0 \strokec4 ) \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (st.session_state.PROB_EVENTS[kept_card]):\cb1 \
\cb3                                 kept_override_key = \cf7 \strokec7 f"override_\cf0 \strokec4 \{kept_card\}\cf7 \strokec7 _E\cf0 \strokec4 \{event_j+1\}\cf7 \strokec7 _R\cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7 "\cf0 \cb1 \strokec4 \
\cb3                                 \cf2 \strokec2 if\cf0 \strokec4  kept_override_key \cf2 \strokec2 in\cf0 \strokec4  st.session_state.active_mission_overrides:\cb1 \
\cb3                                     temp_overrides_for_kept_cards[kept_override_key] = st.session_state.active_mission_overrides[kept_override_key]\cb1 \
\cb3                     sum_ev_of_potential_new_hands += calculate_hand_ev_for_round(hypothetical_hand, cur_round, st.session_state.PROB_EVENTS, temp_overrides_for_kept_cards)\cb1 \
\cb3                 \cb1 \
\cb3                 avg_ev_this_discard_path = sum_ev_of_potential_new_hands / \cf2 \strokec2 len\cf0 \strokec4 (deck_for_redraw)\cb1 \
\cb3                 improvement = avg_ev_this_discard_path - ev_current_hand_for_active_section\cb1 \
\cb3                 st.write(\cf7 \strokec7 f"- If '\cf0 \strokec4 \{card_in_hand_to_discard\}\cf7 \strokec7 ' is discarded, average EV with redraw: \cf0 \strokec4 \{avg_ev_this_discard_path\cf7 \strokec7 :.2f\cf0 \strokec4 \}\cf7 \strokec7  VP (Improvement: \cf0 \strokec4 \{improvement\cf7 \strokec7 :.2f\cf0 \strokec4 \}\cf7 \strokec7  VP)"\cf0 \strokec4 )\cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  improvement > best_discard_option[\cf7 \strokec7 "improvement"\cf0 \strokec4 ]: best_discard_option = \{\cf7 \strokec7 "card_to_discard"\cf0 \strokec4 : card_in_hand_to_discard, \cf7 \strokec7 "avg_ev_if_redrawn"\cf0 \strokec4 : avg_ev_this_discard_path, \cf7 \strokec7 "improvement"\cf0 \strokec4 : improvement\}\cb1 \
\cb3             \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  best_discard_option[\cf7 \strokec7 "card_to_discard"\cf0 \strokec4 ] \cf2 \strokec2 and\cf0 \strokec4  best_discard_option[\cf7 \strokec7 "improvement"\cf0 \strokec4 ] > \cf6 \strokec6 0.05\cf0 \strokec4 : st.success(\cf7 \strokec7 f"**Recommendation: Discard '\cf0 \strokec4 \{best_discard_option['card_to_discard']\}\cf7 \strokec7 '.** Expected EV gain: \cf0 \strokec4 \{best_discard_option['improvement']\cf7 \strokec7 :.2f\cf0 \strokec4 \}\cf7 \strokec7  VP."\cf0 \strokec4 )\cb1 \
\cb3             \cf2 \strokec2 else\cf0 \strokec4 : st.info(\cf7 \strokec7 "**Recommendation: Keep current hand.** No discard option offers significant EV improvement."\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 else\cf0 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.write(\cf7 \strokec7 "Select your active missions to see EV and discard recommendations for the current round."\cf0 \strokec4 )\cb1 \
\cb3     st.session_state.current_active_hand_ev = \cf6 \strokec6 0.0\cf0 \strokec4  \cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 with\cf0 \strokec4  st.expander(\cf7 \strokec7 "View Your Available Draw Pool (Main UI)"\cf0 \strokec4 , expanded=\cf2 \strokec2 False\cf0 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.write(\cf7 \strokec7 f"**Size:** \cf0 \strokec4 \{len(AVAILABLE_DRAW_POOL)\}\cf7 \strokec7 "\cf0 \strokec4 )\cb1 \
\cb3     st.write(\cf7 \strokec7 ", "\cf0 \strokec4 .join(\cf2 \strokec2 sorted\cf0 \strokec4 (AVAILABLE_DRAW_POOL)) \cf2 \strokec2 if\cf0 \strokec4  AVAILABLE_DRAW_POOL \cf2 \strokec2 else\cf0 \strokec4  \cf7 \strokec7 "*Empty*"\cf0 \strokec4 )\cb1 \
\cb3 st.divider()\cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # VP Summary & Projections\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.header(\cf7 \strokec7 "\uc0\u55357 \u56522  VP Summary & Projections"\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # User Scores\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.subheader(\cf7 \strokec7 "Your Score"\cf0 \strokec4 )\cb1 \
\cb3 user_summary_cols = st.columns(\cf6 \strokec6 3\cf0 \strokec4 )\cb1 \
\cb3 user_current_grand_total_calc = sec_total + pri_total \cb1 \
\cb3 user_start_vp_label = \cf7 \strokec7 ""\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  st.session_state.get(\cf7 \strokec7 'include_start_vp'\cf0 \strokec4 , \cf2 \strokec2 True\cf0 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     user_current_grand_total_calc += START_VP\cb1 \
\cb3     user_start_vp_label = \cf7 \strokec7 " (incl. Start VP)"\cf0 \cb1 \strokec4 \
\
\cb3 user_summary_cols[\cf6 \strokec6 0\cf0 \strokec4 ].metric(\cf7 \strokec7 "Your Scored Secondary VP"\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{int(sec_total)\}\cf7 \strokec7  VP"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 f"Max \cf0 \strokec4 \{MAX_SECONDARY_SCORE\}\cf7 \strokec7  VP from secondaries."\cf0 \strokec4 )\cb1 \
\cb3 user_summary_cols[\cf6 \strokec6 1\cf0 \strokec4 ].metric(\cf7 \strokec7 "Your Entered Primary VP"\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{int(pri_total)\}\cf7 \strokec7  VP"\cf0 \strokec4 , \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 f"Max \cf0 \strokec4 \{MAX_PRIMARY_SCORE\}\cf7 \strokec7  VP from primaries."\cf0 \strokec4 ) \cb1 \
\cb3 user_summary_cols[\cf6 \strokec6 2\cf0 \strokec4 ].metric(\cf7 \strokec7 f"Your Current Grand Total\cf0 \strokec4 \{user_start_vp_label\}\cf7 \strokec7 "\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{int(user_current_grand_total_calc)\}\cf7 \strokec7  VP"\cf0 \strokec4 )\cb1 \
\
\cb3 active_hand_ev_display_val = st.session_state.get(\cf7 \strokec7 'current_active_hand_ev'\cf0 \strokec4 , \cf6 \strokec6 0.0\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  st.session_state.active_current \cf2 \strokec2 and\cf0 \strokec4  cur_round < MAX_ROUNDS: \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.metric(\cf7 \strokec7 f"EV of Your Active Hand (R\cf0 \strokec4 \{cur_round+1\}\cf7 \strokec7 )"\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{active_hand_ev_display_val\cf7 \strokec7 :.2f\cf0 \strokec4 \}\cf7 \strokec7  VP"\cf0 \strokec4 ,\cb1 \
\cb3               \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 "Expected VPs from your currently selected active missions for this round, considering any probability adjustments you've made above."\cf0 \strokec4 )\cb1 \
\
\cb3 user_sim_future_vp_val = st.session_state.get(\cf7 \strokec7 'total_sim_future_vp'\cf0 \strokec4 , \cf6 \strokec6 0.0\cf0 \strokec4 ) \cb1 \
\cb3 sim_has_run_indicator = \cf7 \strokec7 'run_sim_button_main'\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state \cf2 \strokec2 and\cf0 \strokec4  st.session_state.run_sim_button_main\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  user_sim_future_vp_val > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 or\cf0 \strokec4  sim_has_run_indicator : \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.metric(\cf7 \strokec7 "Your Simulated Future Secondary VP"\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{user_sim_future_vp_val\cf7 \strokec7 :.2f\cf0 \strokec4 \}\cf7 \strokec7  VP"\cf0 \strokec4 ,\cb1 \
\cb3               \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 f"Average VPs expected from your secondary missions in future rounds, based on the last simulation run. This does NOT include the EV of your current active hand. Total secondary VPs (scored + future) will not exceed \cf0 \strokec4 \{MAX_SECONDARY_SCORE\}\cf7 \strokec7 ."\cf0 \strokec4 )\cb1 \
\cb3     \cb1 \
\cb3     user_projected_total_vp_calc = sec_total + pri_total + user_sim_future_vp_val \cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  st.session_state.get(\cf7 \strokec7 'include_start_vp'\cf0 \strokec4 , \cf2 \strokec2 True\cf0 \strokec4 ): user_projected_total_vp_calc += START_VP\cb1 \
\cb3     \cb1 \
\cb3     st.metric(\cf7 \strokec7 f"Your Projected Game End Total VP\cf0 \strokec4 \{user_start_vp_label\}\cf7 \strokec7 "\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{user_projected_total_vp_calc\cf7 \strokec7 :.2f\cf0 \strokec4 \}\cf7 \strokec7  VP"\cf0 \strokec4 ,\cb1 \
\cb3               \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 f"Sum of your current VPs and your simulated future secondary VPs. Primary capped at \cf0 \strokec4 \{MAX_PRIMARY_SCORE\}\cf7 \strokec7 , total Secondary at \cf0 \strokec4 \{MAX_SECONDARY_SCORE\}\cf7 \strokec7 ."\cf0 \strokec4 )\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 else\cf0 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.info(\cf7 \strokec7 "Run a 'Future Rounds Simulation' (in sidebar) to see your projected VPs."\cf0 \strokec4 )\cb1 \
\
\cb3 st.divider()\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # Opponent Scores - SIMPLIFIED DISPLAY\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.subheader(\cf7 \strokec7 "Opponent's Score"\cf0 \strokec4 )\cb1 \
\cb3 opp_current_grand_total_calc = opp_sec_total + opp_pri_total\cb1 \
\cb3 opp_start_vp_label = \cf7 \strokec7 ""\cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  st.session_state.get(\cf7 \strokec7 'include_start_vp'\cf0 \strokec4 , \cf2 \strokec2 True\cf0 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     opp_current_grand_total_calc += START_VP\cb1 \
\cb3     opp_start_vp_label = \cf7 \strokec7 " (incl. Start VP)"\cf0 \cb1 \strokec4 \
\
\cb3 st.metric(\cf7 \strokec7 f"Opponent's Current Grand Total\cf0 \strokec4 \{opp_start_vp_label\}\cf7 \strokec7 "\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{int(opp_current_grand_total_calc)\}\cf7 \strokec7  VP"\cf0 \strokec4 ,\cb1 \
\cb3           \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 f"Sum of opponent's entered secondary (max \cf0 \strokec4 \{MAX_SECONDARY_SCORE\}\cf7 \strokec7 ) and primary (max \cf0 \strokec4 \{MAX_PRIMARY_SCORE\}\cf7 \strokec7 ) VPs, plus starting VP if selected."\cf0 \strokec4 )\cb1 \
\
\cb3 opp_sim_future_vp_val = st.session_state.get(\cf7 \strokec7 'opponent_total_sim_future_vp'\cf0 \strokec4 , \cf6 \strokec6 0.0\cf0 \strokec4 )\cb1 \
\cb3 opp_projected_total_vp_calc = opp_sec_total + opp_pri_total + opp_sim_future_vp_val \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  st.session_state.get(\cf7 \strokec7 'include_start_vp'\cf0 \strokec4 , \cf2 \strokec2 True\cf0 \strokec4 ): opp_projected_total_vp_calc += START_VP\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.metric(\cf7 \strokec7 f"Opponent's Projected Game End Total VP\cf0 \strokec4 \{opp_start_vp_label\}\cf7 \strokec7 "\cf0 \strokec4 , \cf7 \strokec7 f"\cf0 \strokec4 \{opp_projected_total_vp_calc\cf7 \strokec7 :.2f\cf0 \strokec4 \}\cf7 \strokec7  VP"\cf0 \strokec4 ,\cb1 \
\cb3             \cf2 \strokec2 help\cf0 \strokec4 =\cf7 \strokec7 f"Sum of opponent's current VPs and their projected future secondary VPs (based on optimal play using their probabilities). Primary capped at \cf0 \strokec4 \{MAX_PRIMARY_SCORE\}\cf7 \strokec7 , total Secondary at \cf0 \strokec4 \{MAX_SECONDARY_SCORE\}\cf7 \strokec7 ."\cf0 \strokec4 )\cb1 \
\
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Future simulation (User's Simulation)\cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 def\cf0 \strokec4  simulate_future(initial_deck_for_sim, current_app_round_sim, allow_discard_in_sim, num_trials, prob_events_data_sim, current_user_sec_score): \cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     \cf7 \strokec7 """Simulates future rounds for the user: draw 2, optional discard/redraw (optimal for round), score. Respects MAX_SECONDARY_SCORE cap."""\cf0 \cb1 \strokec4 \
\cb3     round_total_vps_sim = \{r_sim_loop: \cf6 \strokec6 0.0\cf0 \strokec4  \cf2 \strokec2 for\cf0 \strokec4  r_sim_loop \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (current_app_round_sim + \cf6 \strokec6 1\cf0 \strokec4 , MAX_ROUNDS)\} \cb1 \
\cb3     \cb1 \
\cb3     total_future_vp_across_trials = \cf6 \strokec6 0.0\cf0 \cb1 \strokec4 \
\
\cb3     \cf2 \strokec2 for\cf0 \strokec4  \cf2 \strokec2 _\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (num_trials):\cb1 \
\cb3         trial_deck_sim = \cf2 \strokec2 list\cf0 \strokec4 (initial_deck_for_sim); random.shuffle(trial_deck_sim) \cb1 \
\cb3         trial_future_secondary_vp = \cf6 \strokec6 0.0\cf0 \strokec4  \cf5 \strokec5 # VP scored in this specific trial from future rounds\cf0 \cb1 \strokec4 \
\
\cb3         \cf5 \strokec5 # Iterate through future rounds for this trial\cf0 \cb1 \strokec4 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  r_val_sim \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (current_app_round_sim + \cf6 \strokec6 1\cf0 \strokec4 , MAX_ROUNDS): \cb1 \
\cb3             \cf5 \strokec5 # Stop if overall secondary cap already met by previously scored VPs + VPs from *this trial's* earlier future rounds\cf0 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  current_user_sec_score + trial_future_secondary_vp >= MAX_SECONDARY_SCORE:\cb1 \
\cb3                 \cf2 \strokec2 break\cf0 \strokec4  \cb1 \
\
\cb3             current_sim_hand_trial = []; \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (trial_deck_sim) >= \cf6 \strokec6 2\cf0 \strokec4 : current_sim_hand_trial = [trial_deck_sim.pop(\cf6 \strokec6 0\cf0 \strokec4 ), trial_deck_sim.pop(\cf6 \strokec6 0\cf0 \strokec4 )]\cb1 \
\cb3             \cf2 \strokec2 elif\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (trial_deck_sim) == \cf6 \strokec6 1\cf0 \strokec4 : current_sim_hand_trial = [trial_deck_sim.pop(\cf6 \strokec6 0\cf0 \strokec4 )]\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  current_sim_hand_trial: \cf2 \strokec2 continue\cf0 \strokec4  \cf5 \strokec5 # No cards to play with this round\cf0 \cb1 \strokec4 \
\cb3             \cb1 \
\cb3             final_hand_for_scoring_this_round_sim = \cf2 \strokec2 list\cf0 \strokec4 (current_sim_hand_trial) \cb1 \
\cb3             \cf5 \strokec5 # Discard/Redraw logic for the simulated hand\cf0 \cb1 \strokec4 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  allow_discard_in_sim \cf2 \strokec2 and\cf0 \strokec4  current_sim_hand_trial \cf2 \strokec2 and\cf0 \strokec4  trial_deck_sim: \cb1 \
\cb3                 ev_current_sim_hand_this_round_sim = calculate_hand_ev_for_round(current_sim_hand_trial, r_val_sim, prob_events_data_sim, \cf2 \strokec2 None\cf0 \strokec4 ) \cb1 \
\cb3                 best_ev_after_discard_sim, card_to_discard_for_sim_trial = ev_current_sim_hand_this_round_sim, \cf2 \strokec2 None\cf0 \strokec4  \cb1 \
\cb3                 \cb1 \
\cb3                 \cf2 \strokec2 for\cf0 \strokec4  card_to_try_discarding_sim \cf2 \strokec2 in\cf0 \strokec4  current_sim_hand_trial: \cb1 \
\cb3                     temp_hand_after_discard_sim = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  current_sim_hand_trial \cf2 \strokec2 if\cf0 \strokec4  c != card_to_try_discarding_sim] \cb1 \
\cb3                     \cf2 \strokec2 if\cf0 \strokec4  trial_deck_sim: \cf5 \strokec5 # Check if there's a card to draw\cf0 \cb1 \strokec4 \
\cb3                         potential_redraw_card_sim = trial_deck_sim[\cf6 \strokec6 0\cf0 \strokec4 ]  \cb1 \
\cb3                         hypothetical_hand_for_ev_sim = temp_hand_after_discard_sim + [potential_redraw_card_sim] \cb1 \
\cb3                         ev_hypothetical_sim = calculate_hand_ev_for_round(hypothetical_hand_for_ev_sim, r_val_sim, prob_events_data_sim, \cf2 \strokec2 None\cf0 \strokec4 ) \cb1 \
\cb3                         \cf2 \strokec2 if\cf0 \strokec4  ev_hypothetical_sim > best_ev_after_discard_sim: best_ev_after_discard_sim, card_to_discard_for_sim_trial = ev_hypothetical_sim, card_to_try_discarding_sim\cb1 \
\cb3                 \cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  card_to_discard_for_sim_trial \cf2 \strokec2 and\cf0 \strokec4  trial_deck_sim: \cf5 \strokec5 # If beneficial and possible, execute discard\cf0 \cb1 \strokec4 \
\cb3                     final_hand_for_scoring_this_round_sim = [c \cf2 \strokec2 for\cf0 \strokec4  c \cf2 \strokec2 in\cf0 \strokec4  current_sim_hand_trial \cf2 \strokec2 if\cf0 \strokec4  c != card_to_discard_for_sim_trial]\cb1 \
\cb3                     final_hand_for_scoring_this_round_sim.append(trial_deck_sim.pop(\cf6 \strokec6 0\cf0 \strokec4 ))\cb1 \
\cb3             \cb1 \
\cb3             \cf5 \strokec5 # Scoring phase for this simulated round\cf0 \cb1 \strokec4 \
\cb3             round_score_for_trial_sim_this_round_raw = \cf6 \strokec6 0.0\cf0 \strokec4  \cb1 \
\cb3             \cf2 \strokec2 for\cf0 \strokec4  card_name_in_scoring_hand_sim \cf2 \strokec2 in\cf0 \strokec4  final_hand_for_scoring_this_round_sim: \cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  card_name_in_scoring_hand_sim \cf2 \strokec2 in\cf0 \strokec4  prob_events_data_sim:\cb1 \
\cb3                     \cf2 \strokec2 for\cf0 \strokec4  pts, prs_list \cf2 \strokec2 in\cf0 \strokec4  prob_events_data_sim[card_name_in_scoring_hand_sim]:\cb1 \
\cb3                         \cf2 \strokec2 if\cf0 \strokec4  \cf6 \strokec6 0\cf0 \strokec4  <= r_val_sim < \cf2 \strokec2 len\cf0 \strokec4 (prs_list) \cf2 \strokec2 and\cf0 \strokec4  random.random() < prs_list[r_val_sim] / \cf6 \strokec6 100.0\cf0 \strokec4 : \cb1 \
\cb3                             round_score_for_trial_sim_this_round_raw += pts\cb1 \
\cb3             \cb1 \
\cb3             \cf5 \strokec5 # Determine how much of this round's score can be added without exceeding the MAX_SECONDARY_SCORE\cf0 \cb1 \strokec4 \
\cb3             remaining_cap_space_for_trial = MAX_SECONDARY_SCORE - (current_user_sec_score + trial_future_secondary_vp)\cb1 \
\cb3             score_to_add_this_round = \cf2 \strokec2 min\cf0 \strokec4 (round_score_for_trial_sim_this_round_raw, remaining_cap_space_for_trial)\cb1 \
\cb3             \cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  score_to_add_this_round > \cf6 \strokec6 0\cf0 \strokec4 :\cb1 \
\cb3                 trial_future_secondary_vp += score_to_add_this_round\cb1 \
\cb3                 \cf5 \strokec5 # Accumulate for per-round average display (this is the capped amount for this round in this trial)\cf0 \cb1 \strokec4 \
\cb3                 round_total_vps_sim[r_val_sim] += score_to_add_this_round \cb1 \
\
\cb3         total_future_vp_across_trials += trial_future_secondary_vp \cf5 \strokec5 # Add this trial's total (already capped) future VP\cf0 \cb1 \strokec4 \
\
\
\cb3     avg_total_future_vp = total_future_vp_across_trials / num_trials \cf2 \strokec2 if\cf0 \strokec4  num_trials > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 else\cf0 \strokec4  \cf6 \strokec6 0.0\cf0 \cb1 \strokec4 \
\cb3     \cf5 \strokec5 # For per-round display, this average is based on potentially capped scores within each trial for that round\cf0 \cb1 \strokec4 \
\cb3     avg_vps_per_round_display = \{r_avg: total_vp / num_trials \cf2 \strokec2 if\cf0 \strokec4  num_trials > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 else\cf0 \strokec4  \cf6 \strokec6 0.0\cf0 \strokec4  \cf2 \strokec2 for\cf0 \strokec4  r_avg, total_vp \cf2 \strokec2 in\cf0 \strokec4  round_total_vps_sim.items()\} \cb1 \
\cb3     \cb1 \
\cb3     \cf2 \strokec2 return\cf0 \strokec4  avg_total_future_vp, avg_vps_per_round_display\cb1 \
\
\cb3 st.sidebar.header(\cf7 \strokec7 "Your Future Rounds Simulation"\cf0 \strokec4 ) \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 if\cf0 \strokec4  cur_round < MAX_ROUNDS - \cf6 \strokec6 1\cf0 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     n_trials_sim_widget = st.sidebar.number_input(\cf7 \strokec7 "Number of Trials "\cf0 \strokec4 , min_value=\cf6 \strokec6 100\cf0 \strokec4 , max_value=\cf6 \strokec6 100000\cf0 \strokec4 , value=\cf6 \strokec6 5000\cf0 \strokec4 , step=\cf6 \strokec6 100\cf0 \strokec4 , key=\cf7 \strokec7 "n_trials_sim_main"\cf0 \strokec4 ) \cb1 \
\cb3     allow_disc_sim_widget = st.sidebar.checkbox(\cf7 \strokec7 "Allow Discard/Redraw in Sim Rounds "\cf0 \strokec4 , \cf2 \strokec2 True\cf0 \strokec4 , key=\cf7 \strokec7 "allow_disc_sim_main"\cf0 \strokec4 ) \cb1 \
\cb3     \cb1 \
\cb3     run_simulation_button = st.sidebar.button(\cf7 \strokec7 "Run Your Future Rounds Simulation \uc0\u9654 \u65039  "\cf0 \strokec4 , key=\cf7 \strokec7 "run_sim_button_main"\cf0 \strokec4 )\cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  run_simulation_button: \cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  AVAILABLE_DRAW_POOL \cf2 \strokec2 or\cf0 \strokec4  \cf2 \strokec2 len\cf0 \strokec4 (AVAILABLE_DRAW_POOL) < \cf6 \strokec6 1\cf0 \strokec4  : \cb1 \
\cb3              st.sidebar.warning(\cf7 \strokec7 "Not enough cards in Your Available Draw Pool for a typical simulation."\cf0 \strokec4 )\cb1 \
\cb3              st.session_state.total_sim_future_vp = \cf6 \strokec6 0.0\cf0 \strokec4  \cb1 \
\cb3         \cf2 \strokec2 else\cf0 \strokec4 :\cb1 \
\cb3             \cf2 \strokec2 with\cf0 \strokec4  st.spinner(\cf7 \strokec7 f"Simulating \cf0 \strokec4 \{n_trials_sim_widget\}\cf7 \strokec7  trials for your future rounds..."\cf0 \strokec4 ):\cb1 \
\cb3                 avg_total_future_vp_result, avg_vps_per_round_display_result = simulate_future(\cb1 \
\cb3                     \cf2 \strokec2 list\cf0 \strokec4 (AVAILABLE_DRAW_POOL), \cb1 \
\cb3                     cur_round, \cb1 \
\cb3                     allow_disc_sim_widget, \cb1 \
\cb3                     n_trials_sim_widget, \cb1 \
\cb3                     st.session_state.PROB_EVENTS,\cb1 \
\cb3                     sec_total \cf5 \strokec5 # Pass current user's *already scored and capped* secondary total\cf0 \cb1 \strokec4 \
\cb3                 )\cb1 \
\cb3             \cb1 \
\cb3             st.session_state.total_sim_future_vp = avg_total_future_vp_result\cb1 \
\
\cb3             \cf2 \strokec2 if\cf0 \strokec4  avg_vps_per_round_display_result:\cb1 \
\cb3                 df_res_list = [\{\cf7 \strokec7 "Sim. Round"\cf0 \strokec4 : r_num_res + \cf6 \strokec6 1\cf0 \strokec4 , \cf7 \strokec7 "Avg Future VP"\cf0 \strokec4 : \cf2 \strokec2 round\cf0 \strokec4 (vp_val_res, \cf6 \strokec6 2\cf0 \strokec4 )\} \cb1 \
\cb3                                \cf2 \strokec2 for\cf0 \strokec4  r_num_res, vp_val_res \cf2 \strokec2 in\cf0 \strokec4  avg_vps_per_round_display_result.items() \cb1 \
\cb3                                \cf2 \strokec2 if\cf0 \strokec4  vp_val_res > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 or\cf0 \strokec4  r_num_res >= cur_round +\cf6 \strokec6 1\cf0 \strokec4 ] \cf5 \strokec5 # Show round if it's a future round, even if 0 VP\cf0 \cb1 \strokec4 \
\cb3                 \cb1 \
\cb3                 \cf2 \strokec2 if\cf0 \strokec4  df_res_list: \cb1 \
\cb3                     st.sidebar.subheader(\cf7 \strokec7 "Your Simulation Results (Avg VP Per Round - Display Only)"\cf0 \strokec4 )\cb1 \
\cb3                     st.sidebar.table(pd.DataFrame(df_res_list))\cb1 \
\cb3                 \cf2 \strokec2 else\cf0 \strokec4 : \cb1 \
\cb3                     st.sidebar.info(\cf7 \strokec7 "Your simulation ran but produced no VPs for future rounds (display)."\cf0 \strokec4 )\cb1 \
\cb3             \cf2 \strokec2 else\cf0 \strokec4 : \cb1 \
\cb3                 st.sidebar.info(\cf7 \strokec7 "Your simulation did not return per-round results for display."\cf0 \strokec4 )\cb1 \
\cb3         st.rerun() \cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 else\cf0 \strokec4 :\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     st.sidebar.info(\cf7 \strokec7 "Your simulation available only before the last round."\cf0 \strokec4 )\cb1 \
\
\pard\pardeftab720\partightenfactor0
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # Edit Opponent's Probabilities \cf0 \cb1 \strokec4 \
\cf5 \cb3 \strokec5 # \uc0\u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \cf0 \cb1 \strokec4 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3 st.divider()\cb1 \
\pard\pardeftab720\partightenfactor0
\cf2 \cb3 \strokec2 with\cf0 \strokec4  st.expander(\cf7 \strokec7 "Edit Opponent's Mission Probabilities (Baseline)"\cf0 \strokec4 , expanded=\cf2 \strokec2 False\cf0 \strokec4 ):\cb1 \
\pard\pardeftab720\partightenfactor0
\cf0 \cb3     updated_opponent_probs_edit = copy.deepcopy(st.session_state.OPPONENT_PROB_EVENTS)\cb1 \
\cb3     \cb1 \
\cb3     cur_round_for_opp_edit_display = cur_round \cf5 \strokec5 # Use the globally calculated cur_round\cf0 \cb1 \strokec4 \
\
\cb3     editable_opponent_cards = \{\cb1 \
\cb3         card_name: events \cf2 \strokec2 for\cf0 \strokec4  card_name, events \cf2 \strokec2 in\cf0 \strokec4  st.session_state.OPPONENT_PROB_EVENTS.items()\cb1 \
\cb3         \cf2 \strokec2 if\cf0 \strokec4  card_name \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.opponent_scoreboard_used_cards \cf2 \strokec2 and\cf0 \strokec4  \\\cb1 \
\cb3            card_name \cf2 \strokec2 not\cf0 \strokec4  \cf2 \strokec2 in\cf0 \strokec4  st.session_state.opponent_manually_removed_cards\cb1 \
\cb3     \}\cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  \cf2 \strokec2 not\cf0 \strokec4  editable_opponent_cards:\cb1 \
\cb3         st.info(\cf7 \strokec7 "All cards appear to have been used by the opponent or manually removed from their pool. No probabilities to edit for their deck."\cf0 \strokec4 )\cb1 \
\
\cb3     \cf2 \strokec2 for\cf0 \strokec4  card_opp, evs_opp \cf2 \strokec2 in\cf0 \strokec4  editable_opponent_cards.items(): \cb1 \
\cb3         st.markdown(\cf7 \strokec7 f"**\cf0 \strokec4 \{card_opp\}\cf7 \strokec7  (Opponent)**"\cf0 \strokec4 ); new_evs_for_card_opp = []\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  event_idx_opp, (pts_opp, prs_list_opp) \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 enumerate\cf0 \strokec4 (evs_opp, start=\cf6 \strokec6 1\cf0 \strokec4 ):\cb1 \
\cb3             num_future_rounds_opp = MAX_ROUNDS - cur_round_for_opp_edit_display\cb1 \
\cb3             num_cols_to_create_opp = \cf6 \strokec6 1\cf0 \strokec4  + num_future_rounds_opp \cf2 \strokec2 if\cf0 \strokec4  num_future_rounds_opp > \cf6 \strokec6 0\cf0 \strokec4  \cf2 \strokec2 else\cf0 \strokec4  \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3             \cb1 \
\cb3             cols_opp = st.columns(num_cols_to_create_opp)\cb1 \
\cb3             cols_opp[\cf6 \strokec6 0\cf0 \strokec4 ].markdown(\cf7 \strokec7 f"*VP: \cf0 \strokec4 \{pts_opp\}\cf7 \strokec7 *"\cf0 \strokec4 )\cb1 \
\cb3             new_prs_for_event_opp = \cf2 \strokec2 list\cf0 \strokec4 (prs_list_opp) \cb1 \
\
\cb3             \cf2 \strokec2 if\cf0 \strokec4  num_future_rounds_opp > \cf6 \strokec6 0\cf0 \strokec4 :\cb1 \
\cb3                 col_idx_offset_opp = \cf6 \strokec6 1\cf0 \strokec4  \cb1 \
\cb3                 \cf2 \strokec2 for\cf0 \strokec4  r_game_round_0_indexed_opp \cf2 \strokec2 in\cf0 \strokec4  \cf2 \strokec2 range\cf0 \strokec4 (cur_round_for_opp_edit_display, MAX_ROUNDS):\cb1 \
\cb3                     r_game_round_1_indexed_opp = r_game_round_0_indexed_opp + \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3                     \cb1 \
\cb3                     prob_val_opp = prs_list_opp[r_game_round_0_indexed_opp]\cb1 \
\cb3                     key_opp = \cf7 \strokec7 f"edit_opp_\cf0 \strokec4 \{card_opp\}\cf7 \strokec7 _E\cf0 \strokec4 \{event_idx_opp\}\cf7 \strokec7 _r\cf0 \strokec4 \{r_game_round_1_indexed_opp\}\cf7 \strokec7 "\cf0 \cb1 \strokec4 \
\cb3                     default_cat_str_opp = find_closest_category(prob_val_opp, CATEGORIES, PCT_MAP)\cb1 \
\cb3                     \cb1 \
\cb3                     choice_opp = cols_opp[col_idx_offset_opp].selectbox(\cb1 \
\cb3                         \cf7 \strokec7 f"R\cf0 \strokec4 \{r_game_round_1_indexed_opp\}\cf7 \strokec7 "\cf0 \strokec4 , \cb1 \
\cb3                         CATEGORIES, \cb1 \
\cb3                         index=CATEGORIES.index(default_cat_str_opp), \cb1 \
\cb3                         key=key_opp, \cb1 \
\cb3                         label_visibility=\cf7 \strokec7 "visible"\cf0 \strokec4  \cb1 \
\cb3                     )\cb1 \
\cb3                     new_prs_for_event_opp[r_game_round_0_indexed_opp] = PCT_MAP.get(choice_opp, \cf6 \strokec6 10\cf0 \strokec4 ) \cb1 \
\cb3                     col_idx_offset_opp += \cf6 \strokec6 1\cf0 \cb1 \strokec4 \
\cb3             \cb1 \
\cb3             new_evs_for_card_opp.append((pts_opp, new_prs_for_event_opp))\cb1 \
\cb3         updated_opponent_probs_edit[card_opp] = new_evs_for_card_opp \cb1 \
\cb3         \cb1 \
\cb3     \cf2 \strokec2 if\cf0 \strokec4  st.button(\cf7 \strokec7 "Apply Opponent's Baseline Probability Changes"\cf0 \strokec4 ):\cb1 \
\cb3         \cf2 \strokec2 for\cf0 \strokec4  card_key_opp \cf2 \strokec2 in\cf0 \strokec4  editable_opponent_cards.keys():\cb1 \
\cb3             \cf2 \strokec2 if\cf0 \strokec4  card_key_opp \cf2 \strokec2 in\cf0 \strokec4  updated_opponent_probs_edit:\cb1 \
\cb3                 st.session_state.OPPONENT_PROB_EVENTS[card_key_opp] = updated_opponent_probs_edit[card_key_opp]\cb1 \
\cb3         \cb1 \
\cb3         st.success(\cf7 \strokec7 "Opponent's Baseline Probabilities updated for available cards!"\cf0 \strokec4 )\cb1 \
\cb3         st.session_state.opponent_total_sim_future_vp = calculate_opponent_future_secondary_vp(\cb1 \
\cb3             cur_round, \cb1 \
\cb3             st.session_state.opponent_scoreboard_used_cards, \cb1 \
\cb3             st.session_state.opponent_manually_removed_cards,\cb1 \
\cb3             st.session_state.OPPONENT_PROB_EVENTS, \cb1 \
\cb3             opp_sec_total\cb1 \
\cb3         )\cb1 \
\cb3         \cf5 \strokec5 # No explicit st.rerun() here\cf0 \cb1 \strokec4 \
\
\
}