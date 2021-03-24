import numpy as np


def dual_ascent(cost_array, fixcosts):
    # costMatrix = [
    #     [0, 4, 6, 12, 3],
    #     [2, 6, 3, 4, 0],
    #     [4, 9, 10, 12, 8],
    #     [6, 0, 12, 3, 7],
    #     [9, 12, 0, 3, 8],
    #     [12, 8, 4, 0, 6]
    # ]
    #
    # F = [12, 6, 9, 9, 12]  # Kosten für Eröffnung


    costMatrix = cost_array
    F = fixcosts
    sortedCostMatrix = np.asarray(np.sort(np.array(costMatrix)))
    print(sortedCostMatrix)


    I = [i + 1 for i in range(len(costMatrix))]
    vi = [[i[0] for i in sortedCostMatrix]]
    Ji = [[[row.index(i) + 1] for row, i in zip(costMatrix, vi[0])]]
    print(I)
    print(vi)
    print(f"Ji = {Ji}")

    sj = [F]
    k = [2 for _ in range(len(vi[0]))]

    print(sj)
    print(k)
    # ------------ Initialization done
    print("----------- Initialisierung abgeschlossen ----------")

    try:
        while True:
            iteration: int = 1  # Da initialisierung bereits durchgeführt wurde
            vi.append([])
            Ji.append([])


            print(f"I = {I}")
            for inde, i in enumerate(I):

                # todo platzhalter Werte eintragen
                if all([ii == 0 for ii in I]):
                    raise StopIteration

                indizes = Ji[-2][i - 1].copy()
                # print(f"JI von letzter Runde: {indizes}")
                # indizes sind alle Ji, die i in der letzten Runde schon hatte.

                # 1. Bestimme delta i - das ist da niedrigste sj für j in J
                # Ist delta i null, entferne i aus I
                delta_i = min([sj[-1][indi - 1] for indi in indizes])
                # Delta i minimiert die für alle j in Ji die sj Werte

                if delta_i == 0:
                    # eines der sj ist 0

                    Ji[-1].append(Ji[-2][inde].copy())
                    print(f"Da Delta {inde+1} NULL ist, bleibt JI gleich und zwar: {Ji[-1]}")
                    vi[-1].append(vi[-2][inde].copy())
                    sj.append(sj[-1].copy())
                    # todo macht die reihenfolge sinn?
                    I[inde] = 0
                    continue

                # Minimiere delta_i oder das k-te Kostenelement des aktuellen Kunden minus
                # sein aktuelles vi. gewinnt, das delta_i, Streiche den Kunden i aus I
                # ci_minus_vi = sortedCostMatrix[i - 1][k[i - 1] - 1] - vi[- 2][i - 1]
                vi_temp = vi[- 2][i - 1]
                ci_temp = list(filter(lambda tmp: tmp > vi_temp, costMatrix[i - 1]))
                ci_temp.sort()
                ci_minus_vi = ci_temp[0] - vi_temp
                #print(f"ci minus vi = {ci_minus_vi}")

                delta = min(delta_i, ci_minus_vi)

                #print(f"Delta = {delta}")


                vi[- 1].append(vi[- 2][i - 1].copy() + delta)

                sj_temp = sj[- 1].copy()
                # ist erstmal nur eine Kopie der letzen sj Zeile

                for indi in indizes:
                    sj_temp[indi - 1] = sj_temp[indi - 1] - delta
                    # hier werden eben die Einträge aktualisiert, die in Ji sind.


                sj.append(sj_temp)

                # todo manchmal gibt es auch mehrere Einträge mit gleichen Werten in den cij!!!!
                # diese müssen alle Ji hinzugefügt werden
                # ji_neu = [a + 1 for a in range(len(costMatrix[i - 1])) if
                #           costMatrix[i - 1][a] == sortedCostMatrix[i - 1][k[i - 1] - 1]]
                ji_neu = [a + 1 for a in range(len(costMatrix[i - 1])) if costMatrix[i - 1][a] <= vi[-1][-1]]

                #todo jetzt muss k noch auf den richtigen Stand gebracht werden. Wenn nämlich zwei cij den gleichen Wert haben ist das dann nämlcih doof



                # ji_neu = costMatrix[i - 1].index(sortedCostMatrix[i - 1][k[i - 1] - 1]) + 1
                print(f"JI_Neu: {ji_neu}")

                # todo die jis passen noch nicht so recht!!!
                Ji[-1].append([])
                for ji_n in ji_neu:
                    Ji[-1][-1].append(ji_n)
                print(f"Ji wurde in Runde {inde + 1} geupdated auf {Ji[-1]}")

                if delta == delta_i:
                    print("Deltas gleich groß")
                    I[inde] = 0
                else:
                    k[i - 1] += 1


                #todo passt das so???
                k[- 1] = len(Ji[-1][-1]) + 1

                #print(f"sj = {sj}")


            print(f"vi {iteration} = {vi}")
            print(f"Ji {iteration} = {Ji}")
            iteration = iteration + 1

    except StopIteration:
        print("-------------- Algorithmus beendet ----------")
        print(f"vi = {vi}")
        print(f"Ji = {Ji}")
        print(f"sj = {sj}")



    return vi, Ji, sj


