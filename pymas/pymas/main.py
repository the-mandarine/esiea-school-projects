#!/usr/bin/env python
"""PyMAS is a multi-agent system scheduler fully modular.
It follows the BDI software model."""

from sys import version_info

# Check the used verson of python
if version_info[0] != 3:
    print("You need python3 to run pyMAS")
    exit(3)

from config import Settings
from agents import Agent

def main():
    """Runs everything needed by the agent"""
    settings = Settings()
    agent = Agent(settings)
    agent.start()

    # The agent is executing
    try:
        agent.join()
    except KeyboardInterrupt:
        agent.stop()
        

if __name__ == '__main__':
    main()

