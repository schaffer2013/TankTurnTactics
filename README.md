# TankTurnTactics

This project is to simulate [Tank Turn Tactics](https://youtu.be/aOYbR-Q_4Hs), a game which uses turn-based tanks to defeat all others. It exists on a grid, and each tank takes turns to do actions. 

## General description
Each tank has a *range*, *extra lives*, and *action points* it can use. During each turn, the active tank first gains one action point, then it can use any or all of its action points with the following actions:
- Move to an open spot (in a cardinal direction)
- Shoot a tank within range (as "box distance", shown in gray)
- Donate the current action point to a tank in range
- Increase shooting range by 1
- Pass (do nothing, but maintain your current action point)
- Wither (do nother, but lose current action point. This is generally bad)

##
<img width="55" alt="image" src="https://user-images.githubusercontent.com/9828010/236706502-01b3ef53-339e-49c5-a30d-2556a4e03696.png">
Each "tank" is represented with a rectange

![tankturns_nn](https://user-images.githubusercontent.com/9828010/236706222-56200bc2-b24b-47f7-9916-1cc8327d634e.gif)
