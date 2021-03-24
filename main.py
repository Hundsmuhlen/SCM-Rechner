from flask import Flask, render_template, request, redirect, session
from ScmTest2 import l2metrik, l8metrik, l22metrik, l1metrik, domKrit, schwerpunkt, entfernung, delta, weiszfeld, \
    l8_center_gewichtet_eindimensional, l1_zu_l8_transformation, l8_center_ungewichtet, l8_zu_l1_transformation
from ScmTest3 import matrix_from_weights_vector
from diskreteVerfahren import greedy, dual_ascent, dual_ascent_zu_grosser_matrix, greedy_zu_einer_matrix
import numpy as np
import re
from itertools import combinations
from flask import send_from_directory
import os
import copy


app = Flask(__name__)
# Hier sollte eigentlich eine geheime Phrase stehen. Ich hab einfach mal das absurdeste genommen, was mir eingefallen ist
app.secret_key = "SCMistTollundmachtSpass"


@app.route("/")
def home():
    return render_template("new_index.html")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon2.ico')


@app.route("/graph-settings", methods=["GET", "POST"])
def graph_settings():
    if request.method == "GET":
        return render_template("graph_settings.html")
    if request.method == "POST":
        try:
            session["graph_dimensions"] = int(request.form.get("graph_dimensions"))
        except ValueError:
            return render_template("median_error.html", message="Du musst eine positive Anzahl an Punkten eingeben!")

        return render_template("graph_input.html", dimensions=session["graph_dimensions"])


@app.route("/graph-input", methods=["POST"])
def graph_input():
    weights_vector = []
    weights_matrix = []
    dist_matrix = []
    weighted_matrix = []
    matrix_sum = []
    matrix_max = []
    result = []

    for i in range(session["graph_dimensions"]):
        weights_vector.append(float(request.form.get(f"w{i + 1}")))
    print(weights_vector)

    for row in range(session["graph_dimensions"]):
        r = []
        for col in range(session["graph_dimensions"]):
            r.append(float(request.form.get(f"{row + 1}{col + 1}")))
        dist_matrix.append(r)

    weights_matrix = matrix_from_weights_vector(weights_vector)
    weighted_matrix = np.matmul(np.array(weights_matrix), np.array(dist_matrix))
    matrix_sum = np.asarray(weighted_matrix.sum(axis=0))
    matrix_max = np.asarray(np.amax(weighted_matrix, axis=0))

    result.append(matrix_sum)
    result.append(matrix_max)
    result.append(np.asarray(weighted_matrix))
    print(result)

    session.pop("graph_dimensions", None)
    return render_template("graph_results.html", results=result)


@app.route("/median-settings", methods=["GET", "POST"])
def median_settings():
    if request.method == "GET":
        return render_template("median_settings.html")
    if request.method == "POST":
        try:
            session["median_amount_2d_points"] = int(request.form.get("nr_of_points"))
        except ValueError:
            return render_template("median_error.html", message="Du musst eine positive Anzahl an Punkten eingeben!")

        try:
            session["median_delta"] = float(request.form.get("weiszfeld_delta"))
            print(f"Gewünschtes Delta: {session['median_delta']}")
        except ValueError:
            session["median_delta"] = 0
        except TypeError:
            session["median_delta"] = 0

        try:
            # todo
            x = float(request.form.get("weiszfeld_start_x"))
            y = float(request.form.get("weiszfeld_start_y"))
            session["weiszfeld_startpunkt"] = [x, y]
        except ValueError:
            print("No alternative starting Point")
        except TypeError:
            print("No alternative starting Point")

        return render_template("median_input.html", dimensions=session["median_amount_2d_points"])


