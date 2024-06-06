from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from plots import get_plots
from tkinter import (Button, DoubleVar, Entry, Frame, Label, LEFT, OptionMenu,
                     StringVar, Tk)
from zernike_terms import ZERNIKE_TERM_NAMES


# https://stackoverflow.com/a/15549675
class NavigationToolbar(NavigationToolbar2Tk):
    toolitems = [
        t for t in NavigationToolbar2Tk.toolitems
        if t[0] in ('Home', 'Pan', 'Zoom', 'Save')
    ]


def display_gui(fig, update_zernike_amp, update_plot_func):
    window = Tk()
    window.title('Zernike Visualization')

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0,
                                column=0,
                                ipadx=40,
                                ipady=20,
                                rowspan=17)
    toolbar_frame = Frame(master=window)
    toolbar_frame.grid(row=16, column=0)
    NavigationToolbar(canvas, toolbar_frame)

    Label(window,
          text='Noll Zernike Term Amplitude (Unitless)').grid(row=0,
                                                              column=1,
                                                              columnspan=4,
                                                              pady=10)
    zernike_inputs = []
    for term in range(1, 25):
        term_row = term - 12 if term > 12 else term
        column = 3 if term > 12 else 1
        Label(window, text=f'Z{term}', justify=LEFT).grid(row=term_row,
                                                          column=column,
                                                          padx=10)
        entry_text = DoubleVar()
        Entry(window, width=10,
              textvariable=entry_text).grid(row=term_row,
                                            column=column + 1,
                                            padx=5)
        zernike_inputs.append(entry_text)

    def my_callback_curry(zernike_term, input_var):

        def curried(*args):
            try:
                term_val = input_var.get()
            except Exception:
                term_val = 0.0
            update_zernike_amp(zernike_term, term_val)

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

    def reset_terms():
        update_zernike_amp('all', 0.0)
        for zernike_input in zernike_inputs:
            zernike_input.set(0.0)

    Button(window, text='Reset Terms', command=reset_terms).grid(row=14,
                                                                 column=1,
                                                                 columnspan=2,
                                                                 padx=10,
                                                                 sticky='W')

    Label(window, text='Plot Type:', justify=LEFT).grid(row=15,
                                                        column=1,
                                                        columnspan=2,
                                                        padx=10,
                                                        sticky='W')
    plots_arr = get_plots()
    plot_names = [name for name, func in plots_arr]
    plot_type = StringVar(window)

    def plot_type_change(new_plot):
        for name, func in plots_arr:
            if name == new_plot:
                update_plot_func(func)

    OptionMenu(window, plot_type, *plot_names,
               command=plot_type_change).grid(row=16,
                                              column=1,
                                              columnspan=4,
                                              padx=10,
                                              sticky='W')

    plot_type.set(plot_names[0])
    zernike_inputs[0].set(1.0)

    window.mainloop()
