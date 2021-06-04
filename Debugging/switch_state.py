write = False
if write:
    state = [0, 1, 1, 1]
    with open("enable_switch_state.txt", "w") as file:
        file.write(" ".join(str(e) for e in state))
else:
    with open("enable_switch_state.txt", "r") as file:
        data = file.read()


