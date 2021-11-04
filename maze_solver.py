''' File name: maze_solver.py
    Author: Benjamin Nylen
    Purpose: To create a program that is able to solve a maze,
    utilizing a custom tree class.
'''

class MazeTree:
    ''' This class represents a tree that is utilized for finding
        the correct path from start to end of a maze. It must contain
        a value in each node, and will have 4 children representing
        adjacent spaces within the maze. 

        The constructor of this class begins by building the MazeTree
        node with a value in it, as well as the 4 adjacent child nodes.

        The class only utilizes a single method, which is a __str__ method
        to aid in the printing of the tree:
        __str___(self): Prints the value of the node at that point.
    '''
    def __init__(self,value):
        self._value = value
        self._right = None
        self._left = None
        self._up = None
        self._down = None
    def __str__(self):
        print(self._value)

def interpret_data(file):
    ''' Function Purpose: This function reads in the file, and
        creates a set of tuples based off of all the characters
        in the maze. It should be noted that this function will
        check for characters that do not belong in the maze, and
        if this is the case, the program will shut down. Moreover,
        this function helps in determining the start and end 
        coordinates in the maze.
        Arguments:
        - file: This is the name of the file to be interpreted from
            main.
        Return Values:
        - positions: A set of tuples which contain the coordinates of
        all of the characters that are not spaces.
        - start: the coordinates of the start position, noted by 'S'
        - end: the coordinates of the end position, noted by 'E'
        - s_count: Used to check if there is more than one start
        position in the maze. If this is the case, the main function
        will shut down the program.
        - e_count: Used to check if there is more than one end
        position in the maze. If this is the case, the main function
        will shut down the program.
        - is_chars: A boolean used to check if there is an invalid
        character in the maze. If there is, the main function will
        shut down the program.
    '''
    s_count = 0
    e_count = 0
    is_chars = True
    lines = file.readlines()
    positions = set()
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            if lines[i][j] == '#':
                positions.add((j,i))
            if lines[i][j] == 'S':
                start = (j,i)
                positions.add((j,i))
                s_count += 1
            if lines[i][j] == 'E':
                end = (j,i)
                positions.add((j,i))
                e_count += 1
            if lines[i][j] not in ['#','S','E','\n',' ',]:
                is_chars = False
    if s_count == 0 or e_count == 0:
        start = None
        end = None
    return positions, start, end, s_count, e_count, is_chars

def build_tree(start, positions):
    ''' Function Purpose: This function builds the tree, utilizing
        the start position, as well as the positions set in order
        to figure out which coordinates are adjacent to the start
        Arguments:
        - positions: A set of tuples which contain the coordinates of
        all of the characters that are not spaces.
        - start: the coordinates of the start position, noted by 'S'
        Return Values:
        - root: The beginning of the tree used in this program.
    '''
    root = MazeTree(start)
    positions.remove(start)
    if (start[0],start[1] - 1) in positions:
        curr = (start[0],start[1] - 1)
        root._down = build_tree(curr, positions)
    if (start[0],start[1] + 1) in positions:
        curr = (start[0],start[1] + 1)
        root._up = build_tree(curr, positions)
    if (start[0] - 1,start[1]) in positions:
        curr = (start[0] - 1,start[1])
        root._left = build_tree(curr, positions)
    if (start[0] + 1,start[1]) in positions:
        curr = (start[0] + 1,start[1])
        root._right = build_tree(curr, positions)
    return root  

def print_tree(root,indent=''):
    ''' Function Purpose: This function is utilized
        to print out the contents of the MazeTree object,
        in the form of a preorder traversal. It is a 
        recursive algorithm through the tree, grabbing
        the values.
        Arguments:
        - root: The beginning of the tree used in this program.
        - indent: This variable aids in the spacing of this
        recursive algorithm
        Return Values:
        - The program will return if the current node does
        not have any children.
    '''
    if root is None:
        return
    print(f"  {indent}{root._value}")

    print_tree(root._down, indent+'| ')
    print_tree(root._up, indent+'| ')
    print_tree(root._left, indent+'| ')
    print_tree(root._right, indent+'| ')

    return None

def determine_size(positions_copy):
    ''' Function Purpose: This function carries out
        the purpose of the dumpSize command, which
        requests the dimensions of the maze.
        Arguments:
        - positions_copy: This is a copy of the positions
        set, since the original set is blank after creating
        the tree.
        Return Values:
        None
    '''
    max_x = 0
    max_y = 0
    for element in positions_copy:
        if element[0] > max_x:
            max_x = element[0]
        if element[1] > max_y:
            max_y = element[1]
    print('MAP SIZE:')
    print('  wid:', max_x + 1)
    print('  hei:', max_y + 1)

