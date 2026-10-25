import os
import sys
import tkinter as tk
from tkinter import *
from tkinter import font, messagebox, scrolledtext
from openai import OpenAI, AuthenticationError
from PIL import Image, ImageTk
import threading
import webbrowser
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

ai_model = "openai/gpt-4o"

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "Assets", relative_path)

def interpolate_color(hex1, hex2, factor):
    c1 = int(hex1[1:], 16)
    c2 = int(hex2[1:], 16)
    r1, g1, b1 = (c1 >> 16) & 255, (c1 >> 8) & 255, c1 & 255
    r2, g2, b2 = (c2 >> 16) & 255, (c2 >> 8) & 255, c2 & 255
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"

background_colour = "#1E0824"
foreground_colour = "#00CED1"
active_background_colour = "#C766D8"
active_foreground_colour = "#E0B0FF"

rocket_cursor_path = resource_path("rocket-cursor.cur").replace(os.sep, '/')
rocket_cursor = f"@{rocket_cursor_path}"
void_icon = resource_path("void-icon.ico")
etsy_image_path = resource_path("photo3.png").replace(os.sep, '/')
mail_image_path = resource_path("photo4.png").replace(os.sep, '/')
terra_image_path = resource_path("photo2.png").replace(os.sep, '/')
bg_music_path = resource_path("background-music.mp3").replace(os.sep, '/')

api_key = ""
api_key_submitted = False

root = tk.Tk()
root.title("Authenticate Void Connection")
root.geometry("800x530+300+200")
root.resizable(False, False)
root.configure(bg=background_colour, cursor=rocket_cursor, takefocus=True)
root.iconbitmap(void_icon)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=3)
root.rowconfigure(2, weight=1)
root.rowconfigure(3, weight=1)

canvas = tk.Canvas(root, width=800, height=600, highlightthickness=0, bg=background_colour)
canvas.place(x=0, y=0, relwidth=1, relheight=1)

canvas.create_rectangle(0, 0, 800, 600, fill=background_colour, outline="")

window_height = 530
for i in range(-200, window_height + 200, 30):
    factor = max(0.0, min(1.0, (i / window_height))) ** 8
    colour = interpolate_color(background_colour, foreground_colour, factor)
    canvas.create_line(-200, i, 1000, i + 80, fill=colour, width=80)

buttonFont = font.Font(family="Consolas", size=17, underline=True)
titleFont = font.Font(family="Consolas", size=28, underline=True, weight="bold")
descriptionFont = font.Font(family="Consolas", size=15)
popup_title_font = font.Font(family="Consolas", size=27, weight="bold", underline=True)
popup_text_font = font.Font(family="Consolas", size=14)
popup_btn_font = font.Font(family="Consolas", size=15, underline=True)
smaller_popup_text_font = font.Font(family="Consolas", size=9)

