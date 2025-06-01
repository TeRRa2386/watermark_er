import customtkinter as ctk
from settings import *


class Panel(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(master=parent, fg_color= DARK_GREY)
        self.pack(fill='x', pady=4, ipady=8, padx=10)


class SliderPanel(Panel):

    def __init__(self, parent, text, data_var, min_value, max_value):

        super().__init__(parent=parent)
        # layout
        self.rowconfigure((0,1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='w', padx=12)
        self.num_label = ctk.CTkLabel(self, text=data_var.get())
        self.num_label.grid(column=1, row=0, sticky='e', padx=12)
        self.slider = ctk.CTkSlider(self, fg_color=SLIDER_BG,
                                    variable=data_var,
                                    from_=min_value,
                                    to=max_value,
                                    command=self.update_text)
        self.slider.grid(row=1, column=0, columnspan=2, sticky='ew', padx=7, pady=5)


    def set_state(self, state):

        if self.slider:
            self.slider.configure(state=state)


    def update_text(self, value):

        self.num_label.configure(text=f'{round(value,2)}')


    def refresh(self):
        self.update_text(self.slider.get())

