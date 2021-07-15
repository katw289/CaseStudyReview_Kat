# Introduction

For this case study, I decided to take on problem #2, Barren Land Analysis. I decided to choose this problem as it is the most similar to problems I encounter in my current position.

When reading the components of the project, I immediately related the problem to a graph theory problem I had studied in discrete mathematics, which is counting the connected components of a graph. We can call each piece of land a vertex. Two vertices are adjacent (i.e. have an edge between them) if both vertices are fertile, and they are immediately next to each other in the land grid. (V(x,y) is adjacent to V(x-1, y), V(x+1,y), V(x,y-1), V(x,y+1)). If you have some vertex V, you can find all connected components by doing a depth first search, which is the skeleton of the algorithm I chose.  


## Method of Implementation
My immediate temptation was to do this problem recursively. However, the graph we have created is 240,000 vertices. For the largest recursive call, where there is no barren land, the recursion depth of 1000 would be exceeded extremely quickly. (I believe the stack would have to hold all 240,000 vertices in this case.)

Thus, we move to an iterative solution. The skeletal explanation of the iterative algorithm is the following:

1) Find a source node -- This is any node that is fertile and not yet counted.
2) Mark this node as counted and add it to the stack
Loop(while stack isn't empty):
    3) pop item off stack
    4) count any adjacent, uncounted nodes, then add them to the stack.

We count an area unit each time we "count" a node.

### Let's talk efficiency!
*Every single node must be visited to check if it is uncounted and fertile. It is possible for a single fertile node to be disconnected from any other fertile land, so none can be left out. O(X*Y), in this case, O(240,000)
*Every fertile node is added to the stack exactly once. It will never be revisited. O(num fertile nodes)
*The stack (which could hold up to 240,000 nodes in the worst case) is implemented using a deque instead of a list, to take advantage of the O(1) append and pop operations. (If we used a list, this would be O(N))
*After taking these steps to optimize, I prioritized clear and modular code, as in production code, it needs to be maintainable.


## Testing

### Design Decisions
* I decided that a barren land should always be provided, so with no input a usage statement is printed
  * This could be changed by making a default argument if no input is provided.
* If x1 > x2 or if y1 > y2, take them at their word that this meant the bottom left and top right. This is negative space, so would result in no tiles being marked barren.
  * To change this, I could add an integer check very easily to ensure the correct orderings are maintained, and no "negative" barren spaces are defined.
* Rather than saying the numbers should be entered in a specific way, I allow some flexibility.
  * This meant I read command line arguments in as a string, and did processing on that string. It would be more efficient to read in the values as integers, but that flexibility would be sacrificed.


### Testing inputs:

$python3 BarrenLand.py "0 292 399 307"
* EXPECTED - 116800 116800
* PASS - 116800 116800

$python3 BarrenLand.py 0 292 399 307
* EXPECTED - 116800 116800
* PASS - 116800 116800

$python3 BarrenLand.py {“0 292 399 307”}
* EXPECTED - 116800 116800
* PASS - 116800 116800
* Note: Fails on mac due to zsh error, but passes on windows

$python3 BarrenLand.py "-1 292 399 307"
* EXPECTED - Exception
* PASS - Bad input. Sequence of 4 positive integers needed for each barren area.

$python3 BarrenLand.py "0 899 399 307"
* EXPECTED - Exception
* PASS - Bad Arguments. Barren Land inputs must have x < 400 and y < 600. Exiting.

$python3 BarrenLand.py "0 292 399 307 307"
* EXPECTED - Exception
* PASS - Bad Arguments--Four integer values needed for each segment of barren land. Exiting.

$python3 BarrenLand.py "testing 0 400"
* EXPECTED - Exception
* PASS - Bad input. Sequence of 4 positive integers needed for each barren area.
 
$python3 BarrenLand.py "0 292.3 399 307"
* EXPECTED - Exception
* PASS - Bad input. Sequence of 4 positive integers needed for each barren area.

$python3 BarrenLand.py "999999999999999999999999999999999999999999999999999"
* EXPECTED - Exception
* PASS - Bad Arguments--Four integer values needed for each segment of barren land. Exiting.

$python3 BarrenLand.py
* EXPECTED - Exception
* PASS - usage: BarrenLand.py [-h] barren_land [barren_land ...] \ BarrenLand.py: error: the following arguments are required: barren_land

$python3 BarrenLand.py “48 192 351 207”, “48 392 351 407”, “120 52 135 547”, “260 52 275 547”
* EXPECTED - 22816 192608
* PASS - 22816 192608

$python3 BarrenLand.py 48 192 351 207, 48 392 351 407, 120 52 135 547, 260 52 275 547
* EXPECTED - 22816 192608
* PASS - 22816 192608

$python3 BarrenLand.py {“48 192 351 207”, “48 392 351 407”, “120 52 135 547”, “260 52 275 547”}
* EXPECTED - 22816 192608
* PASS - 22816 192608
* Note: fails on mac due to zsh error, but passes on windows.

$python3 BarrenLand.py 48 192 351 207 48 392 351 407 120 52 135 547 260 52 275 547
* EXPECTED - 22816 192608
* PASS - 22816 192608

$python3 BarrenLand.py “48 192 351 207”, “48 392 351 407”, “120 52 135 547”, “260 -52 275 547”
* EXPECTED - Exception
* PASS - Bad input. Sequence of 4 positive integers needed for each barren area.

$python3 BarrenLand.py “48 192 351 207”, “48 392 351 407”, “120 52 135 547”, “260 52 275 547 800”
* EXPECTED - Exception
* PASS - Bad Arguments--Four integer values needed for each segment of barren land. Exiting.

$python3 BarrenLand.py "0 292 399 291"
* EXPECTED - 240000
* PASS - 240000

##### A note on scalability
* I limited my hard coded values to allow for changes if need be to the width and height of the fertile land. This code could be very easily adapted to different values.

