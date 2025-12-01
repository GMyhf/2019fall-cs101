from turing_machine import TuringMachine

final_states = {"final"}

transition_function = {
    ("q1", "1"): ("1", "R", "q1"),
    ("q1", " "): ("1", "R", "q2"),
    ("q2", "1"): ("1", "R", "q2"),
    ("q2", " "): (" ", "L", "q3"),
    ("q3", "1"): (" ", "N", "q3"),
    ("q3", " "): (" ", "N", "final")
}

t = TuringMachine(
    tape="1111 111 ",
    initial_state="q1",
    final_states=final_states,
    transition_function=transition_function)

print("Input on Tape:\n" + t.get_tape())

while not t.final():
    t.step()

print("Result of the Turing machine calculation:")
print(t.get_tape())
