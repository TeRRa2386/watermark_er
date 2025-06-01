import customtkinter as ctk
from image_widgets import *
from panels import *

class Menu(ctk.CTkTabview):

    def __init__(self, parent, rotation, logo_scale, logo_spacing, import_func, tile_mode, logo_opacity, clear_func, export_image):

        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew', pady=20, padx=10)

        # tabs
        self.add('Edit Logo')

        # widgets
        self.edit_logo_tab = EditFrame(self.tab('Edit Logo'), rotation, logo_scale, logo_spacing, import_func, tile_mode, logo_opacity, clear_func, export_image)


class EditFrame(ctk.CTkFrame):

    def __init__(self, parent, rotation, logo_scale, logo_spacing, import_func, tile_mode, logo_opacity, clear_func, export_image):

        super().__init__(master = parent, fg_color='transparent')
        self.pack(expand=True, fill='both')

        self.rotation_slider = SliderPanel(self, 'Rotation', rotation, 0, 359)
        self.logo_size_slider = SliderPanel(self, 'Logo Size', logo_scale, 0.05, 3.0)
        self.transparency_slider = SliderPanel(self, 'Transparency', logo_opacity, 0.1, 1.0)

        self.tile_mode_switch = ctk.CTkSwitch(self, text="Tile Mode", variable=tile_mode)
        self.tile_mode_switch.pack(pady=10)
        self.spacing_slider = SliderPanel(self, 'Spacing', logo_spacing, 0.5, 3.0)
        self.spacing_slider.pack(fill="x", pady=4, ipady=8, padx=10)

        self.tile_mode_var = tile_mode
        tile_mode.trace_add('write', self.update_slider_states)
        self.update_slider_states()


        LogoImport(self, import_func)
        self.remove_logo_button = RemoveButton(self, self.clear_logo)
        self.clear_func = clear_func
        SaveButton(self, export_image)


    def update_slider_states(self, *args):

        if self.tile_mode_var.get():
            self.spacing_slider.set_state("normal")
        else:
            self.spacing_slider.set_state("disabled")


    def set_controls_enabled(self, enabled=True):

        state = "normal" if enabled else "disabled"

        self.transparency_slider.set_state(state)
        self.rotation_slider.set_state(state)
        self.logo_size_slider.set_state(state)
        self.tile_mode_switch.configure(state=state)
        self.remove_logo_button.configure(state=state)
        self.remove_logo_button.set_enabled(enabled)


    def clear_logo(self):

        self.tile_mode_var.set(False)
        self.clear_func()

    def refresh_all_sliders(self):
        self.transparency_slider.refresh()
        self.rotation_slider.refresh()
        self.logo_size_slider.refresh()
        self.spacing_slider.refresh()