def dual_ascent_zu_grosser_matrix(costMatrix, sj:list, vi, Ji):
    result = costMatrix
    amount_of_i = len(vi[0])

    vi_sum = [sum(v) for v in vi]
    # for v in vi_sum:
    #     vi.append(v)
    #     Ji.append("-")

    ji_vi = []
    for v, j in zip(vi, Ji):
        ji_vi.append(v)
        ji_vi.append(j)

    #ji_vi transponieren
    # ji_vi_transponiert = np.asarray(np.array(ji_vi).T)
    ji_vi_transponiert =[]

    for i in range(len(ji_vi[0])):
        col = []
        for jv in ji_vi:
            try:
                print(jv[i])
                col.append(jv[i])
            except IndexError:
                pass
        ji_vi_transponiert.append(col)

    print("Transponation - Vorher:")
    print(ji_vi)
    print("----------- Nachher ------------")
    print(ji_vi_transponiert)

    result.append(["-" for _ in range(len(costMatrix[0]))])
    for v in vi_sum:
        result[-1].append(v)
        result[-1].append("-")

    for row, row_jivi in zip(result, ji_vi_transponiert):
        row.extend(row_jivi)

    sj_trenner = ["-" for _ in range(len(sj[0]))]

    # Striche zum besseren Trennen in sj einziehen:
    sj.insert(1, sj_trenner)

    i = amount_of_i + 2
    while i < len(sj):
        sj.insert(i, sj_trenner)
        i += (amount_of_i + 1)

    result.extend(sj)
    print(result)
    return result


def greedy_zu_einer_matrix(costMatrix, fj, delta, omega, chosen_js, kostenentwicklung, ui):
    result = costMatrix
    amount_of_i = len(ui[0])
    spalte_null = ["i/j"]
    zeile_null = [i+1 for i in range(len(costMatrix[0]))]

    zeile_null.extend([f"vi-{i}" for i in range(len(ui))])
    spalte_null.extend([i+1 for i in range(len(costMatrix))])


    #ui transponieren:
    ui_transponiert = []
    for i in range(len(ui[0])):
        ui_t = []
        for row in ui:
            ui_t.append(row[i])
        ui_transponiert.append(ui_t)

    for row, row_ui in zip(result, ui_transponiert):
        row.extend(row_ui)

    result.append(["-" for _ in range(len(costMatrix[0]))])
    spalte_null.append("-")
    result.insert(0,zeile_null)

    #Die neuen Kosten an das fj hängen und die Zeile dann an result
    fj_mit_kosten = fj[:]
    fj_mit_kosten.extend(kostenentwicklung)
    result.append(fj_mit_kosten)
    spalte_null.append("fj")

    omega_mit_standort=omega
    for o, so in zip(omega_mit_standort, chosen_js):
        o.append("Gewählter Standort:")
        o.append(so)

    for d, o in zip(delta, omega_mit_standort):
        result.append(["-" for _ in range(len(o))])
        result.append(d)
        result.append(o)
        spalte_null.append("-")
        spalte_null.append("delta j")
        spalte_null.append("omega j")


    print(f"Result = {result}")
    for r, s in zip(result, spalte_null):
        r.insert(0, s)

    return result


def greedy(input_array, fj):
    # input_array2 = [
    #     [0, 15, 35, 50, 30, 20],
    #     [6, 0, 8, 14, 12, 14],
    #     [42, 24, 0, 18, 36, 48],
    #     [40, 28, 12, 0, 28, 28],
    #     [24, 24, 24, 28, 0, 8],
    #     [20, 35, 40, 35, 10, 0]
    # ]
    # # Aufgabe 14
    #
    # input_array = [
    #     [0, 3, 10, 4, 10, 5],
    #     [8, 0, 1, 10, 7, 6],
    #     [5, 7, 0, 3, 3, 10],
    #     [2, 2, 5, 0, 2, 9],
    #     [6, 10, 3, 9, 0, 5],
    #     [4, 1, 2, 1, 9, 0]
    # ]
    #
    # fj = [8, 4, 5, 5, 3, 8]  # Kosten für Eröffnung

    costMatrix = input_array
    sortedCostMatrix = np.asarray(np.sort(np.array(costMatrix)))
    print(sortedCostMatrix)

    ui = [[row[-1] for row in sortedCostMatrix]]
    print(f"ui 0 = {ui[0]}")
    delta = []
    omega = []
    chosen_js = []
    kostenentwicklung = []
    round_counter = 0
    kosten = sum(ui[0])
    kostenentwicklung.append(kosten)
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
        chosen_js.append(chosen_j + 1)
        ui.append(
            [min(ui[-1][i],
                 costMatrix[i][chosen_j])
             for i in range(len(costMatrix))]
        )

        kosten = kosten - max(omega_temp)
        kostenentwicklung.append(kosten)

        round_counter += 1

        if all([x <= 0 for x in omega_temp]):
            print("breaaak")
            break

        print(f"Folgender Standort wird eröffnet {chosen_j + 1}")
        print(f"Deltaj-{round_counter}: {delta_temp}")
        print(f"Omegaj-{round_counter}: {omega_temp}")
        print(f"ui-{round_counter}: {ui[-1]}")
        print(f"neue Kosten: {kosten}")

    return delta, omega, chosen_js, kostenentwicklung, ui

if __name__ == "__main__":
    greedy(1,2)
