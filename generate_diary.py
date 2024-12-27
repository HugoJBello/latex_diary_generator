
import datetime
import locale
from matplotlib import pyplot as plt
from lunar_phase import phase,position
import json

with open('fechas/fechas_importantes_uva.json', 'r') as file:
    fechas_importantes_uva = json.load(file)

with open('fechas/festivos.json', 'r') as file:
    festivos = json.load(file)

def generate_heading():
    f = open("text_blocks/initial.tex", "r")
    return f.read()


def generate_graph(initial_date, number_of_weeks=15):
    fig, ax = plt.subplots()

    # We need to draw the canvas, otherwise the labels won't be positioned and 
    # won't have values yet.
    fig.canvas.draw()



    ax.axis([0, number_of_weeks, 0, 25])

    plt.xticks(range(0, number_of_weeks))
    plt.yticks(range(0, 25))

    ticks = []

    current_date = initial_date
    for i in range(number_of_weeks):
        start = current_date - datetime.timedelta(days=current_date.weekday())
        end = start + datetime.timedelta(days=6)
        current_date = end + datetime.timedelta(days=1)
        date_str = current_date.strftime("%b %d, %Y")
        ticks.append(date_str)

    

    plt.grid()
    plt.xticks(rotation=70)



    ax.set_xticklabels(ticks)
    plt.savefig("graph.png", bbox_inches='tight')

def generate_intro(start, semanas):
    generate_graph(start, semanas)

    f = open("text_blocks/intro.tex", "r")
    intro =  f.read()
    start_str = start.strftime("%b %d, %Y")

    intro = intro.replace("DATE1", start_str)
    intro = intro.replace("WEEKS", str(semanas))
    return intro

def generate_tasks_page(start, end):
    f = open("text_blocks/tasks.tex", "r")
    table =  f.read()
    start_str = start.strftime("%b %d, %Y")
    end_str = end.strftime("%b %d, %Y")

    table = table.replace("DATE1", start_str)
    table = table.replace("DATE2", end_str)
    return table


def generate_calendar_intro(start, semanas):
    f = open("text_blocks/calendar_intro.tex", "r")
    intro =  f.read()
    start_str = start.strftime("%b %d, %Y")
    month = start.strftime("%m")

    intro = intro.replace("DATE1", start_str)
    intro = intro.replace("WEEKS", str(semanas))
    intro = intro.replace("MONTH", str(month))
    return intro


def generate_calendar_page(start):


    f = open("text_blocks/calendar.tex", "r")
    table =  f.read()
    mes = start.strftime("%b")
    
    dateL = start
    dateM = start + datetime.timedelta(days=1)
    dateX = start + datetime.timedelta(days=2)
    dateJ = start + datetime.timedelta(days=3)
    dateV = start + datetime.timedelta(days=4)
    dateS = start + datetime.timedelta(days=5)
    dateD = start + datetime.timedelta(days=7)

    table = table.replace("MES", mes)
    table = table.replace("DATEL", surround_day(dateL))
    table = table.replace("DATEM", surround_day(dateM))
    table = table.replace("DATEX", surround_day(dateX))
    table = table.replace("DATEJ", surround_day(dateJ))
    table = table.replace("DATEV", surround_day(dateV))
    table = table.replace("DATES", surround_day(dateS))
    table = table.replace("DATED", surround_day(dateD))
    
    table = table.replace("MOONL", get_moon_image(phase(position(dateL))[0]))
    table = table.replace("MOONM", get_moon_image(phase(position(dateM))[0]))
    table = table.replace("MOONX", get_moon_image(phase(position(dateX))[0]))
    table = table.replace("MOONJ", get_moon_image(phase(position(dateJ))[0]))
    table = table.replace("MOONV", get_moon_image(phase(position(dateV))[0]))
    table = table.replace("MOONS", get_moon_image(phase(position(dateS))[0]))
    table = table.replace("MOOND", get_moon_image(phase(position(dateD))[0]))
    
    
    table = table.replace("SPECIALL", get_important_dates(dateL))
    table = table.replace("SPECIALM", get_important_dates(dateM))
    table = table.replace("SPECIALX", get_important_dates(dateX))
    table = table.replace("SPECIALJ", get_important_dates(dateJ))
    table = table.replace("SPECIALV", get_important_dates(dateV))
    table = table.replace("SPECIALS", get_important_dates(dateS))
    table = table.replace("SPECIALD", get_important_dates(dateD))
    
    table = table.replace("FESTIVOL", get_festivity_dates(dateL))
    table = table.replace("FESTIVOM", get_festivity_dates(dateM))
    table = table.replace("FESTIVOX", get_festivity_dates(dateX))
    table = table.replace("FESTIVOJ", get_festivity_dates(dateJ))
    table = table.replace("FESTIVOV", get_festivity_dates(dateV))
    table = table.replace("FESTIVOS", get_festivity_dates(dateS))
    table = table.replace("FESTIVOD", get_festivity_dates(dateD))

    

    return table


def surround_day(date):
    return "\\textbf{\\sffamily{" + date.strftime("%d")  + "}} " + date.strftime("%b")

def get_moon_image(phase_index):
    if phase_index == 8 :
        phase_index = 0
    figure = """\\vspace{0.01cm} \centerline{\\includegraphics[width=0.5cm]{moon_phases/Moon_phase_number.svg.png}} \\vspace{0.1cm}"""
    return figure.replace("number", str(phase_index))    

def get_important_dates(date):
    formated_date = date.strftime("%d/%m/%Y")
    result = ""
    if formated_date in fechas_importantes_uva: 
        result = result + fechas_importantes_uva[formated_date]
    return "\\small{" + result + "}"


def get_festivity_dates(date):
    formated_date = date.strftime("%d/%m/%Y")
    result = ""
    if formated_date in festivos: 
        result = result + " " + festivos[formated_date]
    return "\\small{" + result + "}"
 
    

def main():

    initial_date =  datetime.datetime.now()
    number_of_weeks = 10

    resulting_tex = ""

    resulting_tex = generate_heading()

    start = initial_date - datetime.timedelta(days=initial_date.weekday())
    resulting_tex = resulting_tex + generate_intro(start, number_of_weeks)
    
    calendar_intro = generate_calendar_intro(start, number_of_weeks)

    current_date = initial_date
    for i in range(number_of_weeks):
        start = current_date - datetime.timedelta(days=current_date.weekday())
        end = start + datetime.timedelta(days=6)
        current_date = end + datetime.timedelta(days=1)
        tasks = generate_tasks_page(start,end)
        resulting_tex = resulting_tex + tasks + "\n\\newpage"

    resulting_tex = resulting_tex + calendar_intro

    current_date = initial_date
    for i in range(number_of_weeks):
        start = current_date - datetime.timedelta(days=current_date.weekday())
        end = start + datetime.timedelta(days=6)
        current_date = end + datetime.timedelta(days=1)

        calendar = generate_calendar_page(start)
        resulting_tex = resulting_tex + calendar + "\n\\newpage"
    
    resulting_tex = resulting_tex + "\\end{document}"


    with open('result.tex', 'w') as f:
        f.write(resulting_tex)


main()


