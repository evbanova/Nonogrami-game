import unittest
from unittest.mock import MagicMock, patch
import sqlite3
import random
import tkinter as tk
import sys
sys.path.append('C:\\Users\\evaba\\Documents\\uni\\Python\\Nonogrami_version3\\Nonogrami_version3\\')

#importing the function of the game to be tested
import Nonogrami_version3
from Nonogrami_version3 import puzzle_convert, get_puzzle, count_filled_cells, calculate_clues, calculate_clues, white_matrix_0, on_cell_click_0, make_matrix, exit_game, click_to_fill, make_drawing, save_drawing, clean_drawing

class TestNonogramiFunctions(unittest.TestCase):

    #making a database and window for testing
    @patch('Nonogrami_version3.hearts', 5)
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE puzzles (id INTEGER PRIMARY KEY, size INTEGER, matrix TEXT)''')
        self.cursor.execute('''CREATE TABLE guessed_puzzles (id INTEGER PRIMARY KEY, size INTEGER, matrix TEXT)''')
        self.conn.commit()
        self.test_root = tk.Toplevel()
        self.size = 5 
        self.canvas = tk.Canvas(self.test_root)
        self.canvas.pack()


    #making sure we close the database and the window after testing
    def tearDown(self):
        self.conn.close()
        self.test_root.destroy()

    def test_puzzle_convert(self):
        matrix_str = '110011000'
        expected_matrix = [[1, 1, 0], [0, 1, 1], [0, 0, 0]]
        self.assertEqual(puzzle_convert(matrix_str, 3), expected_matrix)

    def test_count_filled_cells(self):
        matrix = [[1, 0, 1], [0, 1, 0], [1, 1, 1]]
        self.assertEqual(count_filled_cells(matrix), 6)

    def test_calculate_clues(self):
        matrix = [[1, 0, 1], [1, 1, 0], [0, 1, 1]]
        expected_row_clues = [[1, 1], [2], [2]]
        expected_col_clues = [[2], [2], [1, 1]]
        row_clues, col_clues = calculate_clues(matrix)
        self.assertEqual(row_clues, expected_row_clues)
        self.assertEqual(col_clues, expected_col_clues)

    def test_white_matrix_0(self):
        white_matrix_0(self.size, self.canvas)
        self.assertEqual(Nonogrami_version3.hearts, 5)
        self.assertEqual(Nonogrami_version3.player_count, 0)
        self.assertEqual(len(Nonogrami_version3.guessed_cells), 0)

    def test_on_cell_click_correct_guess(self):
        matrix = [[1] * self.size for i in range(self.size)]
        event = MagicMock(x=300, y=300)
        on_cell_click_0(event, 400/(self.size + 2), matrix, self.canvas, self.size, self.size*self.size, 1) 
        self.assertGreater(Nonogrami_version3.player_count, 0)

    def test_on_cell_click_wrong_guess(self):
        matrix = [[0] * self.size for i in range(self.size)]
        event = MagicMock(x=300, y=300)
        on_cell_click_0(event, 400/(self.size + 2), matrix, self.canvas, self.size, self.size*self.size, 1)   
        self.assertLess(Nonogrami_version3.hearts, 5)

    @patch('Nonogrami_version3.show_frame')
    def test_make_drawing(self, mock_show_frame):
        make_drawing(self.canvas, self.size)
        self.assertEqual(len(Nonogrami_version3.drawing_matrix), self.size)

    @patch('sqlite3.connect')
    def test_save_drawing(self, mock_connect):
        mock_cursor = mock_connect.return_value.cursor.return_value
        save_drawing(MagicMock())
        mock_cursor.execute.assert_called_once()


if __name__ == '__main__':
    unittest.main()
