import tkinter as tk
import sqlite3
import random



#Creating the database
conn = sqlite3.connect('nonogrami_database.db')
cursor = conn.cursor()

cursor.execute(''' CREATE TABLE IF NOT EXISTS puzzles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    size INTEGER NOT NULL,
                    matrix TEXT NOT NULL ) ''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS guessed_puzzles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    size INTEGER NOT NULL,
                    matrix TEXT NOT NULL ) ''')


#Inserting random puzzles as data in the table
matrix_5x5 = '0011101001001101111011111'
matrix_10x10 = '1111110011001011100000000000011100011010101111111100000001110000000110000111111100000000000111000011'
matrix_15x15 = '001110000000000101000000000000110000000000000011000000000000000011111100001000011111100001111110001000000000000111000000000000011000000000111010000000000111010000000000111111100000000000011100000000000011000000000000010000000'
cursor.execute(''' INSERT INTO puzzles (size, matrix) VALUES (?, ?) ''', (5, matrix_5x5))
cursor.execute(''' INSERT INTO puzzles (size, matrix) VALUES (?, ?) ''', (10, matrix_10x10))
cursor.execute(''' INSERT INTO puzzles (size, matrix) VALUES (?, ?) ''', (15, matrix_15x15))

conn.commit()



#Creating the user interface
root = tk.Tk();
root.title('Nonogrami Game')
root.geometry('500x500')



# Create  frames
frame0 = tk.Frame(root, bg='lightpink')
frame1 = tk.Frame(root, bg='lightblue')
frame2 = tk.Frame(root, bg='lightpink')
frame3 = tk.Frame(root, bg='lightpink')
frame_grid5 = tk.Frame(root, bg='lightblue')
frame_grid10 = tk.Frame(root, bg='lightblue')
frame_grid15 = tk.Frame(root, bg='lightblue')
frame1_2 = tk.Frame(root, bg='lightblue')
frame_grid5_2 = tk.Frame(root, bg='lightblue')
frame_grid10_2 = tk.Frame(root, bg='lightblue')
frame_grid15_2 = tk.Frame(root, bg='lightblue')

# Place frames in the same location
for frame in (frame0, frame1, frame2, frame3, frame_grid5, frame_grid10, frame_grid15, frame1_2, frame_grid5_2, frame_grid10_2, frame_grid15_2):
    frame.grid(row=0, column=0, sticky='nsew')

# Function to show a specific frame
def show_frame(frame):
    frame.tkraise()



#Create frame0 things
label_entry = tk.Label(frame0, text='NONOGRAMI GAME \n Enjoy! \n', pady=100, padx=20, bg='lightpink')
button_new_game = tk.Button(frame0, text='New game', width=15, height=2, command=lambda: show_frame(frame1),  bg='pale violet red')
button_make_painting = tk.Button(frame0, text='Make painting', width=15, height=2, command=lambda: show_frame(frame1_2), bg='pale violet red')

#Place frame0 things
label_entry.grid(row=1, column=1)
button_new_game.grid(row=2, column=1, padx=180, pady=5)
button_make_painting.grid(row=4, column=1, padx=180, pady=5)



#Create frame1 things
label_choose = tk.Label(frame1, text='Choose the size of the \n matrix you want to play on \n', pady=100, bg='lightblue')
button_grid5 = tk.Button(frame1, text='5x5\nEasy', width=8, height=3, command=lambda: show_frame(frame_grid5), bg='sky blue')
button_grid10 = tk.Button(frame1, text='10x10\nMedium', width=8, height=3, command=lambda: show_frame(frame_grid10), bg='sky blue')
button_grid15 = tk.Button(frame1, text='15x15\nHard', width=8, height=3, command=lambda: show_frame(frame_grid15),  bg='sky blue')
button_home = tk.Button(frame1, text='Home', width=8, height=1, command=lambda: show_frame(frame0),  bg='sky blue')

#Place frame1 things
label_choose.grid(row=0, column=1)
button_grid5.grid(row=1, column=0, padx=40)
button_grid10.grid(row=1, column=1)
button_grid15.grid(row=1, column=2, padx=40)
button_home.grid(row=2, column=1, pady=90)



#Create frame1_2 things
label_choose_2 = tk.Label(frame1_2, text='Choose the size of the \n matrix you want to draw on \n', pady=100, bg='lightblue')
button_grid5_2 = tk.Button(frame1_2, text='5x5\nEasy', width=8, height=3, command=lambda: show_frame(frame_grid5_2), bg='sky blue')
button_grid10_2 = tk.Button(frame1_2, text='10x10\nMedium', width=8, height=3, command=lambda: show_frame(frame_grid10_2), bg='sky blue')
button_grid15_2 = tk.Button(frame1_2, text='15x15\nHard', width=8, height=3, command=lambda: show_frame(frame_grid15_2),  bg='sky blue')
button_home_2 = tk.Button(frame1_2, text='Home', width=8, height=1, command=lambda: show_frame(frame0),  bg='sky blue')

