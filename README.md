# TankTurnTactics

This project is to simulate [Tank Turn Tactics](https://youtu.be/aOYbR-Q_4Hs), a game which uses turn-based tanks to defeat all others. It exists on a grid, and each tank takes turns to do actions. 

### Need help starting it?
- Run from `main.py`
- Make sure `VISUAL` is set to `True`
- Make sure there is some reasonable `MOVE_DELAY` time (maybe 300 ms?)

## General description
Each tank has a *range*, *extra lives*, and *action points* it can use. During each turn, the active tank first gains one action point, then it can use any or all of its action points with the following actions:
- Move to an open spot (in a cardinal direction)
- Shoot a tank within range (as "box distance", shown in gray)
- Donate the current action point to a tank in range
- Increase shooting range by 1
- Pass (do nothing, but maintain your current action point)
- Wither (do nothing, but lose current action point. This is generally bad)

## Tank icon
<img width="55" alt="image" src="https://user-images.githubusercontent.com/9828010/236706502-01b3ef53-339e-49c5-a30d-2556a4e03696.png">
Each "tank" is represented with a rectangle. The important features are:

- Tank index (middle, bottom) to track each player
- Extra lives (bottom, corners). Each tank starts with 2 extra lives and loses one when it's shot.
- Range (top, right)
- Available action points (top, left)


## Gameplay
This currently auto-plays based on separate, but unlearning Neural Networks. Taken at [this commit](https://github.com/schaffer2013/TankTurnTactics/commit/5b010eb0f10aac5dfa515b281ae16cdbb280215a).
The output of the NN gives a list of weighted action choices, which gets randomly chosen based on weight (the "better" the option, the higher chance it has to get chosen). If weighted-random choice (WRC) is an illegal move (trying to move to an occupied spot, shooting a dead or out-of-range tank, etc), the agent is forced to choose "Wither" as a punishment. With this example, the "Wither percentage" over all actions chosen was over 72%. This key metric should quickly drop as closed-loop training happens.

![tankturns_nn](https://user-images.githubusercontent.com/9828010/236706222-56200bc2-b24b-47f7-9916-1cc8327d634e.gif)
