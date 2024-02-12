# UNO Game

This is a basic python implementation of UNO.

## Non-AI
If you want to play the game against a bot that randomly selects cards, grab the game on the no_AI branch.
- Install the requirements
```
pip install -r requirements.txt
```
- Play the game by running:
```
py uno.py
```
- It will ask you for the number of players (including yourself), and then the number of bots. Examples:
If you want to see bots playing, type 2 for each input. If you want to play against a bot, type 2 for players and 1 for bot (see image below).

![Alt text](image.png)

## Reinforcement Learning
The main branch has the game with an AI agent playing.
- Install the requirements
```
pip install -r requirements.txt
```
To train the agent, just run:
```
py agent.py
```
- It will run 1 million games and save the data on the train_data folder and model folder
- If you want to play less games, just change the number on line 116 of the agent.py. If left blank, the default is 1,000 games.
```
    # play 1 million games
    agent = Agent(1000000)
    
    # play 10 thousand games
    agent = Agent(10000)
    
    # play 1 thousand games
    agent = Agent()
    
    # play 1 game
    agent = Agent(1)
```