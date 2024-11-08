
import datetime
import locale
from matplotlib import pyplot as plt


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

    intro = intro.replace("DATE1", start_str)
    intro = intro.replace("WEEKS", str(semanas))
    return intro

def generate_calendar_page(start):


    f = open("text_blocks/calendar.tex", "r")
    table =  f.read()
    mes = start.strftime("%b")

    dateL = start.strftime("%Y-%m-%d")
    dateM = (start + datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    dateX = (start + datetime.timedelta(days=2)).strftime("%Y-%m-%d")
    dateJ = (start + datetime.timedelta(days=3)).strftime("%Y-%m-%d")
    dateV = (start + datetime.timedelta(days=4)).strftime("%Y-%m-%d")
    dateS = (start + datetime.timedelta(days=5)).strftime("%Y-%m-%d")
    dateD = (start + datetime.timedelta(days=6)).strftime("%Y-%m-%d")



    table = table.replace("MES", mes)
    table = table.replace("DATEL", dateL)
    table = table.replace("DATEM", dateM)
    table = table.replace("DATEX", dateX)
    table = table.replace("DATEJ", dateJ)
    table = table.replace("DATEV", dateV)
    table = table.replace("DATES", dateS)
    table = table.replace("DATED", dateD)

    return table



def main():

    initial_date =  datetime.datetime.now()
    number_of_weeks = 8

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


