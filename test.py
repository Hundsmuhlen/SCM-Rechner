import numpy as np

testarray = [False, False, False, False]
ta = [[7, 8, 9], [1, 2, 3], [4, 5, 6]]

if not any(testarray):
    print("erfolgreich")

t = np.matrix(testarray)
print(np.matrix(ta).T)
print(np.matrix(ta).T.T)
print(t)
print(t.T)
tt = t.T
print(tt.T)
print(ta[-1])
round_counter = 0
max_rounds = 10
d = 1
delta_nr = 0.2

dicti = {"we": 0}
if "we" in dicti:
    print("MOooooooooooooin")
print(min([0]))

while round_counter < max_rounds and d > delta_nr:
    round_counter += 1
    d = d / 2
    print(f"Runde nr: {round_counter}, d = {d}")
