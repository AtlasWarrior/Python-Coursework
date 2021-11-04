''' File: twine.py
    Author: Benjamin Nylen
    Purpose: This program serves as a game which supports the following commands:
    n, e, w, s, back, crossings, map, ranges, and a blank string. Based on user
    input, the program will form a continuous game, asking for commands until
    the loop is broken. It should be noted that user position and history
    are consistently updated as the games continues along.
'''


def interpret_data(x,y,position,obstacles_lst):
    ''' This function's purpose is to interpret user commands, and point each command
        to the proper function in order to carry out said command task. The 4 arguments
        come from main. The variable x, y, and position are all utilized to keep
        the user updated consistently on the position and history. The 4th argument,
        obstacles_lst is utilized in the case that an obstacles file is passed in,
        where it will be directed to another function for other purposes.
    '''
    lst = [(0,0)]
    command_log = ['n','e','w','s','back','crossings','ranges','','map']
    command_list = []
    string = ''
    while True:
        print('Current position:', position)
        print('Your history:' + '    ',lst)
        print('What is your next command?')
        try:
            user_data = input().strip()
        except:
            break
        if user_data in command_log:
            if user_data == 'n' or user_data == 'e' or user_data == 'w' or user_data == 's':
                x,y,position = directional_commands(x,y,position,command_list,lst,user_data,obstacles_lst)
            if user_data == '':
                print('You do nothing.')
            if user_data == 'back' or user_data == 'ranges' or user_data == 'crossings':
                x,y,position = other_commands(x,y,position,lst,user_data,command_list)
            if user_data == 'map':
                print('+-----------+')
                map(position,x,y,lst,obstacles_lst)
                print('+-----------+')
        else:
            print('ERROR: Invalid Command. Please Enter a Supported Command')
        print()
        

def map(position,x,y,lst,obstacles_lst):
    ''' This function is responsible for printing out the map, in the case
        that the user inputs the command "map." The 4 arguments come from main
        and the interpret_data function. The variables x,y, and position are
        passed in to ensure that the position and history are consistently
        updated. The variable lst is passed in from interpret data, in order
        for the map to print out the previous history as to where the player
        has been. Finally, obstacles_lst is passed in so the map can make
        note of all of the obstacles and their locations.
    '''
    grid = [[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' '],[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']]
    for element in lst:
        grid[element[1]+5][element[0]+5] = '.'
    grid[5][5] = '*'
    grid[position[1]+5][position[0]+5] = '+'
    for obstacle in obstacles_lst:
        grid[obstacle[1]+5][obstacle[0]+5] = 'X'
    for row in grid[::-1]:
        print('|',end='')
        for column in row:
            print(column, end='')
        print('|',end='')
        print()

def other_commands(x,y,position,lst,user_data,command_list):
    ''' This function is responsible for handling the back, 
        ranges, and crossings commands. The x, y, position, and
        user_data argument are utilized to determine which command
        was inputted, and so that the history and position of the
        player can be updated. The variable lst is utilized for the
        crossings function, and will determine how many times that 
        has been seen throughout the history. Finally, command_list
        is utilized for back, so that the x and y variables can be
        adjusted.
    '''
    if user_data == 'back':
        if len(lst) == 1:
            print("Cannot move back, as you're at the start!")
        else:
            lst.pop()
            position = lst[-1]
            string = command_list.pop()
            if string == 'n':
                y -= 1
            elif string == 'e':
                x -= 1
            elif string == 'w':
                x += 1
            else:
                y += 1
            print('You retrace your steps by one space')
        return x,y,position
                
    elif user_data == 'ranges':
        furthest_west = 0
        furthest_east = 0
        furthest_south = 0
        furthest_north = 0
        for element in lst:
            xval = element[0]
            yval = element[1]
            furthest_west = min(xval, furthest_west)
            furthest_east = max(xval, furthest_east)
            furthest_south = min(yval,furthest_south)
            furthest_north = max(yval, furthest_north)
        print('The furthest West your twine goes is', furthest_west)
        print('The furthest East your twine goes is', furthest_east)
        print('The furthest South your twine goes is', furthest_south)
        print('The furthest North your twine goes is', furthest_north)
        return x,y,position
    elif user_data == 'crossings':
        times_crossed = 1
        for element in lst[:-1]:
            if element == lst[-1]:
                times_crossed += 1
        print('There have been', times_crossed, 'times in the history when you were at this point.')
        return x,y,position


def directional_commands(x,y,position,command_list,lst,user_data,obstacles_lst):
    ''' This function is responsible for handling the n, e, w, and s comamnds.
        The arguments x, y, and position are passed in so that each variable
        can be properly updated following entering a specific directional 
        command. The variable user_data is passed in so that the function
        can determine which directional command the user has inputted.
        Finally, the command_list, lst, and obstacles_lst variables are
        passed in to check for potential obstacles in the player's path,
        update the list of commands inputted by the user, and update the
        history of where the player has been.
    '''
    if user_data == 'n':
        if (x,y + 1) in obstacles_lst:
            print('You could not move in that direction, because there is an obstacle in the way.')
            print('You stay where you are.')
        else:
            position = (x,y + 1)
            y += 1
            lst.append(position)
            command_list.append(user_data)
    elif user_data == 's':
        if (x,y - 1) in obstacles_lst:
            print('You could not move in that direction, because there is an obstacle in the way.')
            print('You stay where you are.')
        else:
            position = (x,y - 1)
            y -= 1
            lst.append(position)
            command_list.append(user_data)
    elif user_data == 'e':
        if (x + 1,y) in obstacles_lst:
            print('You could not move in that direction, because there is an obstacle in the way.')
            print('You stay where you are.')
        else:
            position = (x + 1,y)
            x += 1
            lst.append(position)
            command_list.append(user_data)
    elif user_data == 'w':
        if (x - 1,y) in obstacles_lst:
            print('You could not move in that direction, because there is an obstacle in the way.')
            print('You stay where you are.')
        else:
            position = (x - 1,y)
            x -= 1
            lst.append(position)
            command_list.append(user_data)
    return x,y,position

def obstacles(user_input,obstacles_file):
    ''' This function is responsible for reading in the
        obstacles file and intepreting the data in a way
        that the program deems useful. The argument 
        user_data is passed in to get the full name of the
        file to be opened.
    '''
    if user_input == '-':
        return []
    obstacles_lst = []
    #obstacles_file = open(user_input,'r')
    for line in obstacles_file:
        remove = line.strip().split()
        x = int(remove[0])
        y = int(remove[1])
        obstacles_lst.append((x,y))
    return obstacles_lst


def main():
    x = 0
    y = 0
    position = (x,y)
    f_name = None
    while f_name is None:
        print('Please give the name of the obstacles filename, or - for none:')
        try:
            user_input = input().strip()
        except:
            break
        if user_input == '':
            print('ERROR: Please enter a valid file name.')
            continue
        elif user_input == '-':
            break
        else:
            try:
                f_name = open(user_input,'r')
                break
            except:
                f_name = None
                continue
    obstacles_lst = obstacles(user_input,f_name)
    interpret_data(x,y,position,obstacles_lst)

main()