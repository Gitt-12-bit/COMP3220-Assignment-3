#ID NUMBERS: 620171757, 620160983
from agents.base_agent import Agent
from agents import attacking, defensive
import gui

#Builds the attacking and defensive agents and starts the GUI
def main():
    agents = {
        "Attacking": Agent("Attacking", attacking.evaluate),
        "Defensive": Agent("Defensive", defensive.evaluate)
    }

    gui.run(agents)

if __name__ == "__main__":
    main()