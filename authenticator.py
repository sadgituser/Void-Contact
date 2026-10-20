import os
import sys
import tkinter as tk
from tkinter import *
from tkinter import font

def resource_path(relative_path):
    # Get paths to Assets, even when bundled as an app
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "Assets", relative_path)

def interpolate_color(hex1, hex2, factor):
    # Blend the colours
    c1 = int(hex1[1:], 16)
    c2 = int(hex2[1:], 16)
    r1, g1, b1 = (c1 >> 16) & 255, (c1 >> 8) & 255, c1 & 255
    r2, g2, b2 = (c2 >> 16) & 255, (c2 >> 8) & 255, c2 & 255
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

# Colours
background_colour = "#1E0824"
foreground_colour = "#00CED1"
active_background_colour = "#C766D8"
active_foreground_colour = "#E0B0FF"

# Cursor path and Icon
void_cursor_path = resource_path("void-cursor.cur").replace(os.sep, '/')
void_cursor = f"@{void_cursor_path}"
void_icon = resource_path('void-icon.ico')

# Root Window Settings
root = tk.Tk()
root.title("Authenticate Void Connection")
root.geometry("800x600+300+200")
root.resizable(False, False)
root.configure(bg=background_colour, cursor=void_cursor, takefocus=True)
root.iconbitmap(void_icon)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=3)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

# Canvas setup matching background color
canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0, bg=background_colour)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

# Solid base rectangle covering the window
canvas.create_rectangle(0, 0, 800, 600, fill=background_colour, outline="")

# Draw slanted gradient lines extending far past the screen edges
window_height = 600
for i in range(-200, window_height + 200, 30):
    # Gradient
    factor = max(0.0, min(1.0, (i / window_height))) ** 8
    color = interpolate_color(background_colour, foreground_colour, factor)
    canvas.create_line(-200, i, 1000, i + 80, fill=color, width=80)

# Fonts
buttonFont = font.Font(family="Consolas", size=16, underline=True)
titleFont = font.Font(family="Consolas", size=26, underline=True, weight="bold")
descriptionFont = font.Font(family="Consolas", size=14)
popup_title_font = font.Font(family="Consolas", size=18, weight="bold", underline=True)
popup_text_font = font.Font(family="Consolas", size=13)
popup_btn_font = font.Font(family="Consolas", size=11, underline=True)

# Labels and Button
titleLabel = canvas.create_text(
    400, 60,
    text="VOID CONTACT: CONNECTION ESTABLISHED",
    font=titleFont,
    fill=active_foreground_colour
)
descriptionLabel = canvas.create_text(
    400, 250,
    text="Here you can talk with the Void, an entity that a group of scientists discovered only a few months ago and established uplink communications to it. " \
    "To understand more about how the scientists actually tap into the communication and lore about the Void, then check out the project's Info page on the menubar! " \
    "The Void is ready to speak, however, you must authenticate yourself with the Void Science network first, and then you will be granted access!",
    font=descriptionFont,
    fill=active_foreground_colour,
    width=720,
    justify="center"
)
closeRootButton = Button(root,
    text="CLOSE CONNECTION",
    font=buttonFont,
    command=root.destroy,
    bg=foreground_colour,
    fg=background_colour,
    activebackground=active_background_colour,
    activeforeground=active_foreground_colour
)

# Create Canvas
canvas.create_window(400, 500, window=closeRootButton)


def open_lore_popup(parent_root):
    lorePopup = tk.Toplevel(parent_root)
    lorePopup.title("VOID LORE")
    lorePopup.geometry("600x400+350+250")
    lorePopup.resizable(False, False)
    lorePopup.configure(bg=background_colour, cursor=void_cursor)
    lorePopup.iconbitmap(void_icon)

    width, height = 600, 400
    canvas = tk.Canvas(lorePopup, width=width, height=height, highlightthickness=0, bg=background_colour)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    canvas.create_rectangle(0, 0, width, height, fill=background_colour, outline="")

    for i in range(-100, height + 100, 30):
        factor = max(0.0, min(1.0, (i / height))) ** 5
        colour = interpolate_color(background_colour, foreground_colour, factor)
        canvas.create_line(-100, i, width + 100, i + 60, fill=colour, width=60)

    canvas.create_text(
        width // 2, 40, 
        text="VOID SCIENCE: LORE",
        font=popup_title_font,
        fill=active_foreground_colour,
        justify="center"
    )

    canvas.create_text(
        width // 2, 100,
        text="Here I will put the lore of the app, but I will do that later!",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=520,
        justify="center"
    )

    lorePopup_exit_btn = Button(lorePopup,
        text="CLOSE WINDOW",
        font=popup_btn_font,
        command=lorePopup.destroy,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )

    canvas.create_window(width // 2, 350, window=lorePopup_exit_btn)

def open_info_popup(parent_root):
    infoPopup = tk.Toplevel(parent_root)
    infoPopup.title("HOW VOID WORKS")
    infoPopup.geometry("600x400+350+250")
    infoPopup.resizable(False, False)
    infoPopup.configure(bg=background_colour, cursor=void_cursor)
    infoPopup.iconbitmap(void_icon)

    width, height = 600, 400
    canvas = tk.Canvas(infoPopup, width=width, height=height, highlightthickness=0, bg=background_colour)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    canvas.create_rectangle(0, 0, width, height, fill=background_colour, outline="")

    for i in range(-100, height + 100, 30):
        factor = max(0.0, min(1.0, (i / height))) ** 5
        colour = interpolate_color(background_colour, foreground_colour, factor)
        canvas.create_line(-100, i, width + 100, i + 60, fill=colour, width=60)

    canvas.create_text(
        width // 2, 40,
        text="HOW THE VOID WORKS",
        font=popup_title_font,
        fill=active_foreground_colour,
        justify="center"
    )

    canvas.create_text(
        width // 2, 100, 
        text="Here I will put the description of how the app works, but I will come back to it later!",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=520,
        justify="center"
    )

    infoPopup_exit_btn = Button(infoPopup,
        text="CLOSE WINDOW",
        font=popup_btn_font,
        command=infoPopup.destroy,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10, 
        pady=3
    )

    canvas.create_window(width // 2, 350, window=infoPopup_exit_btn)


menubar = tk.Menu(root)
infoMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Information", menu=infoMenu)
infoMenu.add_command(label="Lore", command=lambda: open_lore_popup(root))
infoMenu.add_command(label="How It Works", command=lambda: open_info_popup(root))

#Initialise Root Window
root.config(menu=menubar)
root.mainloop()