#Place frame1_2 things
label_choose_2.grid(row=0, column=1)
button_grid5_2.grid(row=1, column=0, padx=40)
button_grid10_2.grid(row=1, column=1)
button_grid15_2.grid(row=1, column=2, padx=40)
button_home_2.grid(row=2, column=1, pady=90)



#Create frame2 things
label_lost = tk.Label(frame2, text='You lost! \n Try again! \n', padx=200, pady=150, bg='light pink')
button_home_lost = tk.Button(frame2, text='Home', width=8, height=1, command=lambda: show_frame(frame0),  bg='pale violet red')

#Place frame2 things
label_lost.grid(row=0, column=0)
button_home_lost.grid(row=1, column=0, pady=50)



#Create frame3 things
label_lost = tk.Label(frame3, text='You won! \n Bravo! \n', padx=200, pady=150, bg='light pink')
button_home_won = tk.Button(frame3, text='Home', width=8, height=1, command=lambda: show_frame(frame0),  bg='pale violet red')

#Place frame things
label_lost.grid(row=0, column=0)
button_home_won.grid(row=1, column=0, pady=50)



#creating some variables used in multiple frames
hearts = 5
player_count = 0
guessed_cells = set()
drawing_matrix = []


#creating matrixes for frame_grid5, frame_gird10, frame_grid15 in the following functions

#Converting the gotten puzzle from the database into a list of list for easier use in the main game logic
def puzzle_convert(chosen_puzzle, size):
    matrix = []
    for i in range(0, len(chosen_puzzle), size):
        row = list(map(int, chosen_puzzle[i:i+size]))
        matrix.append(row)
    return matrix


#get puzzle from database
def get_puzzle(size):
    conn = sqlite3.connect('nonogrami_database.db')
    cursor = conn.cursor()
    cursor.execute(''' SELECT id, matrix FROM puzzles WHERE size = ?''', (size,))
    result = cursor.fetchall()
    if not result:
        raise ValueError("No puzzles found for the given size.")
    # Choose a random puzzle from the result
    r_chosen_puzzle = random.choice(result)
    chosen_puzzle = r_chosen_puzzle[1]
    chosen_puzzle_id = r_chosen_puzzle[0]
    chosen_puzzle = puzzle_convert(chosen_puzzle, size)
    conn.commit()
    return (chosen_puzzle, chosen_puzzle_id)

#moving a puzzle that the player has solved in the guessed puzzles table
def move_puzzle(puzzle_id):
    conn = sqlite3.connect('nonogrami_database.db')
    cursor.execute(''' INSERT INTO guessed_puzzles (size, matrix) SELECT size, matrix FROM puzzles WHERE id = ?''', (puzzle_id,))
    cursor.execute(''' DELETE FROM puzzles WHERE id = ?''', (puzzle_id,))
    conn.commit()



#finding the count of correct cells (used in winning logic)
def count_filled_cells(matrix):
    count = 0
    for row in matrix:
        count += row.count(1)
    return count

#calculatin the clues of a certain painting
def get_clues_from_line(line):
    clues = []
    count = 0
    for cell in line:
        if cell == 1:
            count += 1
        else:
            if count > 0:
                clues.append(count)
                count = 0
    if count > 0:
        clues.append(count)
    return clues

def calculate_clues(matrix):
    row_clues = []
    for row in matrix:
        clues = []
        count = 0
        for cell in row:
            if cell == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        row_clues.append(clues if clues else [0])

    col_clues = []
    for col in range(len(matrix[0])):
        clues = []
        count = 0
        for row in matrix:
            if row[col] == 1:
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        col_clues.append(clues if clues else [0])

    return row_clues, col_clues


#when creating an matrix, or exiting game restarting the canvas and hearts 
def white_matrix_0(size, canvas):
    cell_size= 400/(size + 2)
    for i in range(size):
        for j in range(size):
            x1 = cell_size*2 + j*cell_size
            y1 = cell_size*2 + i*cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill='sky blue')
    global hearts, player_count, guessed_cells
    hearts = 5
    player_count = 0
    guessed_cells.clear()

def white_matrix(size, canvas, label_hearts):
    white_matrix_0(size, canvas)
    label_hearts.config(text=f'Hearts left: {hearts}')


