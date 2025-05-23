Warhammer 40k VP Simulator - User Manual
1. Introduction
Welcome to the Warhammer 40k VP Simulator! This application is designed to help you track your scores during a game of Warhammer 40,000 (10th Edition), analyze the Expected Value (EV) of your active secondary missions, get recommendations on discarding missions, and simulate potential future scores for both yourself and your opponent.

The tool allows you to:

Customize the probability of scoring for each secondary mission.

Track round-by-round scores for yourself and your opponent.

Manage your available card pool.

Get real-time EV for your active secondary missions.

Receive discard recommendations based on EV.

Simulate your future secondary scores.

Project your opponent's future secondary scores.

Compare projected final scores.

2. Sidebar - Settings & Management
The sidebar on the left contains global settings, data import/export, and management tools for your card deck.

2.1. General Settings
Include Starting VP (10 VP) in Totals: Check this box if you want the standard 10 Starting Victory Points (often for having a painted army or other pre-game conditions) to be included in the "Current Grand Total" and "Projected Game End Total VP" for both players. This is checked by default.

2.2. Probability Profiles
This section allows you to manage the baseline probabilities of scoring for each secondary mission.

Import settings CSV: You can upload a CSV file containing your custom probabilities for all missions. This is useful for saving and loading different probability sets (e.g., for different armies or playstyles).

The CSV should have card names as the index (first column).

Columns should follow the format E{event_number}_pts for victory points of an event and E{event_number}_r{round_number} for the probability percentage in that round (e.g., E1_pts, E1_r1, E1_r2, ..., E2_pts, E2_r1, etc.).

Export Current Profile as CSV: Download the currently active set of mission probabilities (either the defaults or your edited/imported set) as a CSV file.

2.3. Card Deck Management (Your Deck)
This section helps you manage the pool of cards available for you to draw from.

Your Scoreboard Used Cards: Displays a list of cards you have already marked as "Used" in the main scoreboard. These are automatically removed from your draw pool.

