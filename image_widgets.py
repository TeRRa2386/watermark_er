import customtkinter as ctk
from tkinter import filedialog, Canvas
from settings import *


class ImageImport(ctk.CTkFrame):

    def __init__(self, parent, import_func):

        super().__init__(master=parent)
        self.grid(column=0, columnspan=2, row=0, sticky='nsew')
        self.import_func = import_func

        ctk.CTkButton(self, text='Open Image', command=self.open_dialog).pack(expand=True)

    def open_dialog(self):

        path = filedialog.askopenfilename()
        self.import_func(path)


class ImageOutput(Canvas):

    def __init__(self, parent, resize_image):

        super().__init__(master=parent, background=BACKGROUND_COLOR, bd=0, highlightthickness=0, relief='ridge')
        self.grid(row=0, column=1, sticky='nsew', pady=10, padx=10)
        self.bind('<Configure>', resize_image)


class CloseOutput(ctk.CTkButton):

    def __init__(self, parent, close_func):

        super().__init__(master=parent,
                         text='x',
                         text_color=WHITE,
                         fg_color='transparent',
                         width=40, height=40,
                         corner_radius=0,
                         hover_color= CLOSE_RED,
                         command=close_func)
        self.place(relx=0.99, rely=0.01, anchor='ne')


class LogoImport(ctk.CTkButton):

    def __init__(self, parent, import_func):

        super().__init__(master=parent,
                         text='Import Logo',
                         command=self.open_dialog,
                         )
        self.place(relx=0.75, rely=0.68, anchor='se')
        self.import_func = import_func

    def open_dialog(self):

        path = filedialog.askopenfilename()
        if path:
            self.import_func(path)


class SaveButton(ctk.CTkButton):

    def __init__(self, parent, export_image):

        super().__init__(master=parent,
                         text='Save',
                         command=export_image,
                         fg_color=GREEN_FG,
                         hover_color=GREEN_HV,
                         )
        self.place(relx=0.75, rely=0.95, anchor='se')


class RemoveButton(ctk.CTkButton):

    def __init__(self, parent, clear_logo):

        super().__init__(master=parent,
                         text='❌ Remove Logo',
                         command=clear_logo,
                         fg_color=RED_FG,
                         hover_color=RED_HV,)
        self.place(relx=0.75, rely=0.75, anchor='se')


    def set_enabled(self, enabled: bool):
        if enabled:
            self.configure(state="normal", fg_color=RED_FG, text_color="white")
        else:
            self.configure(state="disabled", fg_color=GREY_DB, text_color=TEXT_DB)