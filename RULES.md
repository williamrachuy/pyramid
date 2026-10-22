# Pyramid: the rules

This is the rulebook the engine (`web/engine.js`) implements. The author decides the rules. Where the author's description left a choice open, the choice made here is listed under **Interpretations** at the bottom so it can be confirmed or changed.

## The idea

Each player's court is one triangular face of a pyramid. A face has three corners: two on the ground and one at the top. Place the pyramid over the origin with the four ground corners on four rays (the table's diagonals) and the top on the vertical axis. Each face then has one vertex on each of two adjacent ground rays and one on the vertical axis. A vertex's distance from the origin is the value of the card that stands for it.

Neighbouring faces share a ground ray. When the cards for that shared corner match, the two faces' vertices fall on the same point and those faces meet. All four faces share the vertical axis; when all four top cards agree, the four apexes are one point. When every shared corner meets, the four triangles close over a four-sided base: a pyramid. Until then it is an unfolded net.

## Seats and courts

- Four seats: **South** (spades, the human), **East** (hearts), **North** (clubs), **West** (diamonds). Turn order: S, E, N, W.
- Each court has three **subjects** (Ace to 10) above three **royals** (Jack, Queen, King), each in positions **L, C, R** as the owner sees them. Royals are dealt the same way in every court: Jack left, King centre, Queen right.
- The 40 subjects are shuffled into a deck; each court is dealt three.

## The ten lanes (pivot nodes)

| Kind | Lanes | Subjects |
|---|---|---|
| Base corner (ground ray) | 4 | S.R–E.L, E.R–N.L, N.R–W.L, W.R–S.L |
| Ridge (adjacent apexes) | 4 | S.C–E.C, E.C–N.C, N.C–W.C, W.C–S.C |
| Peak (opposite apexes) | 2 | S.C–N.C, E.C–W.C |

The six ridge and peak lanes are every pair of centre cards, so all six pair exactly when the four apexes agree.

A lane is **paired** when its two subjects match in rank. Suit doesn't matter. **Aces are wild:** an ace pairs with anything. As a vertex, an ace takes the value of the card it is paired with; two aces paired make **1**. An unpaired ace is 1.

## Control

A lane is ruled by the royals under its two subjects: the left royal under the left subject, and so on. Whoever's royal trumps controls the lane.

- Different ranks: **K beats Q, Q beats J, J beats K.**
- Same rank: **spades beat hearts, hearts beat clubs, clubs beat diamonds, diamonds beat spades.**
- Same rank and same colour (spades/clubs, hearts/diamonds) is a **stalemate**: nobody controls the lane.

With the standard deal, each court controls its right corner, each centre King beats the next seat's by suit, and both peaks are stalemated (the King of spades against the King of clubs, and the King of hearts against the King of diamonds).

## A turn

Every action costs one gem. Each turn begins with **one free action**.

- **Swap two of your own subjects.** No lane needed.
- **Swap two of your own royals.** This changes who controls your lanes.
- **Swap across a lane you control.** The subjects at its two ends trade places.
- **Swap across a lane you are not part of** by paying its controller: the action's gem goes to them. A stalemated lane can't be swapped by anyone.
- **Draw** a card into your hand (hand limit 3).
- **Play** a card from your hand onto one of your subjects. The replaced subject goes to the bottom of the deck.
- **End your turn.**

## Gems

- When a lane becomes paired, a gem forms on it. A lane forms at most one gem per turn, so a pair can't be farmed by breaking and re-making it.
- A gem is collected automatically, at once, by whoever controls its lane. A gem on a stalemated lane waits until someone controls it, for example after a royal swap.
- A court whose three subjects are all its own suit (a flush) forms a gem at the court's centre, which goes to its owner.
- Pairs already on the table at the deal don't form gems.

## The end

When all ten lanes are paired, the pyramid is complete and the game ends immediately. Whoever made that final pair takes **the capstone: +5 gems**. Then **most gems wins**; ties are shared. A round clock (20, 30 or none) ends the game the same way if it runs out first, with no capstone.

The capstone exists to make closing worth racing for. Without it, ending the game only ever helps the leader, so players behind keep breaking pairs. In AI self-play (30 games per setting, Normal), no competitive game closed the pyramid without a capstone. With +5, about half of games closed, in about 14 rounds on average. +8 did no better than +5.

## Interpretations (for the author to confirm)

1. **The free gem is a free action, not banked score.** "Every turn a player gets a free gem, meaning a free action": if it were banked, passing every turn would be the safest way to win, since gems are the score. The engine has a switch (`freeGemBanks`) to bank it instead.
2. **Your own lane needs control; someone else's lane needs a toll.** On a lane you're part of but don't control, you can't swap. On a lane you aren't part of, you pay the controller one gem (this is the action's cost, not an extra). Stalemated lanes are frozen for everyone.
3. **Royal swaps are allowed** (as in the Python prototype). Without them control is fixed for the whole game, and a gem waiting on a stalemated lane could never be collected "later in the turn".
4. **The centre has six lanes**: ridges to both neighbours and a peak to the opposite court, as in the prototype.
5. **Hand cards are played by replacement** and the replaced card goes to the bottom of the deck, so the deck never runs out of meaning.
6. **One gem per lane per turn**, to stop pair-break-pair loops.
7. **A round clock** stays as a backstop for games that never close.
8. **The capstone (+5)** was the author's chosen fix for games that never closed (see The end).
