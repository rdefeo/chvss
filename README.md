# chvss
Super simple 5x5 python chess game. The home rank will be randomized for each player. Requires a color terminal. 

To move, specify the file and rank for both the starting and ending positions. Therefore, to move the C file pawn, you would enter "c2 c3".

```
$ ./chvss.py
5 R Q K N B
4 P P P P P
3 . . . . .
2 P P P P P
1 Q R N K B
  a b c d e
Move? c2 c3
5 R Q K N B
4 P P P P P
3 . . P . .
2 P P . P P
1 Q R N K B
  a b c d e
Capturing P!!
5 R Q K N B
4 P . P P P
3 . . P . .
2 P P . P P
1 Q R N K B
  a b c d e
```

TODO:
1. Improve move input format to allow: "pc2" for "Pawn to C2"
2. Improve computer move scoring
