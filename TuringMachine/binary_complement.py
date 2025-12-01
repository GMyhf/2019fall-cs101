from turing_machine import TuringMachine

final_states = {"final"}

transition_function = {
    ("init","0"):("1", "R", "init"),
    ("init","1"):("0", "R", "init"),
    ("init"," "):(" ", "N", "final"),
}

t = TuringMachine(
        tape="010011001",
        initial_state="init",
        final_states=final_states,
        transition_function=transition_function)

print("Input on Tape:\n" + t.get_tape())

while not t.final():
    t.step()

print("Result of the Turing machine calculation:")
print(t.get_tape())
