from agents.base_agent import Agent
from agents import attacking, defensive
import gui

def main():
    agents = {
        "Attacking": Agent("Attacking", attacking.evaluate),
        "Defensive": Agent("Defensive", defensive.evaluate)
    }

    gui.run(agents)

if __name__ == "__main__":
    main()