def determine_wid_hei(positions_copy):
    ''' Function Purpose: This function serves a similar
        purpose to the determine size function. However,
        this one aids in printing out the tree, by simply 
        grabbing the dimensions and putting them into a tuple.
        Arguments:
        - positions_copy: This is a copy of the positions
        set, since the original set is blank after creating
        the tree.
        Return Values:
        - (max_x, max_y): A tuple containing the width and height
        of the maze.
    '''
    max_x = 0
    max_y = 0
    for element in positions_copy:
        if element[0] > max_x:
            max_x = element[0]
        if element[1] > max_y:
            max_y = element[1]
    return (max_x, max_y)

def determine_path(root, end):
    ''' Function Purpose: This function serves the purpose
        of carrying out the dumpSolution command. It is
        a recursive algorithm that searches through the
        tree and creates a list containing the solution
        from start to end of the maze. 
        Arguments:
        - root: The beginning of the tree used in this program,
        AKA the start position.
        - end: the coordinates of the end position, noted by 'E'
        Return Values:
        - This function will simply return when it had reached the end
        of the tree. Otherwise, it will continue to add to the list
        of coordinates containing the solution.
    '''
    if root is None:
        return
    if root._value == end:
        return [root._value]
    children = [root._left,root._right,root._up,root._down]
    for element in children:
        recursive = determine_path(element,end)
        if recursive is not None:
            return [root._value] + recursive

def print_map(path,start,end,positions_copy,maxes):
    ''' Function Purpose: This function serves the purpose
        of printing out the map if the user does not
        provide a specific command. It should be noted
        that on this map, the solution is noted using
        periods.
        Arguments:
        - path: This is a variable defined in main, that
        represents the list of coordinates containing
        the solution from start to finish, as determined in
        the determine_path() function.
        - start: the coordinates of the start position, noted by 'S'
        - end: the coordinates of the end position, noted by 'E'
        - positions_copy: This is a copy of the positions
        set, since the original set is blank after creating
        the tree.
        - maxes: This is a variable created in main, denoting
        the tuple returned in the determine_wid_hei function
        in order to figure out the dimensions of the maze
        for printing.
    '''
    grid = []
    for i in range(maxes[1]+1):
        inner = []
        for j in range(maxes[0]+1):
            element = (j,i)
            if element == start:
                inner.append('S')
            elif element == end:
                inner.append('E')
            elif element in path:
                inner.append('.')
            elif element in positions_copy:
                inner.append('#')
            else:
                inner.append(' ')
        grid.append(inner)
    for element in grid:
        print(''.join(element)),


def main():
    while True:
        try:
            file_name = input()
            file = open(file_name,'r')
            positions, start, end, s_count, e_count, is_chars = interpret_data(file)
            if not is_chars:
                print('ERROR: Invalid character in the map')
                break
            if s_count > 1:
                print('ERROR: The map has more than one START position')
                break
            if e_count > 1:
                print('ERROR: The map has more than one END position')
                break
            if start is None:
                print('ERROR: Every map needs exactly one START and exactly one END position')
                break
            positions_copy = positions.copy()
            root = build_tree(start, positions)
        except FileNotFoundError:
            print('ERROR: Could not open file: NO_SUCH_FILE')
            break
        except EOFError:
            break
        command = input()
        if command == 'dumpCells':
            print('DUMPING OUT ALL CELLS FROM THE MAZE:')
            for element in sorted(positions_copy):
                if element == start:
                    print(' ', element, '   START')
                elif element == end:
                    print(' ', element, '   END')
                else:
                    print(' ', element)
        elif command == 'dumpTree':
            print('DUMPING OUT THE TREE THAT REPRESENTS THE MAZE:')
            print_tree(root,indent='')
        elif command == 'dumpSolution':
            print('PATH OF THE SOLUTION:')
            path = determine_path(root, end)
            for element in path:
                print(' ', element)
        elif command == 'dumpSize':
            determine_size(positions_copy)
        elif command == '':
            print('SOLUTION:')
            path = determine_path(root, end)
            maxes = determine_wid_hei(positions_copy)
            print_map(path,start,end,positions_copy, maxes)
        else:
            print('ERROR: Unrecognized command NOT_A_VALID_COMMAND')
            break
main()