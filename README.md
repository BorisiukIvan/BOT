# BOT
This is code of my engine & interface, but you can use your engine, if you want.
Note that this will work only on Lichess and Lichess clones. There's list of some Lichess clones, that support Bot:
1. https://lichess.org - Lichess, supports chess and some chess variants;
2. https://playstarategy.org - Lichess clone that supports much more variants;
3. https://lichess.dev - Empty Lichess preview website;
4. https://lidraughts.org* - Lichess for draughts;
5. https://lishogi.org* - Lichess for shogi;

*) This website does not support chess, so you need to use your own engine if you want your bot to play on this website too.

# About

This is version 2.9 (written on 29 December 2022). This bot can:
- See checkmate in 1 move;
- See checkmate in 2 or 3 moves, if opponent has only one legal move;
- See capture;
- See if opponent can checkmate in 1 move;
- See if opponent can capture piece;

This bot cannot:
- Move by pawn for 2nd to 4th file;
- Castle;
- See if opponent can promote his pawn to queen;
- See primite fork;

And this bot doesn't know any openings, so don't be shocked if he moves 1. Na3 or Nh3 :)
