# ref: https://www.python-course.eu/turing_machine.php
class Tape:
    blank_symbol = " "

    def __init__(self, tape_string=""):
        self.__tape = dict((enumerate(tape_string)))

    def __str__(self):
        s = ""
        min_used_index = min(self.__tape.keys())
        max_used_index = max(self.__tape.keys())
        for i in range(min_used_index, max_used_index + 1):
            s += self.__tape[i]
        return s

    def __getitem__(self, index):
        return self.__tape.get(index, Tape.blank_symbol)

    def __setitem__(self, pos, char):
        self.__tape[pos] = char


class TuringMachine:

    def __init__(self,
                 tape="",
                 blank_symbol=" ",
                 initial_state="",
                 final_states=None,
                 transition_function=None):
        self.__tape = Tape(tape)
        self.__head_position = 0
        self.__blank_symbol = blank_symbol
        self.__current_state = initial_state
        self.__transition_function = transition_function or {}

        self.__final_states = set(final_states) if final_states else set()

    def get_tape(self):
        return str(self.__tape)

    def step(self):
        char_under_head = self.__tape[self.__head_position]
        x = (self.__current_state, char_under_head)
        if x in self.__transition_function:
            write_char, move, next_state = self.__transition_function[x]
            self.__tape[self.__head_position] = write_char

            if move == "R":
                self.__head_position += 1
            elif move == "L":
                self.__head_position -= 1

            self.__current_state = next_state

    def final(self):
        return self.__current_state in self.__final_states
