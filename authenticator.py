import os
import sys
import tkinter as tk
from tkinter import *
from tkinter import font, messagebox
from openai import OpenAI, AuthenticationError

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


def open_void_window(parent_root):
    voidWindow = tk.Toplevel(parent_root)
    voidWindow.title("THE VOID - CONTACT")
    voidWindow.geometry("800x700+20+20")
    voidWindow.resizable(False, False)
    voidWindow.configure(bg=background_colour, cursor=void_cursor)
    voidWindow.iconbitmap(void_icon)

    width, height = 800, 700
    canvas = tk.Canvas(voidWindow, width=width, height=height, highlightthickness=0, bg=background_colour)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    canvas.create_rectangle(0, 0, width, height, fill=background_colour, outline="")

    for i in range(-100, height + 100, 15):
        factor = max(0.0, min(1.0, (i / height))) ** 4
        colour = interpolate_color(background_colour, foreground_colour, factor)
        canvas.create_line(-100, i, width + 100, i - 60, fill=colour, width=60)

    # Rest of code for layout of AI and having the AI respond
 



# Colours
background_colour = "#1E0824"
foreground_colour = "#00CED1"
active_background_colour = "#C766D8"
active_foreground_colour = "#E0B0FF"

# Cursor path and Icon
void_cursor_path = resource_path("void-cursor.cur").replace(os.sep, '/')
void_cursor = f"@{void_cursor_path}"
void_icon = resource_path('void-icon.ico')

#Default API Key
api_key = ""
api_key_submitted = False

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
popup_text_font = font.Font(family="Consolas", size=10)
popup_btn_font = font.Font(family="Consolas", size=11, underline=True)

