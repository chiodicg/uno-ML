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
The main branch will have the game with an AI agent playing.
The implementation is ongoing.