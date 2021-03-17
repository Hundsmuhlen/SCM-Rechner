from flask import Flask, render_template, request, redirect
from ScmTest2 import l2metrik, l8metrik, l22metrik, l1metrik, domKrit, schwerpunkt
import numpy as np
import re
from itertools import combinations
from flask import send_from_directory
import os


app = Flask(__name__)


class state():
    dimensions = 0
    dimensions_set = False
    amount_2d_points = 0



@app.route("/")
def home():
    return render_template("new_index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon2.ico')

@app.route("/median-settings", methods=["GET","POST"])
def median_settings():
    if request.method == "GET":
        return render_template("median_settings.html")
    if request.method == "POST":
        try:
            state.amount_2d_points = int(request.form.get("nr_of_points"))
        except ValueError:
            return render_template("median-error.html", message="Du musst eine positive Anzahl an Punkten eingeben!")
        return render_template("median-input.html", dimensions=state.amount_2d_points)

@app.route("/median-input", methods=["GET","POST"])
def median_input():
    """
    Hier werden Schwerpunkt, verschärftes Dominanzkriterium und ein paar weiszfeld iterationen berechnet
    dabei greifen wir auch auf den state zurück mit den 2d-points. Sind ja hier auch wieder 2d Punkte
    :return:
    """
    if request.method == "POST":
        weights = []
        punkte = []
        dominanzkriterium = []
        fulfilled = []
        sp = None
        delta = None
        weiszfeld_results = []

        for i in range(state.amount_2d_points):
            weights.append(float(request.form.get(f"w{i+1}")))
        print(weights)

        for i in range(state.amount_2d_points):
            x = float(request.form[f"x{i+1}"])
            y = float(request.form[f"y{i+1}"])
            punkte.append(np.array([x, y]))

        for ind, aj in enumerate(punkte):
            points = [e for indi, e in enumerate(punkte) if indi != ind]
            gewichte = weights[:]  # fastest way to copy
            gewichte.pop(ind)
            dk = domKrit(gewichte, points, aj)
            print(dk)
            print(points)
            print(gewichte)
            dominanzkriterium.append(round(dk, 4))

        for d, w in zip(dominanzkriterium,weights):
            if d <= w:
                fulfilled.append(True)
            else:
                fulfilled.append(False)
        sp = schwerpunkt(weights=weights, punkte=punkte)

        #Platz für den Weizfeld
        if all(fulfilled) == False:
            pass



        return render_template("median-results.html",
                               schwerpunkt=sp,
                               weights=weights,
                               punkte=punkte,
                               gamma=dominanzkriterium,
                               fulfilled=fulfilled,
                               punktezahl=state.amount_2d_points)

@app.route("/metriken-multi-settings", methods=["GET", "POST"])
def metriken_multiple_points_settings():
    if request.method == "GET":
        return render_template("metriken_multi_settings.html")
    if request.method == "POST":
        try:
            state.amount_2d_points = int(request.form.get("nr_of_points"))
        except ValueError:
            return render_template("metriken_multi_error.html", message="Du musst eine positive Anzahl an Punkten eingeben!")
        return render_template("metriken_multi_input.html", dimensions=state.amount_2d_points)

@app.route("/metriken-multi-input", methods=["POST"])
def metriken_multi_points_input():
    points = []
    two = []
    rows = []

    for i in range(state.amount_2d_points):
        try:
            x = float(request.form.get(f"x{i + 1}"))
            y = float(request.form.get(f"y{i + 1}"))
            print(f"x = {x}, y = {y}")
            points.append(np.array([x, y]))
        except ValueError:
            return render_template("mp_und_radius_error.html", message="Du musst für alle Punkte Werte eigeben.\n"
                                                                       "Verwende Punkte statt Kommas! - ValueError")
        except TypeError:
            return render_template("mp_und_radius_error.html", message="Du musst für alle Punkte Werte eigeben.\n"
                                                                       "Verwende Punkte statt Kommas! - TypeError")
    two = [i for i in combinations(points, 2)]

    for combi in two:
        row = []
        row.append(np.asarray(combi))
        p1 = combi[0]
        p2 = combi[1]

        l1 = round(l1metrik(p1, p2), 4)
        l2 = round(l2metrik(p1, p2), 4)
        l22 = round(l22metrik(p1, p2), 4)
        l8 = round(l8metrik(p1, p2), 4)

        print(f"l1 {l1}, l2 {l2}, l22 {l22}, l8 {l8}")


        row.append(l1)
        row.append(l2)
        row.append(l22)
        row.append(l8)

        rows.append(row)

    return render_template("metriken_multi_results.html", rows=rows)


@app.route("/metriken-dimensions", methods=["GET"])
def metriken_dimensions():
    return render_template("metriken_settings.html")


@app.route("/metriken-settings", methods=["POST", "GET"])
def metriken():
    if request.method == "POST":
        try:
            dimensions = int(request.form.get("dimensions"))
        except ValueError:
            return render_template("metriken_error.html", message="You have to enter the wanted dimensions!")
        if dimensions < 1 or dimensions == None:
            return render_template("metriken_error.html", message="Have to have more than 0 dimensions!")
        else:
            state.dimensions = dimensions
            return render_template("metriken_input.html", dimensions=dimensions)


@app.route("/metriken-results", methods=["POST", "GET"])
def metriken_results():
    if request.method == "POST":
        l1 = []
        l2 = []
        for i in range(state.dimensions):
            try:
                l1.append(float(request.form.get(f"a1{i}")))
            except ValueError:
                return render_template("metriken_error.html", message=f"Fehler in Spalte 1, Zeile {i + 1}!")
            except TypeError:
                return render_template("metriken_error.html", message=f"Fehler in Spalte 1, Zeile {i + 1}!")
            try:
                l2.append(float(request.form.get(f"a2{i}")))
            except ValueError:
                return render_template("metriken_error.html", message=f"Fehler in Spalte 2, Zeile {i + 1}!")
            except TypeError:
                return render_template("metriken_error.html", message=f"Fehler in Spalte 2, Zeile {i + 1}!")
        p1 = np.array(l1)
        p2 = np.array(l2)

        return render_template("metriken_results.html",
                               l22metrik=round(l22metrik(p1, p2), 4),
                               l2metrik=round(l2metrik(p1, p2), 4),
                               l1metrik=round(l1metrik(p1, p2), 4),
                               l8metrik=round(l8metrik(p1, p2), 4)
                               )


@app.route("/mittelpunkt-und-radius", methods=["POST", "GET"])
def mp_und_rad():
    if request.method == "GET":
        return render_template("mp_und_radius_settings.html")
    if request.method == "POST":
        try:
            state.amount_2d_points = int(request.form.get("nr_of_points"))
        except ValueError:
            return render_template("mp_und_radius_error.html", message="Du musst eine positive Anzahl an Punkten eingeben!")
        return render_template("mp_und_radius_input.html", dimensions=state.amount_2d_points)


@app.route("/mp-und-radius-input", methods=["POST", "GET"])
def mp_und_radius_input():
    from ScmTest3 import mittelpunkt_und_radius, mittelsenkrechte, mittelpunkt, schnittpunkt_ms, \
        punkt_im_radius, mp_und_radius_drei_auf_gleicher_achse
    from itertools import combinations

    if request.method == "POST":
        points = []
        two: tuple = []
        three: tuple = []
        rows = []
        minimal_überdeckender_kreis = None

        for i in range(state.amount_2d_points):
            try:
                x = float(request.form.get(f"x{i + 1}"))
                y = float(request.form.get(f"y{i + 1}"))
                print(f"x = {x}, y = {y}")
                points.append(np.array([x, y]))
            except ValueError:
                return render_template("mp_und_radius_error.html", message="Du musst für alle Punkte Werte eigeben.\n"
                                                                           "Verwende Punkte statt Kommas! - ValueError")
            except TypeError:
                return render_template("mp_und_radius_error.html", message="Du musst für alle Punkte Werte eigeben.\n"
                                                                           "Verwende Punkte statt Kommas! - TypeError")

        two = [i for i in combinations(points, 2)]
        print(f"Zweierkombinationen = {two}")
        three = [i for i in combinations(points, 3)]
        print(f"Dreierkombis = {three}")
        # if there are less than 3 given points the three array stays empty

        column_names = [point for point in points]
        column_names.insert(0, "Radius")
        column_names.insert(0, "Mittelpunkt")
        column_names.insert(0, "Punkte")
        rows.append(column_names)

        for combi in two:
            # erzeugt für jede zweier Kombination einen Kreis dazwischen und überprüft, welche Punkte darin liegen
            row = [np.asarray(combi)]
            mp, radius = mittelpunkt_und_radius(combi[0], combi[1])
            row.append(np.round(mp,4))
            row.append(round(radius,4))

            for point in points:
                row.append(punkt_im_radius(mp, radius, point))
            rows.append(row)

        for combi in three:
            # erstellt für jede 3er Kombination einen MÜK und checkt, welche Punkte drin liegen
            row = [np.asarray(combi)]
            mp = 0
            radius = 0
            a, b, c = combi[0], combi[1], combi[2]
            mi1 = bi1 = mi2 = bi2 = x = y = None

            #------------
            try:
                #Testen ob es eine Mittelsenkrecht gibt, oder ob beide Werte auf gleicher Höhe liegen
                mi1, bi1 = mittelsenkrechte(a, b)
                mi2, bi2 = mittelsenkrechte(a, c)
            except ValueError:
                print("2 Punkte auf gleicher Höhe")
                try:
                    mi1, bi1 = mittelsenkrechte(a, c)
                    mi2, bi2 = mittelsenkrechte(b, c)
                except ValueError:
                    try:
                        mi1, bi1 = mittelsenkrechte(a, b)
                        mi2, bi2 = mittelsenkrechte(b, c)
                    except ValueError:
                        print("Alle 3 Punkte liegen auf der gleichen Achse")
                        mp, radius = mp_und_radius_drei_auf_gleicher_achse(a, b, c)


            try:
                #Testen ob es einen Schnittpunkt gibt
                if radius == 0:
                    print(f"{mi1} -- {bi1} -- {mi2} -- {bi2}")
                    x, y = schnittpunkt_ms(mi1, bi1, mi2, bi2)
                    mp = np.array([x, y])
                    radius = l2metrik(mp, a)
            except ValueError:
                #Es gibt keinen Schnittpunkt der Achsen -> die Punkte liegen alle auf einer Achse
                mp, radius = mp_und_radius_drei_auf_gleicher_achse(a,b,c)
            #---------------
            # if a[1] == b[1] == c[1]:
            #     possible_points = []
            #     possible_points.append(mittelpunkt_und_radius(a, b))
            #     possible_points.append(mittelpunkt_und_radius(a, c))
            #     possible_points.append(mittelpunkt_und_radius(b, c))
            #     mp, radius = max(possible_points, key=lambda item: item[1])
            #
            # mi1, bi1 = mittelsenkrechte(a, b)
            # mi2, bi2 = mittelsenkrechte(a, c)
            # x, y = schnittpunkt_ms(mi1, bi1, mi2, bi2)
            # mp = np.array([x, y])
            # radius = l2metrik(mp, a)

            row.append(np.round(mp,4))
            row.append(round(radius,4))
            for point in points:
                row.append(punkt_im_radius(mp, radius, point))
            rows.append(row)

        for ind, row in enumerate(rows):
            # Check mal ab, was da so rauskommt
            #print(f"ROWS : {row}")
            try:
                print(row)
                if all(row[3:]) and minimal_überdeckender_kreis == None:
                    minimal_überdeckender_kreis = ind
                    print(f"MÜK bei index: {minimal_überdeckender_kreis}")
            except ValueError:
                #print("ValueError bei Checken der Ergebnisse")
                pass
        return render_template("mp_und_radius_results.html", rows=rows, muek=minimal_überdeckender_kreis)


@app.route("/impressum", methods=["GET"])
def impressum():
    return render_template("impressum.html")


if __name__ == "__main__":
    app.run()
