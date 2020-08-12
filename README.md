# chvss
Super simple 5x5 python chess game. I played a version of this game years (decades?) ago on the Palm Pilot. Decided to try my hand at implementing it in python.

## Game features
* The home rank is randomized for each player
* Detects invalid moves (e.g. can't make a mvoe that places self in check)
* Primitive move scoring by computer player

## How to play
Specify the file and rank for both the starting and ending positions. Therefore, to move the C file pawn, you would enter "c2 c3".

![game screenshot](./chvss.png?raw=true)

## TODO:
1. Improve move input format to allow: "pc2" for "Pawn to C2"
2. Improve computer move scoring for better moves
3. Enable pawn promotions
