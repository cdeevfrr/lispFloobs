# The genetic algorithm described in Land Of Lisp

Population lives on a square grid that wraps in both directions.

Members of the population (Floobs) can move in 8 directions,
genotype is one number for each direction, max 1. 

Each timestep, 
- each floob picks a direction to move in with probability based on the values in their 8 directions. They may decide not to move.
- Each floob looses hunger, and dies if its too hungry
- If floobs have enough food, they use some food and make a new floob child at a random side. The childs genes are randomly perturbed from the parents.

Food is generated on the board every few timesteps.

Food is generated on the board with higher probability in certain areas the others (initially this is a square in the middle)

### Edge cases
- Only one food can exist at a spot at a time.
- If two floobs are at the same spot, that's fine - if there's food, one of them will get it and the other won't.



### Extensions
- Different lush zones (stripes? Diagonals? A circle?)
- Eyes (a genotype that makes movement a function of what a floob currently sees)
- Floob age (before birth and for death)
- Can only eat after moving rather than before&after



