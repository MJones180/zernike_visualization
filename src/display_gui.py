import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from tkinter import (DoubleVar, Entry, Frame, Label, LEFT, OptionMenu,
                     StringVar, Tk)

from zernike_terms import ZERNIKE_TERM_NAMES


def handle_zernike_value_changes(zernike_term, term_val, fig):
    print(zernike_term, term_val)
    fig.clf()
    plot1 = fig.add_subplot(111)
    y = [(i + term_val)**2 for i in range(101)]
    # plotting the graph
    plot1.plot(y)
    fig.canvas.draw()


def display_gui(handle_zernike_value_changes):
    # The main window
    window = Tk()
    window.title('Zernike Polynomials')

    # the figure that will contain the plot
    fig = plt.Figure(figsize=(5, 5), dpi=100)
    # adding the subplot
    # specify the window as root
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=1,
                                column=0,
                                ipadx=40,
                                ipady=20,
                                rowspan=16)
    # navigation toolbar
    toolbarFrame = Frame(master=window)
    toolbarFrame.grid(row=17, column=0)
    NavigationToolbar2Tk(canvas, toolbarFrame)

    Label(window, text='<Plot Type>').grid(row=0, column=0, pady=10)
    Label(window,
          text='Noll Zernike Term Amplitude (Unitless)').grid(row=0,
                                                              column=1,
                                                              columnspan=4,
                                                              pady=10)
    zernike_inputs = []
    for term in range(1, 13):
        Label(window, text=f'Z{term}', justify=LEFT).grid(row=term,
                                                          column=1,
                                                          padx=10)
        entry_text = DoubleVar()
        Entry(window, width=10, textvariable=entry_text).grid(row=term,
                                                              column=2,
                                                              padx=5)
        zernike_inputs.append(entry_text)
    for term in range(1, 13):
        Label(window, text=f'Z{term + 12}', justify=LEFT).grid(row=term,
                                                               column=3,
                                                               padx=10)
        entry_text = DoubleVar()
        Entry(window, width=10, textvariable=entry_text).grid(row=term,
                                                              column=4,
                                                              padx=5)
        zernike_inputs.append(entry_text)

    def my_callback_curry(zernike_term, input_var):

        def curried(*args):
            try:
                term_val = input_var.get()
            except Exception:
                term_val = 0.0
            handle_zernike_value_changes(zernike_term, term_val, fig)

        return curried

    for term_idx, zernike_input in enumerate(zernike_inputs):
        zernike_input.trace_add('write',
                                my_callback_curry(term_idx + 1, zernike_input))

    strs = [f'Z{term}: {name}' for term, name in ZERNIKE_TERM_NAMES.items()]
    Label(window, text='\n'.join(strs), justify=LEFT).grid(row=1,
                                                           column=5,
                                                           rowspan=13,
                                                           padx=10,
                                                           sticky='N')

    Label(window, text='Plot Type', justify=LEFT).grid(row=15,
                                                       column=1,
                                                       columnspan=2,
                                                       padx=10,
                                                       sticky='W')
    OPTIONS = ['a', 'b', 'c']
    var1 = StringVar(window)
    var1.set(OPTIONS[1])
    OptionMenu(window, var1, *OPTIONS).grid(row=16,
                                            column=1,
                                            columnspan=4,
                                            padx=10,
                                            sticky='W')

    def update_plot():
        # list of squares
        y = [i**2 for i in range(101)]
        # plotting the graph
        plot1.plot(y)
        fig.canvas.draw()

    window.mainloop()


display_gui(handle_zernike_value_changes)