# Labels and Buttons
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
continueRootButton = Button(root,
    text="CONTINUE TO VOID",
    font=buttonFont,
    command=lambda: [open_void_window(root)],
    bg=foreground_colour,
    fg=background_colour,
    activebackground=active_background_colour,
    activeforeground=active_foreground_colour,
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

# Create Canvas Windows (Initialise Widgets) - Assign Continue Button to a Function
def instantiate_continue_button():
    canvas.create_window(400, 450, window=continueRootButton, tags="continue_button")

canvas.create_window(400, 530, window=closeRootButton)


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
        width // 2, 187,
        text="Back on Earth at the Void Science division of the Global Space Agency (GSA), we discovered an endless void just hanging out in space. Of course, being the curious " \
        "creatures that we are, we approached the Void via an intercept with the ISS, where a small space module fired out of it in order to reach the Void. Our signal antenna " \
        "that was supposed to be used for backup communications on Earth was transmitting to the Void and recieving transmissions back. Over the course of a few months, a reliable " \
        "language was established between us humans and the Void, and that language was (conveniently known as) English. Now, you are the first non-scientist human to take part " \
        "in this experiment of general communications with extraterrestrial beings, aka chatting with aliens. However, since this communications software is proprietary and open-soure, " \
        "we require you to authenticate yourself with a self-generated Access Token which you can enter on the main page of this software. This is all that we here at GSA are allowed to " \
        "disclose to you, so good luck on your communications and we will see you when you report back!",
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
        width // 2, 120, 
        text="This app basically works by using an AI with a set of rules to respond to user queries about an in game universe. In order to talk with the AI, on the main screen, click 'Information' at the top "
        "and go to 'Authenticate User' and it will take you to a new window with a text box that asks you to 'Authenticate Token', here you put in your AI's (ChatGPT-4o-mini) API key. If you are a teenager with "
        "Hackclub (hackclub.com), then you can go to ai.hackcklub.com and sign in with Hackclub to get $3.00 USD of AI use every day. The model in use for this app is ChatGPT-4o-mini. All API keys must be from "
        "Hackclub API, if it is not, then the key will be rejected!",
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

def open_authenticate_popup(parent_window):
        
    def handle_api_submission():
        global api_key
        global api_key_submitted
        api_key = api_entry.get().strip()
        api_key_submitted = True
        confirm_correct_api_key_format()


    authPopup = tk.Toplevel(parent_window)
    authPopup.title("AUTHENTICATE USER")
    authPopup.geometry("600x400+400+300")
    authPopup.resizable(False, False)
    authPopup.configure(bg=background_colour, cursor=void_cursor)
    authPopup.iconbitmap(void_icon)

    width, height = 600, 400
    canvas = tk.Canvas(authPopup, width=width, height=height, highlightthickness=0, bg=background_colour)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    canvas.create_rectangle(0, 0, width, height, fill=background_colour, outline="")

    for i in range(100, height + 100, 30):
        factor = max(0.0, min(1.0, (i / height))) ** 5
        colour = interpolate_color(background_colour, foreground_colour, factor)
        canvas.create_line(-100, i, width + 100, i + 60, fill=colour, width=60)

    canvas.create_text(
        width // 2, 40,
        text="AUTHENTICATE TOKEN",
        font=popup_title_font,
        fill=active_foreground_colour,
        justify="center"
    )

    canvas.create_text(
        width // 2, 120,
        text="Authenticate User Here - Enter Token:",
        font=descriptionFont,
        fill=active_foreground_colour,
        width=520,
        justify="center"
    )

    auth_exit_btn = Button(authPopup,
        text="CLOSE WINDOW",
        font=popup_btn_font,
        command=authPopup.destroy,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )

    api_var = tk.StringVar()

    def on_key_change(*args):
        global api_key_submitted
        if api_key_submitted:
            api_key_submitted = False

    api_var.trace_add("write", on_key_change)

    api_entry = Entry(authPopup,
        textvariable=api_var,
        font=descriptionFont,
        bg="#1E0824",
        fg=active_foreground_colour,
        insertbackground="white",
        width=35
    )

    api_confirm = Button(authPopup,
        text="CONFIRM TOKEN",
        font=popup_btn_font,
        command=lambda: [handle_api_submission(), authPopup.destroy()],
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )

    canvas.create_window(width // 2, 200, window=api_entry, height=30)
    canvas.create_window(width // 2, 275, window=api_confirm)
    canvas.create_window(width // 2, 350, window=auth_exit_btn)


def show_continue_button():
    if api_key_submitted:
        if not canvas.find_withtag("continue_button"):
            instantiate_continue_button()
    else:
        canvas.delete("continue_button")

    root.after(300, show_continue_button)

show_continue_button()


def confirm_correct_api_key_format():
    global api_key_submitted

    # Check to see if API Key is in valid Hackclub format 
    if not api_key.startswith("sk-hc-v1-"):
        api_key_submitted = False
        messagebox.showerror("Key Rejected", "Your API Key format is not the right Hackclub format ('sk-hc-v1-'). Check the 'How It Works' tab for more inforamtion!")
        return

    try:
        # Point OpenAI client to Hackclubs Proxy
        client = OpenAI(base_url="https://ai.hackclub.com/proxy/v1", api_key=api_key)

        # Send a low-cost 'ping' to the AI to see if it responds
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[{"role": "user", "content": "ping"}],
            max_tokens = 5
        )

        # If the AI responds (No Error), then tell the user so
        api_key_submitted = True
        messagebox.showinfo("API Key Accepted", "Your authentication credentials have been accepted! Connection to the Void is now stable!")
    except AuthenticationError:
        # If Hackclub / OpenRouter rejects the key
        api_key_submitted = False
        messagebox.showerror("API Key Rejected - Authentication Failed", "Your authentication credentials were rejected by the server. Please check that your details are correct!")
    except Exception as e:
        # Triggered if there is another error (general)
        api_key_submitted = False
        messagebox.showerror("Connection Error", f"Could not connect to the Void. Error Code: {str(e)}")



menubar = tk.Menu(root)
infoMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Information", menu=infoMenu)
infoMenu.add_command(label="Lore", command=lambda: open_lore_popup(root))
infoMenu.add_command(label="How It Works", command=lambda: open_info_popup(root))
infoMenu.add_command(label="Authenticate User", command=lambda: open_authenticate_popup(root))

#Initialise Root Window
root.config(menu=menubar)
root.mainloop()
