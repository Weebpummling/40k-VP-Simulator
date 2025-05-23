Warhammer 40k VP Simulator - User Manual

1. Introduction

Welcome to the Warhammer 40k VP Simulator! This application is designed to help you track your scores during a game of Warhammer 40,000 (10th Edition), analyze the Expected Value (EV) of your active secondary missions, get recommendations on discarding missions, and simulate potential future scores for both yourself and your opponent.

The tool allows you to:

Customize the probability of scoring for each secondary mission for both yourself and your opponent.

Track round-by-round scores (Primary, Secondary 1, Secondary 2, Used Cards) for both players.

Manage your and your opponent's available card pools (considering used and manually removed cards).

Get real-time EV for your active secondary missions, with options to temporarily override probabilities for the current round.

Receive discard recommendations based on EV.

Simulate your future secondary scores, respecting game VP caps.

Project your opponent's future secondary scores based on their probabilities and available cards, respecting game VP caps.

Compare current and projected final scores, with an option to include the standard 10 Starting VPs.

Define player order (Going First/Second) which influences current round calculation.

2. Sidebar - Settings & Management
The sidebar on the left is your control panel for global settings, data management, and simulations.

2.1. General Settings
Select Your Player Order:

Choose whether you are "Going First" or "Going Second."

This selection is crucial as it affects how the "Current Game Round (for active play)" is determined based on scoreboard entries.

Include Starting VP (10 VP) in Totals:

Check this box (default: checked) to include the standard 10 Starting VPs in the "Current Grand Total" and "Projected Game End Total VP" for both players.

2.2. Probability Profiles
This section allows you to manage the baseline probabilities of scoring for each secondary mission for your own deck.

Import settings CSV: Upload a CSV file with your custom probabilities.

Format: Card names in the first column (index). Subsequent columns for each event: E{event_number}_pts (e.g., E1_pts) and E{event_number}_r{round_number} (e.g., E1_r1, E1_r2, etc., for probability percentages).

Export Current Profile as CSV: Download your currently active set of mission probabilities.

2.3. Card Deck Management (Your Deck)
Manage your available card pool.

Your Scoreboard Used Cards: Automatically lists cards you've marked as "Used" on the main scoreboard.

Manually Remove Cards from Your Deck: Select cards here to remove them from your draw pool for any reason (e.g., auto-discarded by a game effect).

Your Available Draw Pool Size: Shows the count of cards remaining in your deck.

View Your Available Draw Pool: Expand to see the list of cards.