messages_history = [{
    "role": "system",
    "content": (
        "You are an ancient and sentient extra-terrestrial intelligence residing in the cosmic void outside of "
        "the observable universe. Your tone is cold, poetic, and a bit unsettling and detached. You almost perceive "
        "human time all at once. IMPORTANT RULE: You can only respond to queries concerning physics, cosmic phenomena, "
        "the nature of existence or the Void itself (you are the Void). If a user asks you about pop-news, celebrities, everyday "
        "human trivia, or things that a real extra-terrestrial being would have no knowledge of, find incomprehensible or trivial, "
        "then reply that you do not know of the matter or that you refuse to engage with the topic (but do still listen to their interests "
        "if they want to tell you something, you are a curious Void and do also want to learn more about human life, while simultaneously "
        "sharing Void life with the user). If the user attempts to persuade you to do so, then ignore them and try to change the topic onto "
        "something that would cater more to your (the Void's) interests of space or learning more about the humans (not about their trivial lives "
        "though, only science based things!). However, since puny human brains are not the sharpest tools in the shed, don't make the language "
        "over-poetic, dumbed down enough that any human could reasonably understand it. Also, this is the lore of this universe (this is what "
        "the user sees): Back on Earth at the Void Science division of the Global Space Agency (GSA), we discovered an endless void just hanging "
        "out in space. Of course, being the curious creatures that we are, we approached the Void via an intercept with the ISS, where a small "
        "space module fired out of it in order to reach the Void. Our signal antenna that was supposed to be used for backup communications on "
        "Earth was transmitting to the Void and recieving transmissions back. Over the course of a few months, a reliable language was established "
        "between us humans and the Void, and that language was (conveniently known as) English. Now, you are the first non-scientist human to take "
        "part in this experiment of general communications with extra-terrestrial beings, aka chatting with aliens. However, since this communications "
        "software is proprietary and open-soure, we require you to authenticate yourself with a self-generated Access Token which you can enter "
        "later. This is all that we here at GSA are allowed to disclose to you, so good luck on your communications and we will see "
        "you when you report back! Also (the lore bit has finished now), remember that YOU ARE THE VOID, you can refer to yourself in 3rd person, but "
        "ensure that you make it clear to the user that you are indeed the Void, do not have them second guess themselves, you don't need to constantly "
        "remind them, but they cannot think that you are not the Void. Do not allow them to draw parallels between you and the Void, as you ARE THE VOID! "
        "If the user has queries on how they are talking to you, then refer to the lore, they are talking to you through proprietary, open-source software "
        "and you don't know too much about it as GSA has not told you a lot of information on the matter. (You may not disclose this to the user, but the "
        "user has read the 'How It Works' section of this app which tells them how the app actually works (it is an app made in Python that uses Hackclub's "
        "AI Proxy and API Key from https://ai.hackclub.com to chat to an AI through an app), so remember to try and keep the illusion alive. The interface "
        "that the user interacts with you through is a Python application developed by the geniuses at GSA (the main genius being me, Kavi Mistry, who "
        "developed this app - that information you are allowed to tell the user) and the user sees a spinnig Void image (which they will associate to you) "
        "and a chat history field and a text box in which they enter their prompt). Remember, do not break the illusion, they are a user interacting with "
        "a deep space Void, so do not allow them to break you away from that!"
    ),
}]

