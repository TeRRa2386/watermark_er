from menu import *
from PIL import Image, ImageTk, ImageEnhance
from tkinter import filedialog
import os

class App(ctk.CTk):

    def __init__(self):

        #setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1176x664')
        self.title('Watermark-er')
        self.minsize(800,500)
        self.init_parameters()

        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')

        # Some Values
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0
        self.logo_x = None
        self.logo_y = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # widgets
        self.image_import = ImageImport(self, self.import_image)

        # run
        self.mainloop()


    def init_parameters(self):

        self.rotate_float = ctk.DoubleVar(value= ROTATE_DEFAULT)
        self.rotate_float.trace('w',self.manipulate_image)
        self.logo_scale = ctk.DoubleVar(value=SCALE_DEFAULT)
        self.logo_scale.trace('w', self.resize_logo)
        self.logo_spacing = ctk.DoubleVar(value=SPACING_DEFAULT)
        self.logo_spacing.trace('w', self.place_logo)
        self.tile_mode = ctk.BooleanVar(value=TILE_DEFAULT)
        self.tile_mode.trace('w', self.place_logo)
        self.logo_opacity = ctk.DoubleVar(value=OPACITY_DEFAULT)
        self.logo_opacity.trace('w', self.place_logo)


    def manipulate_image(self, *args):

        if not hasattr(self, 'logo'):
            return
        if hasattr(self, 'original_logo'):

            self.logo = self.original_logo.copy().rotate(self.rotate_float.get(), expand=True)
            self.place_logo()


    def import_image(self, path):

        if path:
            self.original = Image.open(path)
            self.image = self.original
            self.image_ratio = self.image.size[0] / self.image.size[1] # 0 is width , 1 is height
            self.image_tk = ImageTk.PhotoImage(self.image)

            self.image_import.grid_forget()
            self.image_output = ImageOutput(self, self.resize_image)
            self.image_output.bind("<ButtonPress-1>", self.start_move_logo)
            self.image_output.bind("<B1-Motion>", self.move_logo)
            self.close_button = CloseOutput(self, self.close_edit)

            self.menu = Menu(self, self.rotate_float, self.logo_scale, self.logo_spacing, self.import_logo, self.tile_mode, self.logo_opacity, self.clear_logo, self.export_image)
            self.menu.edit_logo_tab.set_controls_enabled(False)


    def import_logo(self, path):

        self.reset_values()
        self.logo_x = self.canvas_width // 2
        self.logo_y = self.canvas_height // 2

        self.original_logo = Image.open(path).convert("RGBA")
        self.logo = self.original_logo.copy()
        self.logo_ratio = self.logo.size[0] / self.logo.size[1]
        self.logo_tk = ImageTk.PhotoImage(self.logo)

        self.resize_logo()
        self.menu.edit_logo_tab.set_controls_enabled(True)


    def close_edit(self):

        if hasattr(self, 'logo_x'):
            self.logo_x = None
            self.logo_y = None

        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        self.image_import = ImageImport(self, self.import_image)
        self.menu.edit_logo_tab.set_controls_enabled(False)


    def clear_logo(self):

        if hasattr(self, 'logo'):
            del self.logo
        if hasattr(self, 'logo_tk'):
            del self.logo_tk
        if hasattr(self, 'original_logo'):
            del self.original_logo
        if hasattr(self, 'logo_x'):
            self.logo_x = None
            self.logo_y = None

        self.reset_values()
        self.menu.edit_logo_tab.set_controls_enabled(False)


    def reset_values(self):

        self.rotate_float.set(ROTATE_DEFAULT)
        self.logo_scale.set(SCALE_DEFAULT)
        self.logo_spacing.set(SPACING_DEFAULT)
        self.tile_mode.set(TILE_DEFAULT)
        self.logo_opacity.set(OPACITY_DEFAULT)
        self.menu.edit_logo_tab.refresh_all_sliders()

    def place_image(self):

        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)
        self.place_logo()


    def place_logo(self, *args):
        if not hasattr(self, 'logo') or not hasattr(self, 'image'):
            return

        self.update_idletasks()
        self.image_output.delete("logo_tile")

        base_image_for_composite = self.original.resize((self.image_width, self.image_height)).convert("RGBA")

        rotated_logo = self.original_logo.copy().rotate(self.rotate_float.get(), expand=True)
        resized_logo = rotated_logo.resize((
            int(rotated_logo.width * self.logo_scale.get()),
            int(rotated_logo.height * self.logo_scale.get())
        )).convert("RGBA")

        opacity = self.logo_opacity.get()
        if opacity < 1.0:
            alpha = resized_logo.getchannel("A")
            alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
            resized_logo.putalpha(alpha)

        composite = base_image_for_composite.copy()

        if self.tile_mode.get():
            logo_w, logo_h = resized_logo.size
            spacing = self.logo_spacing.get()
            step_x = int(logo_w * spacing)
            step_y = int(logo_h * spacing)

            cols_needed = int(self.image_width / step_x) + 2
            rows_needed = int(self.image_height / step_y) + 2

            start_x_offset = (self.image_width % step_x) / 2 if step_x > 0 else 0
            start_y_offset = (self.image_height % step_y) / 2 if step_y > 0 else 0

            for i in range(-1, rows_needed):
                for j in range(-1, cols_needed):
                    x = int(j * step_x + start_x_offset - logo_w / 2)
                    y = int(i * step_y + start_y_offset - logo_h / 2)
                    composite.alpha_composite(resized_logo, (x, y))

            self.final_image_for_export = composite
            self.image_tk = ImageTk.PhotoImage(composite)
            self.image_output.create_image(
                self.canvas_width / 2, self.canvas_height / 2,
                image=self.image_tk, tags="logo_tile"
            )
            self.image_output.unbind("<ButtonPress-1>")
            self.image_output.unbind("<B1-Motion>")

        else:
            self.image_tk = ImageTk.PhotoImage(composite)
            if self.logo_x is None:
                self.logo_x = self.canvas_width // 2
            if self.logo_y is None:
                self.logo_y = self.canvas_height // 2

            img_x_offset = (self.canvas_width - self.image_width) / 2
            img_y_offset = (self.canvas_height - self.image_height) / 2

            logo_pos_x_on_image = self.logo_x - img_x_offset - resized_logo.width / 2
            logo_pos_y_on_image = self.logo_y - img_y_offset - resized_logo.height / 2

            composite.alpha_composite(resized_logo, (int(logo_pos_x_on_image), int(logo_pos_y_on_image)))
            self.final_image_for_export = composite

            self.image_output.create_image(
                self.canvas_width / 2, self.canvas_height / 2,
                image=self.image_tk, tags="logo_tile"
            )

            # Logo interactivo visual
            self.logo_tk = ImageTk.PhotoImage(resized_logo)
            self.logo_id = self.image_output.create_image(self.logo_x, self.logo_y,
                                                          image=self.logo_tk,
                                                          anchor='center',
                                                          tags="logo_tile")
            self.image_output.tag_raise(self.logo_id)
            self.image_output.bind("<ButtonPress-1>", self.start_move_logo)
            self.image_output.bind("<B1-Motion>", self.move_logo)
            self.image_output.bind("<ButtonRelease-1>", self.drop_logo)


    def resize_image(self, event):

        self.canvas_width = event.width
        self.canvas_height = event.height
        canvas_ratio = self.canvas_width / self.canvas_height

        if canvas_ratio > self.image_ratio:
            self.image_height = int(self.canvas_height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(self.canvas_width)
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()


    def resize_logo(self, *args):
        if not hasattr(self, 'original_logo'):
            return

        scale = self.logo_scale.get()

        self.logo_width = int(self.original_logo.width * scale)
        self.logo_height = int(self.original_logo.height * scale)

        self.place_logo()


    def start_move_logo(self, event):

        if hasattr(self, 'logo_id'):
            item = self.image_output.find_closest(event.x, event.y)
            if item and item[0] == self.logo_id:
                self.dragging = True

                bbox = self.image_output.bbox(self.logo_id)
                if bbox:
                    center_x = (bbox[0] + bbox[2]) / 2
                    center_y = (bbox[1] + bbox[3]) / 2
                    self.drag_offset_x = center_x - event.x
                    self.drag_offset_y = center_y - event.y
                    self.last_mouse_x = event.x
                    self.last_mouse_y = event.y
            else:
                self.dragging = False


    def move_logo(self, event):

        if hasattr(self, 'dragging') and self.dragging:
            dx = event.x - self.last_mouse_x
            dy = event.y - self.last_mouse_y
            self.image_output.move(self.logo_id, dx, dy)
            self.last_mouse_x = event.x
            self.last_mouse_y = event.y


    def drop_logo(self, event):

        if hasattr(self, 'dragging') and self.dragging:
            self.logo_x = event.x + self.drag_offset_x
            self.logo_y = event.y + self.drag_offset_y
            self.dragging = False
            self.place_logo()


    def export_image(self):

        if not hasattr(self, 'final_image_for_export') or self.final_image_for_export is None:

            ctk.CTkLabel(self, text="No hay imagen para exportar.").pack(pady=20)
            return

        filetypes = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ]

        default_filename = "watermarked_image.png"
        if hasattr(self, 'original') and hasattr(self.original, 'filename'):
            original_base = os.path.basename(self.original.filename)
            name, ext = os.path.splitext(original_base)
            default_filename = f"{name}_watermarked{ext}"

        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=filetypes,
            initialfile=default_filename
        )

        if filepath:
            try:
                if filepath.lower().endswith(('.jpg', '.jpeg')):
                    if self.final_image_for_export.mode == 'RGBA':
                        self.final_image_for_export.convert('RGB').save(filepath)
                    else:
                        self.final_image_for_export.save(filepath)
                else:
                    self.final_image_for_export.save(filepath)

                success_label = ctk.CTkLabel(self, text=f"Image saved in:\n{filepath}", fg_color="green", text_color="white", corner_radius=5)
                success_label.place(relx=0.5, rely=0.9, anchor='center')
                self.after(3000, success_label.destroy) # 3 secs

            except Exception as e:
                error_label = ctk.CTkLabel(self, text=f"Error saving: {e}", fg_color="red", text_color="white", corner_radius=5)
                error_label.place(relx=0.5, rely=0.9, anchor='center')
                self.after(5000, error_label.destroy)


App()