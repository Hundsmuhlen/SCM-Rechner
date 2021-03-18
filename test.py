testarray = [False, False, False, False]

if not any(testarray):
    print("erfolgreich")

round_counter = 0
max_rounds = 10
d = 1
delta_nr = 0.2


while round_counter < max_rounds and d > delta_nr:
    round_counter += 1
    d = d/2
    print(f"Runde nr: {round_counter}, d = {d}")