@app.route("/median-input", methods=["GET", "POST"])
def median_input():
    """
    Hier werden Schwerpunkt, verschärftes Dominanzkriterium und ein paar weiszfeld iterationen berechnet
    dabei greifen wir auch auf die session zurück mit den 2d-points. Sind ja hier auch wieder 2d Punkte
    :return:
    """
    if request.method == "POST":
        weights = []
        punkte = []
        dominanzkriterium = []
        fulfilled = []
        sp = None
        entfernungen = []
        weiszfeld_results = []
        show_weiszfeld = False

        for i in range(session["median_amount_2d_points"]):
            weights.append(float(request.form.get(f"w{i + 1}")))
        print(weights)

        for i in range(session["median_amount_2d_points"]):
            x = float(request.form[f"x{i + 1}"])
            y = float(request.form[f"y{i + 1}"])
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

        for d, w in zip(dominanzkriterium, weights):
            if d <= w:
                fulfilled.append(True)
            else:
                fulfilled.append(False)

        # l22 metrik:
        sp = np.round(schwerpunkt(weights=weights, punkte=punkte), 4)
        entfernungen.append(round(entfernung(weights, punkte, sp, l22metrik), 4))
        entfernungen.append(round(entfernung(weights, punkte, sp, l2metrik), 4))
        entfernungen.append(round(entfernung(weights, punkte, sp, l1metrik), 4))
        entfernungen.append(round(entfernung(weights, punkte, sp, l8metrik), 4))

        # Platz für den Weizfeld

        print(f"Fulfilled Array: {fulfilled}")
        print(f"Session[median_delta] = {session['median_delta']}")
        if not any(fulfilled) and session["median_delta"] > 0:
            print("weiszfeld wurde ausgelöst!!!")
            show_weiszfeld = True
            max_rounds = 10
            round_counter = 0
            d = 1
            x = None

            if "weiszfeld_startpunkt" in session:
                x = session["weiszfeld_startpunkt"]

            else:
                x = sp

            fx = round(entfernung(weights, punkte, x, l2metrik), 4)
            weiszfeld_results = [[x, fx, "---"]]

            while round_counter < max_rounds and d > session["median_delta"]:
                x_new = weiszfeld(weights=weights, punkte=punkte, xk=x)
                fx_new = round(entfernung(weights, punkte, x_new, l2metrik), 4)
                print(f"fx alt : {fx}, fx neu: {fx_new}, x neu: {x_new}, x alt: {x}")
                try:
                    d = delta(fx, fx_new)
                except Exception:
                    print(Exception)
                print(f"delta = {d}")
                x = x_new
                fx = fx_new
                results = [x, fx, d]
                weiszfeld_results.append(results)

                round_counter += 1

        session.pop("weiszfeld_startpunkt", None)
        return render_template("median_results.html",
                               schwerpunkt=sp,
                               entfernungen=entfernungen,
                               weights=weights,
                               punkte=punkte,
                               gamma=dominanzkriterium,
                               fulfilled=fulfilled,
                               punktezahl=session["median_amount_2d_points"],
                               show_weiszfeld=show_weiszfeld,
                               weiszfeld_results=weiszfeld_results)


@app.route("/metriken-multi-settings", methods=["GET", "POST"])
def metriken_multiple_points_settings():
    if request.method == "GET":
        return render_template("metriken_multi_settings.html")
    if request.method == "POST":
        try:
            session["metriken_amount_2d_points"] = int(request.form.get("nr_of_points"))
        except ValueError:
            return render_template("metriken_multi_error.html",
                                   message="Du musst eine positive Anzahl an Punkten eingeben!")
        return render_template("metriken_multi_input.html", dimensions=session["metriken_amount_2d_points"])


