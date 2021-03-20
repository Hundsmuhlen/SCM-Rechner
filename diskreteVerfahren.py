import numpy as np


def dual_ascent():
    input_array = [
        [0, 4, 6, 12, 3],
        [2, 6, 3, 4, 0],
        [4, 9, 10, 12, 8],
        [6, 0, 12, 3, 7],
        [9, 12, 0, 3, 8],
        [12, 8, 4, 0, 6]
    ]

    F = [12,6,9,9,12] # Kosten für Eröffnung
    costMatrix = input_array
    sortedCostMatrix = np.asarray(np.sort(np.array(costMatrix)))
    print(sortedCostMatrix)

    I = [i+1 for i in range(len(costMatrix))]
    vi = [[i[0] for i in sortedCostMatrix]]
    Ji = [[[row.index(i)+1] for row, i in zip(input_array, vi[0])]]
    print(I)
    print(vi)
    print(f"Ji = {Ji}")

    sj = [F]
    k = [2 for _ in range(len(vi[0]))]

    print(sj)
    print(k)
    #------------ Initialization done

    while True:
        iteration: int = 1 # Da initialisierung bereits durchgeführt wurde
        vi.append([])
        Ji.append([])

        for inde, i in enumerate(I):
            indizes = Ji[-2][i-1]


            delta_i = min([sj[-1][indi - 1] for indi in indizes])
            if delta_i == 0:
                print(f"Delta{i} = 0")
                I.pop(inde)
                if len(I) == 0:
                    break
                Ji[-1][-1] = Ji[-2][i - 1]
                vi[iteration].append(vi[iteration - 1])
                sj.append(sj[-1])
                continue
            print(f"Delta{i} = {delta_i}")
            delta = min(delta_i, sortedCostMatrix[i-1][k[i-1]] - vi[iteration-1][i-1])
            if delta == delta_i:
                print("Deltas gleich groß")
                I.pop(inde)
                if len(I) == 0:
                    break
                Ji[-1][-1] = Ji[-2][i - 1]
                vi[iteration].append(vi[iteration - 1])
                sj.append(sj[-1])
                continue
            ji_neu = costMatrix[i-1].index(sortedCostMatrix[i-1][k[i-1]])
            k[i - 1] += 1
            vi[iteration].append(vi[iteration-1] + delta)

            sj_temp = sj[-1]

            for indi in indizes:
                sj_temp[indi - 1] += delta

            sj.append(sj_temp)

            Ji[-1].append(Ji[-2][i-1])
            Ji[-1][-1].append(ji_neu)

        print(f"sj = {sj}")
        print(f"vi{iteration} = {vi}")
        print(f"Ji{iteration} = {Ji}")


        break

def greedy():
    input_array = [
        [0, 3,10,4,10,5],
        [8,0,1,10,7,6],
        [5,7,0,3,3,10],
        [2,2,5,0,2,9],
        [6,10,3,9,0,5],
        [4,1,2,1,9,0]
    ]

    fj = [8,4,5,5,3,8]  # Kosten für Eröffnung

    costMatrix = input_array
    sortedCostMatrix = np.asarray(np.sort(np.array(costMatrix)))
    print(sortedCostMatrix)

    ui = [[row[-1] for row in sortedCostMatrix]]
    print(f"ui 0 = {ui[0]}")
    delta = []
    omega = []
    round_counter = 0
    kosten = sum(ui[0])
    print(f"Anfangskosten: {kosten}")

    while True:
        delta_temp = []
        for j in range(len(costMatrix[0])):
            delta_temp_temp = []
            for i in range(len(costMatrix)):
                dtt = ui[-1][i] - costMatrix[i][j]
                delta_temp_temp.append(max(0, dtt))

            delta_temp.append(sum(delta_temp_temp))
        omega_temp = [delta_temp[i] - fj[i] for i in range(len(fj))]


        delta.append(delta_temp)
        omega.append(omega_temp)
        chosen_j = omega_temp.index(max(omega_temp))
        ui.append(
            [min(ui[-1][i],
                 costMatrix[i][chosen_j])
             for i in range(len(costMatrix))]
        )

        kosten = kosten - max(omega_temp)

        round_counter += 1

        if all([x <= 0 for x in omega_temp]):
            print("breaaak")
            break

        print(f"Folgender Standort wird eröffnet {chosen_j+1}")
        print(f"Deltaj-{round_counter}: {delta_temp}")
        print(f"Omegaj-{round_counter}: {omega_temp}")
        print(f"ui-{round_counter}: {ui[-1]}")
        print(f"neue Kosten: {kosten}")



if __name__ == "__main__":
    greedy()