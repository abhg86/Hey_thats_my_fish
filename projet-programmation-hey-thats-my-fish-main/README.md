# Prprog - Hey, That's My Fish!

Project made by Thibault Chanus, Aymeric Behaegel, Léo Laffeach et Hugo Boulier.

> This project is about programming using python. 
> For that we redo the game "Hey, That's My Fish!".

## The Game
> The board is a map using hexagonal tiles, each tile has a number of fish on it.
> Each player has the same number of penguin. 
> When a penguin move of a tile, the tile is removed and the player gain the score of the tile.
> The game end when no one can make a move.

### Rules
- Turn by turn, each player put a penguin on a 1 point tile.
- When all player have placed their penguins, the game start.
- Turn by turn, each player will choose one of their own penguin and move it.
- A move is a direction and a distance from the penguin.
- A move is valid as long as their is no obstacle (otheir penguin, a hole) between the starting and the ending tiles.
- The winner is the player that has the higher score at the end.
- The score of a player is the sum of the score of the tile that he collected.

## How to play
To play, you have to create an instance of Game.
You can give it a list of Player instance as player parameter and a number of penguins per player.
If you want to visualize the game, you have to give to the Game an instance of GraphicsPygame.
```py
    # A game between a human and a random player with 2 penguin for each player, showed with pygame.
    game = Game(players=[HumanPlayer(1), RandomPlayer(2)], 
                nbPenguinsPerPlayer = 2,
                affichage = GraphicsPygame)
    finalScore = game.play()
```

## Implementation

### Files
> ├── README.md \
> ├── game.py \
> ├── gameParameters.py \
> ├── world.py \
> ├── mapMaker.py \
> ├── playerImport.py \
> ├── playerDummy.py \
> ├── Players \
> │   ├── playerFunctions.py \
> │   ├── humanPlayer.py \
> │   ├── randomPlayer.py \
> │   ├── greedyPlayer.py \
> │   ├── selflessPlayer.py \
> │   ├── harePlayer.py \
> │   ├── snailPlayer.py \
> │   ├── chaserPlayer.py \
> │   ├── runnerPlayer.py \
> │   └── connectPlayer.py \
> ├── graphicsDummy.py\
> ├── Graphics \
> │   └── graphicsPygame.py \
> └── .gitignore

### Players

- Human
    > Let a human player to select the penguin and the tiles.

- Random
    > Select randomly between all possible move.

- Greedy & Selfless
    > Greedy : Select randomly between higher score tiles. \
    > Selfless : Select randomly between lower score tiles.

- Hare & Snail
    > Hare : Select randomly between longest possible move. \
    > Snail : Select randomly between shortest possible move (one tile at a time).

- Chaser & Runner
    > Chaser : Select a possible move that reduce the distance with another penguin. \
    > Runner : Select a possible move that maximize the distance with other penguins.

- Connect
    > Choose in priority tiles that will keep the board connected. \
    > If the world will be deconnected, it will choose the connected compound with the higher score.