@app.route("/metriken-multi-input", methods=["POST"])
def metriken_multi_points_input():
    points = []
    two = []
    rows = []

    for i in range(session["metriken_amount_2d_points"]):
        try:
            x = float(request.form.get(f"x{i + 1}"))
            y = float(request.form.get(f"y{i + 1}"))
            print(f"x = {x}, y = {y}")
            points.append(np.array([x, y]))
        except ValueError:
            return render_template("metriken_multi_error.html", message="Du musst für alle Punkte Werte eigeben.\n"
                                                                        "Verwende Punkte statt Kommas! - ValueError")
        except TypeError:
            return render_template("metriken_multi_error.html", message="Du musst für alle Punkte Werte eigeben.\n"
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


@app.route("/metriken-settings", methods=["POST", "GET"])
def metriken():
    if request.method == "GET":
        return render_template("metriken_settings.html")
    else:
        try:
            dimensions = int(request.form.get("dimensions"))
        except ValueError:
            return render_template("metriken_error.html", message="You have to enter the wanted dimensions!")
        if dimensions < 1 or dimensions == None:
            return render_template("metriken_error.html", message="Have to have more than 0 dimensions!")
        else:
            session["metriken_2_points_dimensions"] = dimensions
            return render_template("metriken_input.html", dimensions=dimensions)


@app.route("/metriken-results", methods=["POST", "GET"])
def metriken_results():
    if request.method == "POST":
        l1 = []
        l2 = []
        for i in range(session["metriken_2_points_dimensions"]):
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
            session["m_u_r_amount_of_points"] = int(request.form.get("nr_of_points"))
        except ValueError:
            return render_template("mp_und_radius_error.html",
                                   message="Du musst eine positive Anzahl an Punkten eingeben!")
        return render_template("mp_und_radius_input.html", dimensions=session["m_u_r_amount_of_points"])


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
        minimal_überdeckender_kreis = []

        for i in range(session["m_u_r_amount_of_points"]):
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
            row.append(np.round(mp, 4))
            row.append(round(radius, 4))

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

            # ------------
            try:
                # Testen ob es eine Mittelsenkrecht gibt, oder ob beide Werte auf gleicher Höhe liegen
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
                # Testen ob es einen Schnittpunkt gibt
                if radius == 0:
                    print(f"{mi1} -- {bi1} -- {mi2} -- {bi2}")
                    x, y = schnittpunkt_ms(mi1, bi1, mi2, bi2)
                    mp = np.array([x, y])
                    radius = l2metrik(mp, a)
            except ValueError:
                # Es gibt keinen Schnittpunkt der Achsen -> die Punkte liegen alle auf einer Achse
                mp, radius = mp_und_radius_drei_auf_gleicher_achse(a, b, c)

            row.append(np.round(mp, 4))
            row.append(round(radius, 4))
            for point in points:
                row.append(punkt_im_radius(mp, radius, point))
            rows.append(row)

        for ind, row in enumerate(rows):
            # Check mal ab, was da so rauskommt
            # print(f"ROWS : {row}")
            try:
                print(row)
                if all(row[3:]):
                    minimal_überdeckender_kreis.append(ind)
                    print(f"MÜK bei index: {minimal_überdeckender_kreis}")
            except ValueError:
                # print("ValueError bei Checken der Ergebnisse")
                pass
        return render_template("mp_und_radius_results.html", rows=rows, muek=minimal_überdeckender_kreis)


@app.route("/l1-l8-center-settings", methods=["POST", "GET"])
def l1_l8_center_settings():
    if request.method == "GET":
        return render_template("anzahl_punkte_template.html",
                               page="l1-l8-center",
                               heading="L1 und L-Unendlich Centerprobleme",
                               message="Du kannst später entscheiden, ob du den gewichteten Fall oder ungewichteten Fall haben willst",
                               inhalt="Entscheide im nächsten Schritt, ob du die l1 oder l unendlich Metrik willst",
                               warning=True,
                               name_of_input="l1_l8_center_amount_points")
    if request.method == "POST":
        try:
            session["l1_l8_center_amount_points"] = int(request.form.get("l1_l8_center_amount_points"))
        except ValueError:
            return render_template("median_error.html", message="Du musst eine positive Anzahl an Punkten eingeben!")

        return render_template("l1_l8_center_input.html", dimensions=session["l1_l8_center_amount_points"])


@app.route("/l1-l8-center-input", methods=["POST"])
def l1_l8_center_input():
    weights = []
    punkte = []
    transformierte_punkte = []
    l1_metrik_chosen = True

    for i in range(session["l1_l8_center_amount_points"]):
        try:
            weights.append(float(request.form[f"w{i + 1}"]))
        except Exception as e:
            print(e)

    print("weights eingelesen")

    for i in range(session["l1_l8_center_amount_points"]):
        try:
            x = float(request.form[f"x{i + 1}"])
            y = float(request.form[f"y{i + 1}"])
            punkte.append(np.array([x, y]))
        except ValueError or TypeError:
            return render_template("error_template.html", page="l1-l8-center",
                                   message="Du musst für alle Punkte Werte eigeben.\n "
                                           "Verwende Punkte statt Kommas! - ValueError")

    if len(weights) != len(punkte) and len(weights) > 0:
        return render_template("error_template.html", page="l1-l8-center",
                               message="Eingabefehler! Gleich viele Gewichte und Punkte eingeben")
    print("x und y eingelesen")

    if request.form["l1-or-l8"] == "l1":
        l1_metrik_chosen = True
        transformierte_punkte = l1_zu_l8_transformation(punkte)
        print("L1 Metrik ausgewählt")
    else:
        l1_metrik_chosen = False
        transformierte_punkte = punkte.copy()
        print("L unendlich Metrik ausgewählt")

    if len(weights) == 0:
        # ungewichteter Fall:
        unten_links, oben_rechts, delta_x, delta_y, quadrat, mittelpunkt = l8_center_ungewichtet(transformierte_punkte)
        unten_links_t = l8_zu_l1_transformation([unten_links])
        oben_rechts_t = l8_zu_l1_transformation([oben_rechts])
        mittelpunkt_t = l8_zu_l1_transformation([mittelpunkt])

        return render_template("l1_l8_ungewichtet_results.html",
                               unten_links=np.round(unten_links,4),
                               oben_rechts=np.round(oben_rechts,4),
                               delta_x=np.round(delta_x,4),
                               delta_y=np.round(delta_y,4),
                               quadrat=quadrat,
                               mittelpunkt=np.round(mittelpunkt,4),
                               l1_chosen=l1_metrik_chosen,
                               unten_links_t=np.round(np.asarray(unten_links_t)[0],4),
                               oben_rechts_t=np.round(np.asarray(oben_rechts_t)[0],4),
                               delta_x_t="gilt nur für l unendlich",
                               delta_y_t="gilt nur für l unendlich",
                               quadrat_t="gilt nur für l unendlich",
                               mittelpunkt_t=np.round(np.asarray(mittelpunkt_t)[0],4))

    else:
        x_punkte = [punkt[0] for punkt in transformierte_punkte]
        y_punkte = [punkt[1] for punkt in transformierte_punkte]

        combis, combis_of_actual_points_x, x_delta_list, x_delta_max, x_combi_of_delta_max, x_stern = l8_center_gewichtet_eindimensional(weights,
                                                                                                              x_punkte)
        combis2, combis_of_actual_points_y, y_delta_list, y_delta_max, y_combi_of_delta_max, y_stern = l8_center_gewichtet_eindimensional(weights, y_punkte)

        x_y_stern_t = l8_zu_l1_transformation([[x_stern,y_stern]])


        return render_template("l1_l8_gewichtet_results.html",
                               combi_len=len(combis),
                               combis=combis,
                               combis_of_actual_points_x=combis_of_actual_points_x,
                               combis_of_actual_points_y=combis_of_actual_points_y,
                               x_delta_list=np.round(x_delta_list,4),
                               y_delta_list=np.round(y_delta_list,4),
                               x_delta_max=np.round(x_delta_max,4),
                               x_combi_of_delta_max=x_combi_of_delta_max,
                               x_stern=np.round(x_stern,4),
                               y_stern=np.round(y_stern,4),
                               y_delta_max=np.round(y_delta_max,4),
                               y_combi_of_delta_max=y_combi_of_delta_max,
                               l1_chosen=l1_metrik_chosen,
                               x_stern_t=np.round(np.asarray(x_y_stern_t)[0][0],4),
                               y_stern_t=np.round(np.asarray(x_y_stern_t)[0][1],4)
                               )

        pass


@app.route("/diskrete-settings", methods=["GET", "POST"])
def diskrete_settings():
    if request.method == "GET":
        return render_template("diskrete_settings.html")
    else:
        try:
            nr_of_j = int(request.form.get("nr_of_j"))
            nr_of_i = int(request.form.get("nr_of_i"))
        except ValueError:
            return render_template("diskrete_error.html", message="You have to enter the wanted dimensions!")
        if nr_of_j < 1 or nr_of_j is None or nr_of_i < 1 or nr_of_i is None:
            return render_template("diskrete_error.html", message="Have to have more than 0 dimensions!")
        else:
            session["nr_of_j"] = nr_of_j
            session["nr_of_i"] = nr_of_i
            return render_template("diskrete_input.html", nr_of_i=nr_of_i, nr_of_j=nr_of_j)


@app.route("/diskrete-input", methods=["POST"])
def diskrete_input():
    weights_vector = []
    dist_matrix = []

    for i in range(session["nr_of_j"]):
        weights_vector.append(float(request.form.get(f"w{i + 1}")))
    print(weights_vector)

    for row in range(session["nr_of_i"]):
        r = []
        for col in range(session["nr_of_j"]):
            r.append(float(request.form.get(f"{row + 1}{col + 1}")))
        dist_matrix.append(r)

    distance_matrix = copy.deepcopy(dist_matrix)
    # d_matrix = copy.deepcopy(dist_matrix)
    # weights_two = copy.deepcopy(weights_vector)
    weights = copy.deepcopy(weights_vector)

    vi, Ji, sj = dual_ascent(cost_array=dist_matrix, fixcosts=weights_vector)

    dual_ascent_result_matrix = dual_ascent_zu_grosser_matrix(costMatrix=dist_matrix, sj=sj, vi=vi, Ji=Ji)

    delt, omega, chosen_js, kostenentwicklung, ui = greedy(input_array=distance_matrix, fj=weights)
    greedy_results = greedy_zu_einer_matrix(costMatrix=distance_matrix,
                                            fj=weights,
                                            delta=delt,
                                            omega=omega,
                                            chosen_js=chosen_js,
                                            kostenentwicklung=kostenentwicklung,
                                            ui=ui)

    # session.pop("nr_of_j", None)
    # session.pop("nr_of_i", None)
    return render_template("diskrete_results.html",
                           dual_ascent_results=dual_ascent_result_matrix,
                           greedy_results=greedy_results)


@app.route("/matrix-multi", methods=["GET", "POST"])
def matrix_mul_settings():
    pass


@app.route("/impressum", methods=["GET"])
def impressum():
    return render_template("impressum.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
