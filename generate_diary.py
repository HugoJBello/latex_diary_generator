
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

def generate_calendar_page(start, end):
    f = open("text_blocks/week.tex", "r")
    table =  f.read()
    start_str = start.strftime("%b %d, %Y")
    end_str = end.strftime("%b %d, %Y")

    table = table.replace("DATE1", start_str)
    table = table.replace("DATE2", end_str)
    return table




def main():

    initial_date =  datetime.datetime.now()
    number_of_weeks = 8

    resulting_tex = ""

    resulting_tex = generate_heading()

    start = initial_date - datetime.timedelta(days=initial_date.weekday())
    resulting_tex = resulting_tex + generate_intro(start, number_of_weeks)
    
    current_date = initial_date
    for i in range(number_of_weeks):
        start = current_date - datetime.timedelta(days=current_date.weekday())
        end = start + datetime.timedelta(days=6)
        current_date = end + datetime.timedelta(days=1)
        table = generate_calendar_page(start,end)
        resulting_tex = resulting_tex + table + "\n\\newpage"
    
    
    resulting_tex = resulting_tex + "\\end{document}"


    with open('result.tex', 'w') as f:
        f.write(resulting_tex)
main()


