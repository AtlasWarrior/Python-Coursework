''' File: sudoku_helper.py
    Author: Benjamin Nylen
    Purpose: This program serves as an interactive tool
            to help people solve sudoku puzzles.
'''

from list_node import *
import os

def interpret_data(sudoku):
    ''' Function Purpose: To read the information from the input file into an of 
        array of strings, which will be able to be converted into a 2D array later.
        Parameters: 
        - Sudoku: The text file to be interpreted from main.
        Return Values:
        - array_of_strings: An array of strings created from the original text file.
    '''
    array_of_strings = []
    try:
        file = open(sudoku, 'r').readlines()
    except:
        return
    for element in file:
        remove_space = element.strip().split()
        join = ''.join(remove_space)
        if join == '':
            continue
        array_of_strings.append(join)
    return array_of_strings

def arr_of_strs_to_2d_array(array_of_strings):
    ''' Function Purpose: To convert the array of strings into a 2D array, which
        can be later used to get the rows, columns, and squares of the puzzle.
        Parameters:
        - array_of_strings: An array of strings created from the original text file.
        Return Values:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
    '''
    lst = []
    for x in range(len(array_of_strings)):
        list_of_letters = []
        for y in range(0,len(array_of_strings[x])):
            list_of_letters.append(array_of_strings[y][x])
        lst.append(list_of_letters)
    return lst

def command_center(lst, head):
    ''' Function Purpose: This function is responsible for handling commands,
        as well as interpreting the command and calling the correct function
        to carry out said command.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    input_yes = True   # set to true for other commands
    print('Your command:')
    while True:
        try:
            command_line = input()
        except:
            break
        split_command = command_line.split()
        if split_command == []:
            input_yes = False
            continue
        elif split_command[0] == 'set':
            x = int(split_command[1])
            y = int(split_command[2])
            value = split_command[3]
            set_command(x,y,value,lst)
            new_node = push_listnode(head,lst)
            print()
            print_grid(lst)
            print('Your command:')
        elif split_command[0] == 'conflicts':
            conflicts_command(lst)
            print()
            print_grid(lst)
            print('Your command:')
        elif split_command[0] == 'back':
            head = back_command(new_node, lst, new_node)
            print('Your command:')
        elif split_command[0] == 'search':
            search_command(lst)
            print('Your command:')
        else:
            print('ERROR: Invalid command')
            print()
            print_grid(lst)
            print('Your command:')


def search_command(lst):
    ''' Function Purpose: This function is responsible for carrying out the
        search command in command_center.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    columns, rows = get_columns_and_rows(lst)
    for i in range(len(lst)):
        for j in range(len(lst[i])):
            dictt = {}
            if lst[i][j] == '.':
                get_col(lst, i, dictt)
                get_row(lst, j, dictt)
                print(dictt)
                square_lst = get_square(lst,i,j)
                check_specific_row_column(lst, i, j, dictt, rows, columns, square_lst)
    print(dictt)

def get_col(lst, i, dictt):
    ''' Function Purpose: To pull a specific column from the grid.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        - i: Index of column
        - dictt: A dictionary noting which numbers are in the row/column.
        Return Values:
        - None
    '''
    col = lst[i]
    for element in col:
        if element not in dictt:
            if element != '.':
                dictt[element] = 1

def get_row(lst, j, dictt):
    ''' Function Purpose: To pull a specific column from the grid.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        - j: Index of row
        - dictt: A dictionary noting which numbers are in the row/column.
        Return Values:
        - None
    '''
    getting_rows = []
    for element in lst:
        getting_rows.append(element[j])
    for element in getting_rows:
        if element not in dictt:
            if element != '.':
                dictt[element] = 1
               
def check_specific_row_column(lst, i, j, dictt, columns, rows, square_lst):
    ''' Function Purpose: To pull a specific column from the grid.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        - i: index of column
        - j: Index of row
        - dictt: A dictionary noting which numbers are in the row/column.
        - columns: A 2D array containing each column as an index.
        - rows: A 2D array containing each row as an index.
        - square_lst: A list containing the values of a specific subregion or 
                      square within the sudoku puzzle.
        Return Values:
        - None
    '''
    if columns[i][j] not in dictt:
        if columns[i][j] != '.':
            dictt[columns[i][j]] = 1
    if rows[i][j] not in dictt:
        if rows[i][j] != '.':
                dictt[rows[i][j]] = 1
    for element in square_lst:
        if element not in dictt:
            if element != '.':
                dictt[element] = 1
    
# loop through rows and columns and append each to a dictionary 

def back_command(head, lst, new_node):
    ''' Function Purpose: This function is responsible for carrying out the
        back command in command_center, and adjusting the head pointer in the
        linked list. It will pop the current head pointer, and set the head
        equal to the 2nd node in the linked list
        Parameters:
        - head: Refers to the beginning of the linked list.
        Return Values:
        - head: Returns the 2nd node in the linked list, which is now head.
    '''
    if head.next is None:
        print('ERROR: You are already at the init state, you cannot go back.')
        print()
        print_grid(lst)
    else:    
        head = head.next
        print_grid(head.val)
    return head

