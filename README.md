# H2O-Mark_er 🖼💧

H2O-Maker is a lightweight desktop application built with Python and `customtkinter` that allows users to watermark images with custom logos. It supports manual placement or tiling mode, rotation, scaling, opacity adjustment, and export options.

## ✨ Features

- Import an image and a logo (supports PNG, JPG, etc.)
- Drag the logo manually or tile it over the image
- Adjust:
  - Rotation
  - Scale
  - Spacing (for tiled mode)
  - Opacity
- Save the final watermarked image

## 🛠 Technologies

- Python 3.x
- `customtkinter`
- `Pillow` (PIL)

## 🚀 Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/h2o-maker.git
cd h2o-maker
```

2. (Optional) Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python main.py
```

### Packaging as Executable

You can generate an executable using:

```bash
pyinstaller main.spec
```

This will generate the app inside the `dist/` folder.

## 📦 Folder Structure

```
h2o-maker/
│
├── main.py                # Main application logic
├── image_widgets.py       # Widget components for GUI
├── settings.py            # Constants and configurations
├── main.spec              # PyInstaller build config
├── requirements.txt
└── README.md
```

## 📄 License

This project is licensed under the MIT License. Feel free to use and modify it.

---

Created with ❤️ by Juan Silva.