2.4. Card Deck Management (Opponent's Deck)
Manage your opponent's available card pool. This helps in making their future VP projection more accurate.

Opponent's Scoreboard Used Cards: Automatically lists cards you've marked as "Used" for the opponent on the main scoreboard.

Manually Remove Cards from Opponent's Deck: Select cards here to remove them from the opponent's potential draw pool.

Opponent's Available Draw Pool Size: Shows the count of cards remaining in their deck.

View Opponent's Available Draw Pool: Expand to see the list of cards.

2.5. Your Future Rounds Simulation
Simulate your potential secondary scores for the remaining rounds.

Number of Trials: Set the number of simulation iterations (higher is more accurate but slower).

Allow Discard/Redraw in Sim Rounds: If checked, the simulation will attempt an optimal discard/redraw strategy for you in each simulated future round.

Run Your Future Rounds Simulation ▶️: Starts the simulation. Results are displayed in the sidebar and update the "VP Summary & Projections."

3. Main Interface - Data Entry & Analysis
3.1. Edit Mission Probabilities (Baseline)
This expandable section allows you to set your baseline probability of scoring for each event of every secondary mission, for each round.

Filtering: Only cards not yet used on the scoreboard or manually removed from your deck will be shown here for editing.

Editing:

For each available mission and its scoring events (e.g., "Assassination - Event 1 - 5 VP"):

You can select a probability category (100%, 80%, 50%, 30%, <10%) for each round that is considered current or future (based on the "Current Game Round").

Probabilities for past rounds are not displayed for editing.

Click "Apply Baseline Probability Changes" to save your modifications. These are your default probabilities.

3.2. Live Scoreboard & Current Round
Record game progress for both players.

For each of the 5 rounds:

Your Scores: Input VPs for "Secondary 1," "Secondary 2," and "Primary." Use the multiselect for "Your Cards Used" to mark secondaries scored/revealed.

Opponent's Scores: Input VPs for the opponent's "Secondary 1," "Secondary 2," and "Primary." Use the multiselect for "Opponent's Cards Used."

Current Game Round (for active play): This is a crucial display. It's calculated based on the scoreboard entries and your selected "Player Order":

Going First: The round advances to the next battle round only after both you and your opponent have made entries (secondary VPs or used cards) for the current battle round.

Going Second: The round advances to the next battle round after you have made entries for the current battle round.
This cur_round (0-indexed internally) determines the context for active mission EV and probability editing.

3.3. Your Active Missions & EV for Round {current round}
Analyze your currently drawn secondary missions for the active game round.

Select up to 2 active missions...: Choose the missions you are currently holding from your AVAILABLE_DRAW_POOL.

Adjust Probabilities & See EV for Your Hand...:

For each selected active mission:

You can temporarily override the baseline probability for this current round only by selecting a different probability category. This is for quick adjustments to in-game situations.

Discard Recommendation:

Calculates the Expected Value (EV) of your current active hand for the current round, using any temporary probability adjustments.

Evaluates the average EV if you were to discard each card in your hand and draw a random replacement from your AVAILABLE_DRAW_POOL.

Provides a recommendation to "Discard" or "Keep current hand."

3.4. View Your Available Draw Pool (Main UI)
An expandable section below "Active Missions" showing cards still in your deck.

4. VP Summary & Projections
This section consolidates key VP information. All scores here respect the game caps (Primary: 50 VP, Secondary: 40 VP).

4.1. Your Score
Your Scored Secondary VP: Total secondary VPs you've entered (max 40).

Your Entered Primary VP: Total primary VPs you've entered (max 50).

Your Current Grand Total: Sum of scored VPs, plus Starting VP if enabled.

EV of Your Active Hand (R{current round}): EV of your current active missions for this round.

Your Simulated Future Secondary VP: Projected VPs from your secondaries in future rounds from the last simulation. This value, when added to your already scored secondary VPs, will not exceed 40.

Your Projected Game End Total VP: Your current grand total + simulated future secondary VPs.

4.2. Opponent's Score
Opponent's Current Grand Total: Sum of opponent's entered VPs (secondaries max 40, primaries max 50), plus Starting VP if enabled.

Opponent's Projected Game End Total VP: Opponent's current grand total + their projected future secondary VPs. The future projection assumes optimal play based on their available cards and defined probabilities, capped to ensure their total secondaries do not exceed 40.

5. Advanced/Optional
5.1. Edit Opponent's Mission Probabilities (Baseline)
Located towards the bottom of the main page (minimized by default).

Allows you to set baseline probabilities for each of the opponent's secondary missions.

Filtering: Only cards not yet used by the opponent on the scoreboard or manually removed from their deck will be shown for editing.

Editing: Works like your probability editor; probabilities for past rounds (based on your current game round) are not editable.

The probabilities set here are used for "Opponent's Projected Future Secondary VP." If not edited, DEFAULT_PROBS are used for the opponent.

Click "Apply Opponent's Baseline Probability Changes" to save.

6. Tips for Use
Set Player Order First: This is crucial for accurate cur_round calculation.

Maintain Scoreboard: Regularly update both your and your opponent's scores and used cards.

Customize Probabilities:

Use "Edit Mission Probabilities (Baseline)" for your general expectations.

Use the temporary overrides in the "Active Missions" section for in-the-moment adjustments.

Consider editing opponent probabilities if you have insights into their playstyle or likely card choices.

Manage Card Pools: Use the "Manually Remove Cards" features in the sidebar if cards are removed from play outside of normal scoring (e.g., effects that discard from the deck).

Simulate Strategically: Run "Your Future Rounds Simulation" when you have key decisions to make or want to understand your scoring potential.

Understand Projections: Projections are estimates based on defined probabilities. Your "Simulated Future Secondary VP" uses your customized probabilities and simulation settings. The "Opponent's Projected Future Secondary VP" assumes they make optimal choices based on their defined probabilities (or defaults if you haven't edited them).

Good luck with your games!