def conflicts_command(lst):
    ''' Function Purpose: This function is responsible for carrying out the
        conflicts command in command_center.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    columns, rows = get_columns_and_rows(lst)
    is_clear = None
    is_clear = find_conflict_in_columns(columns, is_clear)
    is_clear = find_conflict_in_rows(rows, is_clear)
    is_clear = find_conflict_in_subregions(lst, is_clear)
    if is_clear is True:
        print('Hooray! No conflicts found.')

def find_conflict_in_subregions(lst, is_clear): 
    ''' Function Purpose: This function is responsible for carrying out
        a portion of the conflicts command. It searches and finds a 
        conflict in each subregion, or square of the sudoku puzzle.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    for x in range(3):
        for y in range(3):
            temp_dict = {}
            square_lst = get_square(lst,x,y)  
            for element in square_lst:
                if element != '.':
                    if element not in temp_dict:
                        temp_dict[element] = 1
                    else:
                        temp_dict[element] += 1
            for keys, values in temp_dict.items():
                if temp_dict[keys] > 1:
                    print('ERROR: Sub-region', str(x + 1) + ',' + str(y + 1), 'has a conflict.')
                    is_clear = False
                    break
                else:
                    if is_clear == False:
                        is_clear = False
                    else:
                        is_clear = True
                    continue
    return is_clear        

def find_conflict_in_rows(rows, is_clear):
    ''' Function Purpose: This function is responsible for carrying out
        a portion of the conflicts command. It searches and finds a 
        conflict in each row of the sudoku puzzle.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    for x in range(len(rows)):
        temp_dict = {}
        for y in range(len(rows[x])):
            if rows[x][y] != '.':
                if rows[x][y] not in temp_dict:
                    temp_dict[rows[x][y]] = 1
                else:
                    temp_dict[rows[x][y]] += 1
        for keys, values in temp_dict.items():
            if temp_dict[keys] > 1:
                print('ERROR: Row', x + 1, 'has a conflict.')
                is_clear = False
                break
            else:
                if is_clear == False:
                    is_clear = False
                else:
                    is_clear = True
                continue
    return is_clear 

def find_conflict_in_columns(columns, is_clear):
    ''' Function Purpose: This function is responsible for carrying out
        a portion of the conflicts command. It searches and finds a 
        conflict in each column of the sudoku puzzle.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    for x in range(len(columns)):
        temp_dict = {}
        for y in range(len(columns[x])):
            if columns[x][y] != '.':
                if columns[x][y] not in temp_dict:
                    temp_dict[columns[x][y]] = 1
                else:
                    temp_dict[columns[x][y]] += 1
        for keys, values in temp_dict.items():
            if temp_dict[keys] > 1:
                print('ERROR: Column', x + 1, 'has a conflict.')
                is_clear = False
                break
            else:
                if is_clear == False:
                    is_clear = False
                else:
                    is_clear = True
                continue
    return is_clear 

def get_square(lst,sx,sy):
    ''' Function Purpose: This function is utilized within
        find_conflict_in_subregions, and puts each square of the
        sudoku puzzle into a list, so that it can be checked properly.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        - sx: The x value of the square being checked.
        - sy: The y value of the square being checked.
        Return Values:
        - square_lst: A list containing the values of a specific subregion or 
                      square within the sudoku puzzle.
    '''
    square_lst = []
    column = sx * 3
    row = sy * 3
    for x in range(column, column + 3):
        for y in range(row, row+3):
            square_lst.append(lst[x][y])
    return square_lst

def get_columns_and_rows(lst):
    ''' Function Purpose: This function is mainly utilized within the
        conflicts_command function. It is served to gather each column
        and row into its own 2D list, so that the conflicts_command
        function will be able to properly check if there is a conflict
        somewhere on the sudoku board.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - columns: A 2D array containing each column as an index.
        - rows: A 2D array containing each row as an index.
    '''
    columns = []
    rows = []
    for x in range(len(lst)):
        each_column = []
        each_row = []
        for y in range(len(lst[x])):
            each_column.append(lst[x][y])
            each_row.append(lst[y][x])
        columns.append(each_column)
        rows.append(each_row)
    return columns, rows

def set_command(x,y, value,lst):
    ''' Function Purpose: This function is responsible for carrying out
        the set command in command_center. 
        Parameters:
        - x: The x value of the position to be set.
        - y: The y value of the position to be set.
        - value: The number to which the position will be set to.
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    if lst[x-1][y-1] != '.':
        print("ERROR: The 'set' command cannot run, because the space already holds a value.")
    else:
        lst[x-1][y-1] = value
        print('Square', str(x) + ',' + str(y), 'set to', str(value) + '.')


def push_listnode(head,lst):
    ''' Function Purpose: This function is responsible for inserting a new node
        into the linked list, after a specific value has been set.
        Parameters:
        - head: The beginning of the linked list.
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - new_node = The new beginning of the linked list, which was inserted.
    '''
    new_node = ListNode(dup_grid(lst))
    new_node.next = head
    head = new_node
    return new_node

def dup_grid(lst):
    ''' Function Purpose: This function is responsible for duplicating
        the sudoku board, for the purposes of keeping track of the player's
        history.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - copy: A new version of the sudoku board, similar to the current one.
    '''
    copy = []
    for row in lst:
        row_lst = []
        for column in row:
            row_lst.append(column)
        copy.append(row_lst)
    return copy

def print_grid(lst):
    ''' Function Purpose: This function is responsible for simply
        printing out the sudoku board.
        Parameters:
        - lst: A 2D array of strings, which contain the necessary information to 
               properly access the sudoku puzzle throughout the program.
        Return Values:
        - None
    '''
    for y in range(9):
        if y == 3 or y == 6:
            print('\n')
        for x in range(9):
            if x == 3 or x == 6:
                print(' ', end='')
            if lst[x][y] == 0:
                print('.', end='')
                continue
            print(lst[x][y], end='')
        print()
 
def main():
    sudoku = input('Please give the name of the file that contains the board: \n')
    array_of_strings = interpret_data(sudoku)
    if array_of_strings is None:
        print('ERROR: The file could not be opened.')
    else:
        lst = arr_of_strs_to_2d_array(array_of_strings)
        head = ListNode(lst)
        print_grid(lst)
        command_center(lst,head)

main()