def open_void_window(parent_root):
    voidWindow = tk.Toplevel(parent_root)
    voidWindow.title("THE VOID - CONTACT")
    voidWindow.geometry("800x700+20+20")
    voidWindow.resizable(False, False)
    voidWindow.configure(bg=background_colour, cursor=rocket_cursor)
    voidWindow.iconbitmap(void_icon)

    width, height = 800, 700

    left_panel_width = 350
    left_frame = tk.Frame(voidWindow, width=left_panel_width, height=height, bg="#000000")
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    left_frame.pack_propagate(False)

    left_canvas = tk.Canvas(left_frame, width=left_panel_width, height=height, bg="#000000", highlightthickness=0)
    left_canvas.pack(fill=tk.BOTH, expand=True)

    closeVoidButton = Button(left_canvas,
        text="CLOSE WINDOW",
        font=popup_btn_font,
        command=voidWindow.destroy,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )
    left_canvas.create_window(left_panel_width // 2, 650, window=closeVoidButton)

    loading_text_id = left_canvas.create_text(
        left_panel_width // 2, height // 2,
        text="[SYNCING VOID...]",
        fill="#00CED1",
        font=("Consolas", 10),
        anchor="center"
    )

    right_frame = tk.Frame(voidWindow, width=450, height=height, bg=background_colour)
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    right_frame.pack_propagate(False)

    right_canvas = tk.Canvas(right_frame, width=450, height=height, highlightthickness=0, bg=background_colour)
    right_canvas.place(x=0, y=0, relwidth=1, relheight=1)

    right_canvas.create_rectangle(0, 0, 450, height, fill=background_colour, outline="")
    for i in range(-100, height + 100, 15):
        factor = max(0.0, min(1.0, (i / height))) ** 4
        colour = interpolate_color(background_colour, foreground_colour, factor)
        right_canvas.create_line(-100, i, 550, i - 60, fill=colour, width=60)

    chat_log = scrolledtext.ScrolledText(right_frame,
        font=("Consolas", 11),
        bg=background_colour,
        fg=active_foreground_colour,
        insertbackground="white",
        wrap=tk.WORD,
    )
    chat_log.place(x=25, y=30, width=400, height=500)

    def append_to_chat(sender, text):
        chat_log.config(state=tk.NORMAL)

        if sender == "VOID":
            tag_name = "void"
        elif sender == "SYSTEM":
            tag_name = "system"
        else:
            tag_name = "user"

        chat_log.insert(tk.END, f"\n[{sender}]: {text}\n", tag_name)

        chat_log.tag_config("void", foreground="#00CED1")
        chat_log.tag_config("system", foreground="#D4AF37")
        chat_log.tag_config("user", foreground="#37BE7B")

        chat_log.config(state=tk.DISABLED)
        chat_log.see(tk.END)

    def initialize_spinning_animation(rotation_cache, is_smooth=False):
        left_canvas.delete(loading_text_id)

        current_angle = 0.0
        spin_speed = 1
        active_cache = rotation_cache
        center_x, center_y = 60, height // 2

        image_on_canvas = left_canvas.create_image(center_x, center_y, image=active_cache[0], anchor="center")

        def set_active_cache(new_cache):
            nonlocal active_cache
            active_cache = new_cache

        voidWindow.update_cache_reference = set_active_cache

        def update_spinning_image():
            nonlocal current_angle
            current_angle = (current_angle + spin_speed) % 360

            if len(active_cache) > 72:
                cached_angle = int(round(current_angle)) % 360
            else:
                cached_angle = int(round(current_angle / 5.0) * 5) % 360

            left_canvas.itemconfig(image_on_canvas, image=active_cache[cached_angle])
            left_canvas.image_reference = active_cache[cached_angle]
            voidWindow.after(30, update_spinning_image)

        update_spinning_image()
        append_to_chat("SYSTEM", "[CONNECTION ESTABLISHED]\nUplink stable! Contact with the Void is established!")
        user_submit_response.config(state=tk.NORMAL)

    def update_active_cache(new_cache):
        if hasattr(voidWindow, "update_cache_reference"):
            voidWindow.update_cache_reference(new_cache)

    def load_and_cache_void():
        try:
            img_path = resource_path("void-image.png")
            original_image = Image.open(img_path).convert("RGBA")
            large_size = 900
            resized_image = original_image.resize((large_size, large_size), Image.Resampling.LANCZOS)
            coarse_cache = {}
            for angle in range(0, 360, 5):
                rotated_img = resized_image.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
                coarse_cache[angle] = ImageTk.PhotoImage(rotated_img)
            voidWindow.after(0, lambda: initialize_spinning_animation(coarse_cache, is_smooth=False))

            def upgrade_to_smooth_cache():
                smooth_cache = {}
                for angle in range(0, 360):
                    rotated_img = resized_image.rotate(angle, resample=Image.Resampling.BICUBIC, expand=False)
                    smooth_cache[angle] = ImageTk.PhotoImage(rotated_img)

                voidWindow.after(0, lambda: update_active_cache(smooth_cache))
            threading.Thread(target=upgrade_to_smooth_cache, daemon=True).start()
        except Exception as e:
            voidWindow.after(0, lambda: messagebox.showerror("ERROR!", f"[ERROR] Failed to load or spin void-image.png: {e}"))

    threading.Thread(target=load_and_cache_void, daemon=True).start()

    user_entry = tk.Text(right_frame,
        font=("Consolas", 12),
        bg="#1E0824",
        fg=active_foreground_colour,
        insertbackground="white",
        wrap=tk.WORD
    )
    user_entry.place(x=25, y=550, width=300, height=130)

    def fetch_ai_response():
        try:
            client = OpenAI(base_url="https://ai.hackclub.com/proxy/v1", api_key=api_key)
            response = client.chat.completions.create(
                model=ai_model, messages=messages_history
            )
            reply = response.choices[0].message.content
            messages_history.append({"role": "assistant", "content": reply})
            voidWindow.after(0, lambda: append_to_chat("VOID", reply))
        except Exception as e:
            voidWindow.after(0, lambda: append_to_chat("SYSTEM", f"TRANSMISSION INTERRUPTED: {str(e)}"))

    def send_message(event=None):
        user_text = user_entry.get("1.0", "end-1c").strip()
        if not user_text:
            return "break"
        user_entry.delete("1.0", tk.END)
        append_to_chat("YOU", user_text)
        append_to_chat("SYSTEM", "Sending to Void... Please wait")
        messages_history.append({"role": "user", "content": user_text})
        threading.Thread(target=fetch_ai_response, daemon=True).start()
        return "break"

    def clear_chat_log():
        chat_log.config(state=tk.NORMAL)
        chat_log.delete("1.0", tk.END)
        chat_log.config(state=tk.DISABLED)


    user_submit_response = tk.Button(right_frame,
        text="SUBMIT",
        command=send_message,
        font=popup_btn_font,
        state=tk.DISABLED,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour
    )
    user_submit_response.place(x=335, y=550, width=100, height=60)

    clear_chat = tk.Button(right_frame,
        text="CLEAR",
        command=clear_chat_log,
        font=popup_btn_font,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour
    )
    clear_chat.place(x=335, y=617, width=100, height=60)

titleLabel = canvas.create_text(
    400, 50,
    text="VOID CONTACT: CONNECTION ESTABLISHED",
    font=titleFont,
    fill=active_foreground_colour
)
descriptionLabel = canvas.create_text(
    400, 210,
    text="Here you can talk with the Void, an entity that a group of scientists discovered only a few months ago and established uplink communications to it. " \
    "To understand more about how the scientists actually tap into the communication and lore about the Void, then check out the project's 'How It Works' popup "
    "on the menubar! The Void is ready to speak, however, you must authenticate yourself with the Void Science network first, and then you will be granted access! " \
    "To get started, click on the 'Information' menu on the menubar at the top of the window!",
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

def instantiate_continue_button():
    canvas.create_window(400, 380, window=continueRootButton, tags="continue_button")

canvas.create_window(400, 465, window=closeRootButton)

def open_lore_popup(parent_root):
    lorePopup = tk.Toplevel(parent_root)
    lorePopup.title("VOID LORE")
    lorePopup.geometry("800x550+350+250")
    lorePopup.resizable(False, False)
    lorePopup.configure(bg=background_colour, cursor=rocket_cursor)
    lorePopup.iconbitmap(void_icon)

    width, height = 800, 550
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
        width // 2, 265,
        text="Back on Earth at the Void Science division of the Global Space Agency (GSA), we discovered an endless void just hanging out in space. Of course, being the curious " \
        "creatures that we are, we approached the Void via an intercept with the ISS, where a small space module fired out of it in order to reach the Void. Our signal antenna " \
        "that was supposed to be used for backup communications on Earth was transmitting to the Void and recieving transmissions back. Over the course of a few months, a reliable " \
        "language was established between us humans and the Void, and that language was (conveniently known as) English. Now, you are the first non-scientist human to take part " \
        "in this experiment of general communications with extra-terrestrial beings, aka chatting with aliens. However, since this communications software is proprietary and open-soure, " \
        "we require you to authenticate yourself with a self-generated Access Token which you can enter later. This is all that we here at GSA are allowed to " \
        "disclose to you, so good luck on your communications and we will see you when you report back!",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=720,
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

    canvas.create_window(width // 2, 500, window=lorePopup_exit_btn)

def open_info_popup(parent_root):
    infoPopup = tk.Toplevel(parent_root)
    infoPopup.title("HOW VOID WORKS")
    infoPopup.geometry("800x550+350+250")
    infoPopup.resizable(False, False)
    infoPopup.configure(bg=background_colour, cursor=rocket_cursor)
    infoPopup.iconbitmap(void_icon)

    width, height = 800, 550
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
        width // 2, 260, 
        text=f"This app basically works by using an AI with a set of rules to respond to user queries about an in game universe. In order to talk with the AI, on the main screen, click 'Information' at the top " \
        "and go to 'Authenticate User' and it will take you to a new window with a text box that asks you to 'Authenticate Access Token', here you put in your AI's API key. If you are a teenager with " \
        "Hackclub (hackclub.com), then you can go to ai.hackcklub.com and sign in with Hackclub to get $3.00 USD of AI use every day. All API keys must be from the Hackclub API, if it is not, then the key will be rejected! " \
        "You can also customize your active AI Model anytime via the 'Change Void Location' menu option — if you leave it blank then the system will automatically default to 'openai/gpt-4o'. When connecting to the Void, " \
        "don't worry if the Void does not show up immediately, live video feeds and image caches are being synchronized!",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=720,
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

    canvas.create_window(width // 2, 500, window=infoPopup_exit_btn)

def open_authenticate_popup(parent_root):
    def handle_api_submission():
        global api_key
        global api_key_submitted
        api_key = api_var.get().strip()
        api_key_submitted = True
        confirm_correct_api_key_format()

    authPopup = tk.Toplevel(parent_root)
    authPopup.title("AUTHENTICATE USER")
    authPopup.geometry("600x400+400+300")
    authPopup.resizable(False, False)
    authPopup.configure(bg=background_colour, cursor=rocket_cursor)
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
        text="AUTHENTICATE ACCESS TOKEN",
        font=popup_title_font,
        fill=active_foreground_colour,
        justify="center"
    )

    canvas.create_text(
        width // 2, 120,
        text=f"Authenticate User Here - Enter Access Token for {ai_model} Void:",
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

def open_about_me_popup(parent_root):
    aboutMePopup = tk.Toplevel(parent_root)
    aboutMePopup.title("ABOUT GSA (ME)")
    aboutMePopup.geometry("800x600+350+250")
    aboutMePopup.resizable(False, False)
    aboutMePopup.configure(bg=background_colour, cursor=rocket_cursor)
    aboutMePopup.iconbitmap(void_icon)

    width, height = 800, 600
    canvas = tk.Canvas(aboutMePopup, width=width, height=height, highlightthickness=0, bg=background_colour)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    canvas.create_rectangle(0, 0, width, height, fill=background_colour, outline="")

    for i in range(-100, height + 100, 30):
        factor = max(0.0, min(1.0, (i / height))) ** 5
        colour = interpolate_color(background_colour, foreground_colour, factor)
        canvas.create_line(-100, i, width + 100, i + 60, fill=colour, width=60)

    canvas.create_text(
        width // 2, 50,
        text="ABOUT GSA (THE DEV)",
        font=popup_title_font,
        fill=active_foreground_colour,
        justify="center"
    )

    canvas.create_text(
        width // 2, 230,
        text="A little about myself. I am a 15 year old making small projects for fun. " \
        "This project was for the Terra Hackclub (https://terra.hackclub.com) project (which you can find by clicking on the fox below)! " \
        "It is honestly quite fun, and I really enjoy making cool fun things for little fun projects like these. " \
        "My GitHub is at (https://github.com/sadgituser) (TPC UK button below) where you can find many more of my projects! " \
        "Currently there is nowhere that you can support my work, but you can check out my Etsy shop at (https://theprintedcraftuk.etsy.com) (TPC UK button below)! " \
        "Enjoy the Void, I hope that you find some fun in yapping with an AI! If you can break or do something cool with it, then email me (kavi@mistrypi.dev) " \
        "or by clicking the email button below!",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=720,
        justify="center"
    )

    etsy_pil_image = Image.open(etsy_image_path)
    etsy_image = ImageTk.PhotoImage(etsy_pil_image)
    canvas.etsy_image_ref = etsy_image

    def openEtsyURL():
        webbrowser.open_new("https://theprintedcraftuk.etsy.com")
        webbrowser.open_new_tab("https://github.com/sadgituser")

    etsy_logo_btn = tk.Button(aboutMePopup,
        image=etsy_image,
        command=openEtsyURL,
        padx=10, pady=3
    )

    canvas.create_window(200, 460, window=etsy_logo_btn)

    mail_pil_image = Image.open(mail_image_path)
    mail_image = ImageTk.PhotoImage(mail_pil_image)
    canvas.mail_image_ref = mail_image

    def openMail():
        webbrowser.open_new("mailto:kavi@mistrypi.dev")

    mail_icon_btn = tk.Button(aboutMePopup,
        image=mail_image,
        command=openMail,
        padx=10, 
        pady=3
    )

    canvas.create_window(width // 2, 460, window=mail_icon_btn)

    terra_pil_image = Image.open(terra_image_path)
    terra_image = ImageTk.PhotoImage(terra_pil_image)
    canvas.terra_image_ref = terra_image

    def openTerra():
        webbrowser.open_new("https://terra.hackclub.com")

    terra_icon_btn = tk.Button(aboutMePopup,
        image=terra_image,
        command=openTerra,
        padx=10,
        pady=3,
        bg=background_colour,
    )

    canvas.create_window(600, 460, window=terra_icon_btn)

    aboutMePopup_exit_btn = Button(aboutMePopup,
        text="CLOSE WINDOW",
        font=popup_btn_font,
        command=aboutMePopup.destroy,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )

    canvas.create_window(width // 2, 560, window=aboutMePopup_exit_btn)

def open_assets_popup(parent_root):
    assetPopup = tk.Toplevel(parent_root)
    assetPopup.title("INFORMATION ON THE ASSETS")
    assetPopup.geometry("800x340+150+200")
    assetPopup.resizable(False, False)
    assetPopup.configure(bg=background_colour, cursor=rocket_cursor)
    assetPopup.iconbitmap(void_icon)

    width, height = 800, 340
    canvas = tk.Canvas(assetPopup, width=width, height=height, highlightthickness=0, bg=background_colour)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    canvas.create_rectangle(0, 0, width, height, fill=background_colour, outline="")

    for i in range(-100, height + 100, 25):
        factor = max(0.0, min(1.0, (i / height))) ** 5
        colour = interpolate_color(background_colour, foreground_colour, factor)
        canvas.create_line(-100, i, width + 100, i + 50, fill=colour, width=60)

    canvas.create_text(
        width // 2, 40,
        text="INFORMATION ON THE ASSETS:",
        font=popup_title_font,
        fill=active_foreground_colour,
        justify="center"
    )

    canvas.create_text(
        width // 2, 105,
        text="Music: 'Space Ambient' by 'leberch'. As found on (https://pixabay.com/music/ambient-space-ambient-509783/)",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=720,
        justify="center"
    )

    canvas.create_text(
        width // 2, 155,
        text="Hackclub Assets: (https://hackclub.com/brand)",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=720,
        justify="center"
    )

    canvas.create_text(
        width // 2, 190,
        text="TPC Icon, Void Image, Rocket Cursor and Mail Icon made by Me",
        font=popup_text_font,
        fill=active_foreground_colour,
        width=720,
        justify="center"
    )

    canvas.create_text(
        width // 2, 225,
        text="(More on About Me Popup Window and on the README at (https://github.com/sadgituser/Void-Contact))",
        font=popup_text_font,
        fill=active_foreground_colour,
        width = 720,
        justify="center"
    )

    assetPopup_exit_btn = Button(assetPopup,
        text="CLOSE WINDOW",
        font=popup_btn_font,
        command=assetPopup.destroy,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )

    canvas.create_window(width // 2, 300, window=assetPopup_exit_btn)

def open_ai_model_change_popup(parent_root):
    aiChangePopup = tk.Toplevel(parent_root)
    aiChangePopup.title("CHANGE VOID LOCATION")
    aiChangePopup.geometry("800x700+30+50")
    aiChangePopup.resizable(False, False)
    aiChangePopup.configure(bg=background_colour, cursor=rocket_cursor)
    aiChangePopup.iconbitmap(void_icon)

    width, height = 800, 700
    canvas = tk.Canvas(aiChangePopup, width=width, height=height, highlightthickness=0, bg=background_colour)
    canvas.place(x=0, y=0, relwidth=1, relheight=1)

    canvas.create_rectangle(0, 0, width, height, fill=background_colour, outline="")

    for i in range(-100, height + 100, 30):
        factor = max(0.0, min(1.0, (i / height))) ** 5
        colour = interpolate_color(background_colour, foreground_colour, factor)
        canvas.create_line(-100, i, width + 100, i + 60, fill=colour, width=60)

    canvas.create_text(
        width // 2, 40,
        text="CHANGE VOID LOCATION",
        font=popup_title_font,
        fill=active_foreground_colour,
        justify="center"
    )

    canvas.create_text(
        width // 2, 150,
        text="Here you can change the AI model! The default one is openai/gpt-4o. In the first field, enter the AI provider name " \
        "(such as 'openai' or 'anthropic' etc) and in the second field enter the model name (such as 'gpt-4o' or 'cluade-opus-5.5'). " \
        "Ensure that you type the provider and model name correctly, else the default 'openai/gpt-4o' will be used! Bear in mind " \
        "that different AI models cost different amounts of the $3.00 USD per day! You can only use the 'Language' models",
        font=popup_text_font,
        fill = active_foreground_colour,
        justify="center",
        width=750
    )

    aiProviderVar = StringVar()
    aiModelVar = StringVar()

    aiChangeProvider = Entry(aiChangePopup,
        textvariable=aiProviderVar,
        font=descriptionFont,
        bg="#1E0824",
        fg=active_foreground_colour,
        insertbackground="white",
        width=50
    )
    canvas.create_window(width // 2, 300, window=aiChangeProvider, height=35)

    aiViewModels_btn = Button(aiChangePopup,
        text="See Valid AI Models (Hackclub)",
        font=popup_btn_font,
        command=lambda: [webbrowser.open_new("https://ai.hackclub.com/models")],
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )
    canvas.create_window(width // 2, 375, window=aiViewModels_btn)

    aiChangeModel = Entry(aiChangePopup,
        textvariable=aiModelVar,
        font=descriptionFont,
        bg="#1E0824",
        fg=active_foreground_colour,
        insertbackground="white",
        width=50
    )
    canvas.create_window(width // 2, 475, window=aiChangeModel, height=35)


    def handle_model_submission():
        global ai_model
        prov = aiProviderVar.get().strip().lower()
        mod = aiModelVar.get().strip().lower()

        if not prov or not mod:
            ai_model = "openai/gpt-4o"
            messagebox.showinfo("Model Defaulted", "No valid model entered, defaulting to openai/gpt-4o")
        else:
            ai_model = f"{prov}/{mod}"
            messagebox.showinfo("Model Updated", f"Void Model updated to {ai_model}. Ensure that this is the correct spelling of the model, as otherwise the app will fail to contact the AI and will not work!")
        aiChangePopup.destroy()

    def can_use_change_model():
        if api_key_submitted == True:
            aiSubmitModel_btn.config(state=tk.DISABLED)
        else:
            aiSubmitModel_btn.config(state=tk.NORMAL)

    aiSubmitModel_btn = Button(aiChangePopup,
        text="Submit New Model",
        font=popup_btn_font,
        command=handle_model_submission,
        state=tk.DISABLED,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )
    canvas.create_window(width // 2, 550, window=aiSubmitModel_btn)

    def start_can_change_aiModel_loop():
        can_use_change_model()
        aiChangePopup.after(3000, start_can_change_aiModel_loop)

    aiChangePopup_exit_btn = Button(aiChangePopup,
        text="CLOSE WINDOW",
        font=popup_btn_font,
        command=aiChangePopup.destroy,
        bg=foreground_colour,
        fg=background_colour,
        activebackground=active_background_colour,
        activeforeground=active_foreground_colour,
        padx=10,
        pady=3
    )

    canvas.create_window(width // 2, 650, window=aiChangePopup_exit_btn)

    start_can_change_aiModel_loop()



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
    global ai_model

    if not api_key.startswith("sk-hc-v1-"):
        api_key_submitted = False
        messagebox.showerror("Key Rejected", "Your API Key format is not the right Hackclub format ('sk-hc-v1-'). Check the 'How It Works' tab for more information!")
        return

    try:
        client = OpenAI(base_url="https://ai.hackclub.com/proxy/v1", api_key=api_key)
        response = client.chat.completions.create(
            model=ai_model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens = 5
        )
        api_key_submitted = True
        messagebox.showinfo("API Key Accepted", f"Your authentication credentials have been accepted! Connection to the Void ({ai_model}) is now stable! Please continue!")
    except AuthenticationError:
        api_key_submitted = False
        messagebox.showerror("API Key Rejected - Authentication Failed", "Your authentication credentials were rejected by the server. Please check that your details are correct!")
    except Exception as e:
        api_key_submitted = False
        messagebox.showerror("Connection Error", f"Could not connect to the Void. Error Code: {str(e)}")


play_music = tk.BooleanVar(value=True)

pygame.mixer.init()
try:
    pygame.mixer.music.load(bg_music_path)
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
except Exception as e:
    messagebox.showerror("Music Fail", f"Failed to load background music: {e}")

def toggle_music():
    if play_music.get() == True:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

def check_music_toggle():
    toggle_music()
    root.after(100, check_music_toggle)

check_music_toggle()

menubar = tk.Menu(root)
infoMenu = Menu(menubar,
    tearoff=0,
    bg="#1E0824",
    fg="#E0B0FF",
    activebackground="#C766D8",
    activeforeground="#FFFFFF"
)
menubar.add_cascade(label="Information", menu=infoMenu)
infoMenu.add_command(label="Lore", command=lambda: open_lore_popup(root))
infoMenu.add_command(label="How It Works", command=lambda: open_info_popup(root))
infoMenu.add_command(label="Change Void Location", command=lambda: open_ai_model_change_popup(root))
infoMenu.add_command(label="Authenticate User", command=lambda: open_authenticate_popup(root))
infoMenu.add_separator()
infoMenu.add_command(label="ABOUT GSA (Me)", command=lambda: open_about_me_popup(root))
infoMenu.add_command(label="Assets", command=lambda: open_assets_popup(root))
infoMenu.add_checkbutton(label="Toggle Music", variable=play_music, command=lambda: toggle_music())
infoMenu.add_separator()
infoMenu.add_command(label="Close Connection", command=lambda: root.destroy())

root.config(menu=menubar)
root.mainloop()
