from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from plots import fig
from tkinter import (Button, DoubleVar, Entry, Frame, Label, LEFT, OptionMenu,
                     RIGHT, StringVar, Tk)
from zernike_terms import ZERNIKE_TERM_NAMES, ZERNIKE_TERM_RANGE


# Remove some of the useless buttons
# https://stackoverflow.com/a/15549675
class NavigationToolbar(NavigationToolbar2Tk):
    toolitems = [
        t for t in NavigationToolbar2Tk.toolitems
        if t[0] in ('Home', 'Pan', 'Zoom', 'Save')
    ]


# A common syntax throughout is the following two lines:
#   v = <Element>()
#   v.grid
# This just creates a temporary reference to the element so that it can be put
# on the grid. This could be done in one line, but then the lines get too long.
# Additionally, the GUI has been hardcoded to handle 24 Zernike terms.
def display_gui(
    update_zernike_amp,
    update_cmap,
    cmap_names,
    update_plot_func,
    plot_names,
):
    # ================
    # Init the GUI
    # ================
    window = Tk()
    window.title('Zernike Visualization')

    # ================
    # Display the Plot
    # ================

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    v = canvas.get_tk_widget()
    v.grid(row=0, rowspan=18, column=0, ipadx=20, ipady=20)

    # ============================
    # Display the Plotting Toolbar
    # ============================

    toolbar_frame = Frame(master=window)
    toolbar_frame.grid(row=17, column=0, padx=10, pady=10, sticky='W')
    NavigationToolbar(canvas, toolbar_frame)

    # =======================
    # Display the Input Boxes
    # =======================

    # Label that sits above all the inputs boxes
    v = Label(window, text='Noll Zernike Term Amplitude (Unitless)')
    v.grid(row=0, column=1, columnspan=6, pady=10)

    zernike_inputs = []
    for term in range(*ZERNIKE_TERM_RANGE):
        row = term - 12 if term > 12 else term
        offset = 3 if term > 12 else 0
        v = Label(window, text=f'{ZERNIKE_TERM_NAMES[term]}', justify=RIGHT)
        v.grid(row=row, column=1 + offset, padx=(10, 0), sticky='E')
        v = Label(window, text=f'Z{term}', justify=RIGHT)
        v.grid(row=row, column=2 + offset, sticky='E')
        entry_text = DoubleVar()
        v = Entry(window, width=8, textvariable=entry_text)
        v.grid(row=row, column=3 + offset, padx=10)
        zernike_inputs.append(entry_text)

    # ==============================
    # Track and Update Input Changes
    # ==============================

    # Wrapper to pass the input being changed in
    def input_change_wrapper(zernike_term, input_var):

        def curried(*args):
            try:
                term_val = input_var.get()
            except Exception:
                term_val = 0.0
            update_zernike_amp(zernike_term, term_val)

        return curried

    # Track the changes to each of the inputs
    for term_idx, zernike_input in enumerate(zernike_inputs, 1):
        zernike_input.trace_add(
            'write',
            input_change_wrapper(term_idx, zernike_input),
        )

    # ===========
    # Reset Terms
    # ===========

    def reset_terms():
        update_zernike_amp('all_zero')
        for zernike_input in zernike_inputs:
            zernike_input.set(0.0)

    # Button to reset the Zernike terms and plot
    v = Button(window, text='Reset Terms', command=reset_terms)
    v.grid(row=14, column=1, columnspan=6, padx=10, sticky='WE')

    # ===============
    # Change Colormap
    # ===============

    # Label to change the plot type
    v = Label(window, text='Colormap:', justify=LEFT)
    v.grid(row=15, column=1, columnspan=2, padx=10, sticky='W')

    # Option menu to change the plot type
    cmap_name = StringVar()
    v = OptionMenu(window, cmap_name, *cmap_names, command=update_cmap)
    v.grid(row=15, column=3, columnspan=4, padx=10, sticky='WE')

    # ================
    # Change Plot Type
    # ================

    # Label to change the plot type
    v = Label(window, text='Plot Type:', justify=LEFT)
    v.grid(row=16, column=1, columnspan=2, padx=10, sticky='W')

    # Option menu to change the plot type
    plot_type = StringVar()
    v = OptionMenu(window, plot_type, *plot_names, command=update_plot_func)
    v.grid(row=16, column=3, columnspan=4, padx=10, sticky='WE')

    # ==============
    # Default values
    # ==============

    # The default plot type and cmap
    plot_type.set(plot_names[0])
    cmap_name.set(cmap_names[0])
    # Update the first term and revert it to display the initial plot
    update_zernike_amp(1, 1)
    update_zernike_amp(1, 0)

    # ===========
    # Display GUI
    # ===========

    window.mainloop()
