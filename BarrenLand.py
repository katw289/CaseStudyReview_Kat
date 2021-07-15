import argparse
import sys
import re
from collections import deque

#############################################################################################################################
# Object Definitions!
#  - In this section, the Land object and LandMap objects are defined.
#  - A single Land object represents a node, fertile or infertile, in the graph. It holds information about its location,
#    its counting status, and if it is barren or not.
#  - The LandMap object consists of a matrix of Land objects, which represents the entirety of the graph. It has functions to
#    mark barren areas and count the size of fertile connected components. The location in the matrix corresponds to the x,y
#    values of the graph.
#############################################################################################################################

  #Land is a class to represent one unit of land, or a node in the graph
class Land:
    def __init__(self, x, y):
        self.wasCounted = False
        self.barren = False
        self.x = x
        self.y = y
        return

      ##Change land to barren
    def set_barren(self):
        self.barren = True
          #Barren land does not need to be counted
        self.wasCounted = True
        return

      ##Returns True if land is barren
    def is_barren(self):
        return self.barren

      ##Marks that the node has been counted
    def set_counted(self):
        self.wasCounted = True
        return

      ##Returns true if the node has already been counted
    def was_counted(self):
        return self.wasCounted

      ##Returns the x and y coordinates of this node on the grid.
    def get_location(self):
        return self.x, self.y            



  ##Land map is a class that holds the collection of Land objects (or nodes in the graph)
  ##The units are organized in a matrix such that the x and y coordinates of each land unit correspond
  ##to their position in the matrix.
class LandMap:
    def __init__(self, x, y):
        self.map = [[Land(i,j) for i in range(x)] for j in range(y)]
        self.width = x
        self.length = y
          #variables for clarity in get_adjacencies function
        self.max_x = x-1
        self.max_y = y-1
        return

      ##This function returns a list of 2-4 adjacent land tiles for any tile in the graph.
    def get_adjacencies(self, x, y):
        if(x==self.max_x):
            adjac_list = [(x-1, y)]
        elif(x==0):
            adjac_list = [(x+1, y)]
        else:
            adjac_list = [(x-1, y),(x+1, y)]
        if(y==self.max_y):
            adjac_list = adjac_list + [(x, y-1)]
        elif(y==0):
            adjac_list = adjac_list + [(x, y+1)]
        else:
            adjac_list = adjac_list + [(x, y-1), (x, y+1)]
        return adjac_list

      ##set a single unit of land to be barren
    def set_barren_single(self, x, y):
        self.map[y][x].set_barren()
        return

      ##Using bottom left and top right coordinates, mark an entire rectangle of fertile land as barren.
    def set_barren_area(self, x1, y1, x2, y2):
        for x in range(x1, x2+1):
            for y in range(y1, y2+1):
                self.set_barren_single(x, y)

      ##This function sends source nodes (or a newly found connected component of the graph) to the depth traversal function.
      ##If there are 2 connected components of fertile land in the map, the DFT function will be called exactly twice.
    def get_fertile_area(self):
        areas = []
        for x in range(self.width):
            for y in range(self.length):
                if(not self.map[y][x].was_counted()):
                    areas.append(self.get_area_portion_DFT(x,y))
        if(len(areas)==0):
            return [0]
        return areas
                
      ##This function implements the depth first traversal for a single connected component. 
    def get_area_portion_DFT(self, x, y):
          #stack is deque for O(1) append and pop operations
        stack = deque()
          ##append source node
        stack.append(self.map[y][x])
        self.map[y][x].set_counted()
          ##every time we do a "count" command, we add one to the area.
        area = 1
        while(len(stack)>0):
            current = stack.pop()
            x, y = current.get_location()
            adj_list = self.get_adjacencies(x,y)
            for item in adj_list:
                  #x and y value of each adjacent value iterated through.
                x,y = item
                if(not self.map[y][x].was_counted()):
                      #if the adjacent value was not counted already, it is marked counted and added to the stack.
                    stack.append(self.map[y][x])
                    self.map[y][x].set_counted()
                    area = area + 1
        return area

#############################################################################################################################
# Command Line Parsing Utilities
#   - Due to the design decision to allow flexibility in how the values are input, there is a lot of regex parsing of user input.
#   - This is separated into 4 distinct functions, that represent a phase of the parsing process.
#       1. parse_command_line()
#           -This function does the basic argparse definitions of the parser arguments.
#       2. verify_args()
#           -This is where the majority of the input parsing is done. When the function completes, the user input is scaled down
#           to just the integer values.
#       3. get_ints_from_args() 
#           - turn the string values into integer values
#       4. get_four_tuples_from_args()
#           - This separates the integer values into 4-tuples to be easily parsed by main.
#############################################################################################################################

def parse_command_line():
    parser = argparse.ArgumentParser(description="Calculate Areas of Fertile Land")
    parser.add_argument("barren_land", type=str, nargs='+', help="variable that holds the coordinates of the barren land.")
    args = parser.parse_args()
    args = verify_args(args.barren_land)
    return(args)

  ##string parsing to pull integers from user input. Called in parse_command_line function.
def verify_args(args):
    barren_lands = []
      #This join is necessary to ensure that the arguments entered are a multiple of 4. In the case where there are no quotation marks
      #around the user input, even with 4 integer values this function would fail. It also removes the need for a for-loop in cases where
      #there are multiple barren land segments.
    args = " ".join(args)
    args = re.sub('{','',args)
    args = re.sub('}','',args)
    args = re.sub(',',' ', args)
    args = re.sub("  ", ' ', args)
      #In the next section, check_num is redefined multiple times to check different cases to ensure input validity.
    check_num = re.search("^[\s\d]*$", args)
    if(check_num == None):
        print("Bad input. Sequence of 4 positive integers needed for each barren area.")
        exit(2)
    check_num = re.findall("\d+", args)
    if(len(check_num)%4 != 0):
        print("Bad Arguments--Four integer values needed for each segment of barren land. Exiting.") 
        exit(2)
    return args

def get_ints_from_args(args):
    args_int = []
    for item in args.split():
        if item.isdigit():
            args_int.append(int(item))
    return args_int

  #get user input into 4-tuples easily parsed in main body.
def get_four_tuples_from_args(args):
    args_tuple = []
    for i in range(len(args)//4):
          #To pull out each segment of four, use multiply 4 by i to get the first value. Then add to get subsequent positions.
        v1 = args[4*i]
        v2 = args[4*i + 1]
        v3 = args[4*i + 2]
        v4 = args[4*i + 3]
        args_tuple.append((v1, v2, v3, v4))
    return args_tuple

  
  
###########MAIN###################
if __name__=="__main__":
      #This is the only place these values are hard coded. Thus, rework is
      #reduced if modifications are needed.
    x = 400
    y = 600

      #parse command lines
    args = parse_command_line()
    args = get_ints_from_args(args)
    args = get_four_tuples_from_args(args)

      #create the LandMap object, which will instantiate each land unit.
    land_map = LandMap(x, y)

      #add the barren land segments to the land map
    for val in args:
        v1, v2, v3, v4 = val
        if(not (v1 < x and v2 < y and v3 < x and v4 < y)):
            print("Bad Arguments. Barren Land inputs must have x < {} and y < {}. Exiting.".format(x,y))
            exit(2)
        land_map.set_barren_area(v1, v2, v3, v4)
        
      #do the traversal, find the needed values.
    areas = land_map.get_fertile_area()
      #Print!
    for item in sorted(areas):
        print(item, end= ' ')