Manually Remove Cards from Your Deck: Use this multiselect to remove cards from your available draw pool for reasons other than being scored (e.g., a card was auto-discarded due to a game rule, or you know you won't pick it).

Your Available Draw Pool Size: Shows how many cards are currently in your draw pool.

View Your Available Draw Pool: Expand this to see a list of all cards currently available for you to draw.

2.4. Your Future Rounds Simulation
This section, also in the sidebar, is used to simulate your potential secondary scores for the remaining rounds of the game.

Number of Trials: Set how many times the simulation should run. More trials give more statistically stable results but take longer.

Allow Discard/Redraw in Sim Rounds: If checked, the simulation will attempt an optimal discard/redraw strategy for you in each simulated future round.

Run Your Future Rounds Simulation ▶️: Click this button to start the simulation. Results (average VP per future round and total average future VP) will be displayed in the sidebar and used in the "VP Summary & Projections" section.

3. Main Interface - Data Entry & Analysis
The main area of the application is where you'll input game data and see detailed analysis.

3.1. Edit Mission Probabilities (Baseline)
This expandable section allows you to set the baseline probability of scoring for each event of every secondary mission, for each round.

For each mission and each of its scoring events (e.g., "Assassination - Event 1 - 5 VP"):

You can select a probability category (100%, 80%, 50%, 30%, <10%) for each round that has not yet been considered "past" based on the scoreboard.

Past rounds' probabilities are not editable here.

Click "Apply Baseline Probability Changes" to save your modifications. These probabilities are used for EV calculations and simulations unless temporarily overridden.

3.2. Live Scoreboard & Current Round
This is where you record the game's progress round by round for both yourself and your opponent.

For each of the 5 rounds:

Your Scores:

Input VPs for "Secondary 1," "Secondary 2," and "Primary."

Use the multiselect for "Your Cards Used" to indicate which secondary missions you scored or revealed in that round. Cards selected here are removed from your available draw pool.

Opponent's Scores:

Input VPs for the opponent's "Secondary 1," "Secondary 2," and "Primary."

Use the multiselect for "Opponent's Cards Used" to indicate which secondary missions they scored or revealed. These are used for projecting their future score.

Current Game Round (for active play): This indicates the current round for your active play, based on your scoreboard entries for secondaries. This determines which round's probabilities are used for your active mission EV calculations.

3.3. Your Active Missions & EV for Round {current round}
This crucial section helps you analyze your currently drawn secondary missions.

Select up to 2 active missions...: Choose the secondary missions you are currently holding or considering for the current round from your available draw pool.

Adjust Probabilities & See EV for Your Hand...:

For each selected active mission and each of its scoring events:

You can temporarily override the baseline probability for this current round only by selecting a different probability category from the dropdown. This allows you to quickly adjust for specific game situations without changing your baseline probabilities.

The discard recommendation logic below will use these adjusted probabilities.

Discard Recommendation:

The app calculates the Expected Value (EV) of your current active hand for the current round using any temporary probability adjustments you've made.

It then evaluates, for each card in your hand, what the average EV would be if you discarded that card and drew a random replacement from your available draw pool.

A recommendation to "Discard" or "Keep current hand" is provided based on whether any discard option offers a significant EV improvement.

3.4. View Your Available Draw Pool (Main UI)
This expandable section, located below the "Active Missions" area, provides another quick view of the cards remaining in your draw pool.

4. VP Summary & Projections
This section, found below the active missions, consolidates all key Victory Point information.

4.1. Your Score
Your Scored Secondary VP: Total secondary VPs you've entered on the scoreboard (capped at 40).

Your Entered Primary VP: Total primary VPs you've entered (capped at 50).

Your Current Grand Total: Sum of your scored secondary, primary, and (if selected in sidebar) starting VPs.

EV of Your Active Hand (R{current round}): The Expected Value of the missions you currently have selected as active for the current round, using any temporary probability adjustments.

Your Simulated Future Secondary VP: The average total VPs you are projected to score from secondaries in all future rounds, based on the last simulation you ran. This is also capped to ensure your total secondary score doesn't exceed 40.

Your Projected Game End Total VP: Your current grand total plus your simulated future secondary VPs.

4.2. Opponent's Score
Opponent's Current Grand Total: Sum of the opponent's entered secondary, primary, and (if you selected it for totals) starting VPs. Secondary VPs are capped at 40, Primary at 50.

Opponent's Projected Game End Total VP: The opponent's current grand total plus their projected future secondary VPs. Their future secondaries are projected based on them optimally choosing from available cards using their defined probabilities (or defaults), also capped at 40 total secondary VPs.

5. Advanced/Optional
5.1. Edit Opponent's Mission Probabilities (Baseline)
Located towards the bottom of the main page (minimized by default), this expandable section allows you to:

Set the baseline probability of scoring for each event of every secondary mission for your opponent.

This works identically to your own probability editor.

The probabilities set here are used when calculating the "Opponent's Projected Future Secondary VP." If you don't edit these, the opponent's projections will use the DEFAULT_PROBS.

Click "Apply Opponent's Baseline Probability Changes" to save.

6. Tips for Use
Update Probabilities Regularly: Your baseline probabilities are key. Adjust them based on your army, playstyle, and common matchups for more accurate EV calculations.

Use Temporary Overrides: For specific in-game situations (e.g., you're in a perfect position to score a normally difficult mission), use the temporary probability adjustments in the "Active Missions" section.

Scoreboard Accuracy: Keep the scoreboard updated with both your and your opponent's scores and used cards. This directly impacts the "Current Game Round," available card pools, and projections.

Simulation for Planning: Run the "Future Rounds Simulation" at different stages of the game to get an idea of your potential scoring trajectory.

Understand Projections: Remember that all projections are based on the probabilities you've set (or defaults). The opponent's projection assumes they play optimally to maximize their EV based on their defined probabilities.

Good luck, and may your dice be ever in your favor!
