# COMP3220 Assignment-3

This is COMP3220 Assignment 3 for 620171757 and 620160983

PARTNER WITH ID 620160983 BUILT THE DEFENSIVE AGENT, WHILE PARTNER WITH ID 620171757 BUILT THE ATTACKING AGENT

PROGRAM FILES:
agents\attacking.py:    This is the file containing the attacking agent.
agents\base_agent.py:   This is the file containing the base_agent(gives what the Agent class should consist of)
agents\defensive.py:    Thss us the file containing the defensive agent
agents\reference.py:    This is the file containing the basic reference agent
gui.py:                 This is the file containing the code for the gui which illustrates the game running in real time
main.py:                This is the file that contains code for running the gui and building the two agents
matches.py:             This is the file that consists of  the code which executes 8 matches between the attacking and defensive agents
move_search.py:         This file contains all the functions relating to the searches which allow the AI agents to choose their best path based on the nodes discovered. It contains the minimax and alphabeta searches
pruning_compare.py:     This file was made to allow comparison between the alphabeta and minimax searches to show the result of pruning.
test_agent.py:          This file checks that an Agent can be built and choose a legal opening move
test_attacking.py:      This file checks that the attacking agent evaluation works
test_defensive.py:      This file checks that the defensive agent evaluation works 

HOW TO RUN:
1. Open a terminal in the folder which contains all the program files.
2. Run the program by using the command:
            python3 main.py
3. The gui has all the options to select what you wish for the program to do.

CONTROLS:
Only requires mouse for usage. All functionalities work by clicking on screen elements to produce necessary results.

TESTING THE TWO AGENTS AND THE BASE AGENT's ABILITY TO BE BUILT:
To test that each agent works run each command in the terminal consecutively:
            python3 test_agent.py
            python3 test_attacking.py
            python3 test_defensive.py
Each should give whether the agent passed (ran successfully) or failed (had an error in running).

TESTING AI VS AI WITHOUT GRAPHICS:
To test the 8 AI VS AI matches against other, run the following command in the terminal:
            python3 matches.py
This prints which agents plays which colour, the result of the match, whether checkmate or stalemate was reached, and the amount of plies the result was acheived in.

TESTING PRUNING:
To test the pruning of aplhabeta for each AI agent, run the command in the terminal:
            python3 pruning_compare.py
It shows the number of nodes explored by both minimax and alphabeta algorithms, and should show that the same score was acheived by both, even though alpha beta searched significantly less nodes.

AI DISCLOSURE:
Artificial Intelligence tools were used to assist in code planning as well as debugging and refining code.