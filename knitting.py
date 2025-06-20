'''
This file contains functions to generate a knitting pattern based on specific heights and distances,
plus functions to convert the generated pattern to human-readable strings.

'''


def generate_pattern(b_height: int, b_dist: int) -> list:
    '''
    Returns a list representing a knitting pattern for given bumpiness params
    '''
    pattern = []
    for n in range(2):
        row = []
        row.append((' ', b_height))
        row.append(('k', b_dist * 2 + b_height*2 + 2))
        pattern.append(row)
    for n in range(b_height):
        row = []
        row.append((' ', b_height - n))
        if n>0:
            row.append(('k', n))
        row.append(('kyok', 1))
        row.append(('k', b_height - 1 + b_dist))
        row.append(('sk2p', 1))
        row.append(('k', b_height - 1 + b_dist - n))
        pattern.append(row)
    for n in range(2):
        row = []
        row.append(('k', b_dist * 2 + b_height*2 + 2))
        pattern.append(row)
    for n in range(b_height):
        row = []
        row.append((' ', n))
        row.append(('k', b_height - 1 - n))
        row.append(('sk2p', 1))
        row.append(('k', b_height - 1 + b_dist))
        row.append(('kyok', 1))
        row.append(('k', n+b_dist))
        pattern.append(row)
    return pattern

def pattern_to_string(pattern: list) -> str:
    '''
    Converts a list as generated by generate_pattern() to a string that can be easily read by humans.
    This function exists to check that pattern generation wasre working and isn't used for anything else
    Returns a string (instructions).
    '''
    pattern_string = ''
    for n in range(len(pattern)):
        pattern_string += f'Row {n+1}: '
        for i in range(len(pattern[n])):
            #check stitch type and add instructions to the return string
            stitch = pattern[n][i][0]
            if stitch == 'kyok' or stitch == 'sk2p':
                pattern_string += f'{stitch}, '
            elif stitch == 'k':
                num = pattern[n][i][1]
                pattern_string += f'{stitch}{num}, '
        pattern_string += '\n'
    pattern_string +='Repeat from Row 1'
    return pattern_string

def pattern_to_strarray(pattern: list) -> list:
    '''
        Converts a list as generated by generate_pattern() to a list where
        every item in the list is instructions for one row of the knitting pattern
        Returns list of strings (row by row instructions)
    '''
    pattern_strarray = ['Instructions:']

    #set up flags and storage variables for previous rows
    repeat_row_before = False
    repeat_count = 0
    instruction = ''

    for n in range(len(pattern)):
        #check if this row is one that gets repeated and stores it if it is
        if len(pattern[n]) <= 2:
            if repeat_row_before:
                repeat_count += 1
            repeat_row_before = True
            for i in range((len(pattern[n]))):
                stitch = pattern[n][i][0]
                if stitch == 'k':
                    num = pattern[n][i][1]
                    instruction = f'{stitch}{num},'
        else:
            #if the end of the repeated rows is reached, summarise them and add them to the return list
            if repeat_row_before:
                if repeat_count == 0:
                    line = f'Row {n-1}: {instruction}'
                    pattern_strarray.append(line)
                else:
                    end_repeat = n
                    start_repeat = end_repeat-repeat_count
                    repeated_rows = f'Rows {start_repeat}-{end_repeat}: {instruction}'
                    pattern_strarray.append(repeated_rows)
            #otherwise, read a row input list and turn it into a string of human-readable instructions
            pattern_string = f'Row {n+1}: '
            for i in range(len(pattern[n])):
                row_n = len(pattern[n])
                stitch = pattern[n][row_n-i-1][0]
                if stitch == 'kyok' or stitch == 'sk2p':
                    pattern_string += f'{stitch}, '
                elif stitch == 'k':
                    num = pattern[n][row_n-i-1][1]
                    pattern_string += f'{stitch}{num}, '
            repeat_row_before = False
            repeat_count = 0
            pattern_strarray.append(pattern_string)
    pattern_strarray.append('Repeat from Row 1')
    return pattern_strarray 


if __name__ == '__main__':
    '''This was just used for testing'''
    yarn = '8ply'
    bump_height = 2
    bump_distance = 1
    pattern = generate_pattern(bump_height, bump_distance)
    print(pattern_to_string(pattern))
    print(pattern_to_strarray(pattern))


