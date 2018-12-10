#import libraries
from collections import namedtuple
from operator import itemgetter
from pprint import pformat

# Class definition from : https://en.wikipedia.org/wiki/K-d_tree
class Node(namedtuple('Node', 'location left_child right_child')):
    def __repr__(self):
        return pformat(tuple(self))

# code from "https://en.wikipedia.org/wiki/K-d_tree" adapted to our case
# function description : buit a tree from the given set of data points
def k_d_tree(point_list, depth=0):
    k = len(point_list[0])

    # stop condition
    if len(point_list) == 1:
        return Node (
            location=point_list,
            left_child=0,
            right_child=0,
            )

    # find axis of comparison
    axis = depth % k
    if axis == 0:
        axis = 1
    else:
        axis = 0

    # sort point list
    point_list.sort(key=itemgetter(axis))

    # get median
    median = len(point_list) // 2

    # calculate the threshold
    val = float(point_list[median-1][axis] + point_list[median][axis])/2
    
    return Node(
        location=val,
        left_child=k_d_tree(point_list[:median], depth + 1),
        right_child=k_d_tree(point_list[median:], depth + 1)
        )

# our own code 
# function description : find the nearest neighbor of given point
def query(tree, point, depth=0):

    k = 2 # dimension of the k-d tree
    axis = depth % k
    if axis == 0:
        axis = 1
        axis_name = "height"
    else:
        axis = 0
        axis_name = "width "

    # stop case : result found 
    if tree[1] == 0 and tree[2] == 0:
        return tree[0]

    # choose part of the decision tree to visit
    if tree[0] < point[axis]:
        print "trace : point", axis_name, " > ", tree[0], ": YES"
        return query(tree[2], point, depth+1)
    else:
        print "trace : point", axis_name, " < ", tree[0], ": NO"
        return query(tree[1], point, depth+1)

# our own code 
# function description : gives the color of a point
def color(point):
    if point == (1, 2) or point == (2, 6):
        return "Red"
    elif point == (2, 1):
        return "Violet"
    elif point == (4, 2):
        return "Blue"
    elif point == (6, 1):
        return "Green"
    elif point == (2, 5) or point == (1, 4):
        return "Orange"
    elif point == (6, 5):
        return "Purple"
    elif point == (5, 6):
        return "Yellow"


# our own code
# function escription : get the nearest neighbor value, color and trace of calculation
def get_nearest_neighbor(point_list):
    # buit a tree from the set of points "point_list"
    tree = k_d_tree(point_list)
    
    # Unknown data points
    unknown = [(1, 4), (1, 1), (6, 6), (6, 1), (4, 4)]
    for u in unknown:
        # print the unknown data point value
        print "\n******* unknown is :" , u, "*********"
        
        # query the tree with a new data point 
        nearest_neighbor = query(tree, u)[0]

        # print the nearest neighbor of the data point 
        print "nearest_neighbor is :", nearest_neighbor

        # print the color of that nearest neighbor
        print "color is :", color(nearest_neighbor)
        

# our own code
# function description : main function with two examples 
def main():
    # the set of points from chapter 19 example 
    point_list = [(2,1), (1,2), (2,5), (2,6), (4,2), (5,6), (6,5), (6,1)]
    print "\n########################### original set of points ########################"
    get_nearest_neighbor(point_list)

    # the set of points from chapter 19 example with addition of unknown point (1, 4)
    point_list = [(2,1), (1,2), (2,5), (2,6), (4,2), (5,6), (6,5), (6,1), (1,4)]
    print "\n########### set of points with addition of unknown point (1, 4) ###########"
    get_nearest_neighbor(point_list)

# call main function 
if __name__ == '__main__':
    main()