#the main play; what happens everytime we click on a cell on any canvas
def on_cell_click_0(event, cell_size, matrix, canvas, size, original_count, puzzle_id):
    global hearts, player_count, guessed_cells
    col = (event.x - cell_size * 2) // cell_size
    row = (event.y - cell_size * 2) // cell_size

    #do the checking if its a correct cell in the painting
    cell_coordinates = (int(row), int(col))
    if matrix[int(row)][int(col)] and cell_coordinates not in guessed_cells:
        canvas.create_rectangle(cell_size*2 + col*cell_size, cell_size*2 + row*cell_size, 
                                cell_size*2 + (col+1)*cell_size, cell_size*2 + (row+1)*cell_size, fill='dark blue')
        player_count += 1
        guessed_cells.add(cell_coordinates)
    else:
        hearts = hearts - 1
        x_center = cell_size*2 + col*cell_size + cell_size//2
        y_center = cell_size*2 + row*cell_size + cell_size//2
        canvas.create_text(x_center, y_center, text='X', font=('Arial', int(cell_size//2)), fill='dark blue')

def on_cell_click(event, cell_size, matrix, canvas, size, original_count, puzzle_id):
    on_cell_click_0(event, cell_size, matrix, canvas, size, original_count, puzzle_id)
    if canvas == canvas1:
        label_hearts = label_hearts1
    elif canvas == canvas2:
        label_hearts = label_hearts2
    else:
        label_hearts = label_hearts3
    label_hearts.config(text=f'Hearts left: {hearts}')

    if hearts == 0:
        show_frame(frame2)
        white_matrix(size, canvas, label_hearts)
    if player_count == original_count:
        show_frame(frame3)
        white_matrix(size, canvas, label_hearts)
        move_puzzle(puzzle_id)
        

#generating a canvas from a puzzle - array of arrays of 0s and 1s
def make_matrix(canvas, size, matrix, puzzle_id):
    original_count = count_filled_cells(matrix)

    cell_size= 400/(size + 2)
    row_clues, col_clues = calculate_clues(matrix)

    for col, clues in enumerate(col_clues):
        clue_text = "\n".join(map(str, clues))
        x = cell_size*2 + col*cell_size+ cell_size//2
        y = cell_size
        canvas.create_text(x, y, text=clue_text, font=('Arial', 10))

    for row, clues in enumerate(row_clues):
        clue_text = " ".join(map(str, clues))
        x = cell_size
        y = cell_size*2 + row*cell_size+ cell_size//2
        canvas.create_text(x, y, text=clue_text, font=('Arial', 10))

    if canvas == canvas1:
            label_hearts = label_hearts1
    elif canvas == canvas2:
            label_hearts = label_hearts2
    else:
            label_hearts = label_hearts3
    white_matrix(size, canvas, label_hearts)
    canvas.bind('<Button-1>', lambda event: on_cell_click(event, cell_size, matrix, canvas, size, original_count, puzzle_id))


#the function that exits the game when clicked 'Home' and restarting
def exit_game(size, canvas, label_hearts):
    white_matrix(size, canvas, label_hearts)
    show_frame(frame0)



#creating a drawing, saving it in the database and all other needed functions for 'Make painting' interface

#filling a cell when drawing
def click_to_fill(event, cell_size, canvas, size):
    global drawing_matrix
    col = event.x // cell_size
    row = event.y // cell_size
    drawing_matrix[int(row)][int(col)] = 1
    x1 = col * cell_size
    y1 = row * cell_size
    x2 = x1 + cell_size
    y2 = y1 + cell_size
    canvas.create_rectangle(x1, y1, x2, y2, fill='dark blue')

#displaying a clean matrix ready for drawing
def make_drawing(canvas, size):
    global drawing_matrix
    cell_size= 400/size
    clean_drawing(size, canvas)
    drawing_matrix = [[0 for i in range(size)] for j in range(size)]
    canvas.bind('<Button-1>', lambda event: click_to_fill(event, cell_size, canvas, size))


#saving a drawing on a canvas in the database
def save_drawing(frame):
    global drawing_matrix
    matrix_str = ''.join(str(cell) for row in drawing_matrix for cell in row)
    size = len(drawing_matrix)  
    conn = sqlite3.connect('nonogrami_database.db')  
    cursor = conn.cursor()
    cursor.execute(''' INSERT INTO puzzles (size, matrix) VALUES (?, ?) ''', (size, matrix_str))
    conn.commit()
    label_saved = tk.Label(frame, text='Successfully saved!',pady=10, padx=50, bg='lightpink')
    label_saved.grid(row=0, column=0)

#cleaning the matrix after drawing
def clean_drawing(size, canvas):
    cell_size= 400/size
    for i in range(size):
        for j in range(size):
            x1 = j*cell_size
            y1 = i*cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            canvas.create_rectangle(x1, y1, x2, y2, fill='sky blue')
    show_frame(frame0)





#Create frame_grid5 things
label_hearts1 = tk.Label(frame_grid5, text=f'Hearts left: {hearts}', bg='lightblue')
button_home1 = tk.Button(frame_grid5, text='Exit game', command=lambda: exit_game(5, canvas1, label_hearts1), bg='sky blue')
canvas1 = tk.Canvas(frame_grid5, width=400, height=400, bg='light blue')
(puzzle1, puzzle_id1) = get_puzzle(5)
make_matrix(canvas1, 5, puzzle1, puzzle_id1)

#Place frame_grid5 things
canvas1.grid(row=1, column=0, padx=45, pady=10)
button_home1.grid(row=2, column=0, pady=10)
label_hearts1.grid(row=0, column=0)



#Create frame_grid10 things
label_hearts2 = tk.Label(frame_grid10, text=f'Hearts left: {hearts}', bg='lightblue')
button_home2 = tk.Button(frame_grid10, text='Exit game', command=lambda: exit_game(10, canvas2, label_hearts2), bg='sky blue')
canvas2 = tk.Canvas(frame_grid10, width=400, height=400, bg='light blue')
(puzzle2, puzzle_id2) = get_puzzle(10)
make_matrix(canvas2, 10, puzzle2, puzzle_id2)

#Place frame_grid10 things
canvas2.grid(row=1, column=0, padx=45, pady=10)
button_home2.grid(row=2, column=0, pady=10)
label_hearts2.grid(row=0, column=0)



#Create frame_grid15 things
label_hearts3 = tk.Label(frame_grid15, text=f'Hearts left: {hearts}', bg='lightblue')
button_home3 = tk.Button(frame_grid15, text='Exit game', command=lambda: exit_game(15, canvas3, label_hearts3), bg='sky blue')
canvas3 = tk.Canvas(frame_grid15, width=400, height=400, bg='light blue')
(puzzle3, puzzle_id3) = get_puzzle(15)
make_matrix(canvas3, 15, puzzle3, puzzle_id3)

#Place frame_grid15 things
canvas3.grid(row=1, column=0, padx=45, pady=10)
button_home3.grid(row=2, column=0, pady=10)
label_hearts3.grid(row=0, column=0)



#Create frame_grid5_2 things
canvas4 = tk.Canvas(frame_grid5_2, width=400, height=400, bg='light blue')
button_home4 = tk.Button(frame_grid5_2, text='Home', command=lambda: clean_drawing(5, canvas4), bg='sky blue')
button_save1 = tk.Button(frame_grid5_2, text='Save', command=lambda: save_drawing(frame_grid5_2), bg='sky blue')
make_drawing(canvas4, 5)

#Place frame_grid5_2 things
canvas4.grid(row=1, column=0, padx=45)
button_home4.grid(row=2, column=0, pady=5)
button_save1.grid(row=0, column=0, pady=5)



#Create frame_grid10_2 things
canvas5 = tk.Canvas(frame_grid10_2, width=400, height=400, bg='light blue')
button_home5 = tk.Button(frame_grid10_2, text='Home', command=lambda: clean_drawing(10, canvas5), bg='sky blue')
button_save2 = tk.Button(frame_grid10_2, text='Save', command=lambda: save_drawing(frame_grid10_2), bg='sky blue')
make_drawing(canvas5, 10)

#Place frame_grid10_2 things
canvas5.grid(row=1, column=0, padx=45)
button_home5.grid(row=2, column=0, pady=5)
button_save2.grid(row=0, column=0, pady=5)



#Create frame_grid15_2 things
canvas6 = tk.Canvas(frame_grid15_2, width=400, height=400, bg='light blue')
button_home6 = tk.Button(frame_grid15_2, text='Home', command=lambda: clean_drawing(15, canvas6), bg='sky blue')
button_save3 = tk.Button(frame_grid15_2, text='Save', command=lambda: save_drawing(frame_grid15_2), bg='sky blue')
make_drawing(canvas6, 15)

#Place frame_grid15_2 things
canvas6.grid(row=1, column=0, padx=45)
button_home6.grid(row=2, column=0, pady=5)
button_save3.grid(row=0, column=0, pady=5)



# Show the initial frame
show_frame(frame0)


# Make the window layout expandable
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()

