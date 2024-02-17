from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def french_word():
    global current_card, flip_timer
    windows.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(canvas_image, image=card_front)
    canvas.itemconfig(title_text, text="French", fill="black")
    canvas.itemconfig(new_word, text=current_card["French"], fill="black")
    flip_timer = windows.after(3000, count_down)


def count_down():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfigure(title_text, text="English", fill="white")
    canvas.itemconfigure(new_word, text=current_card["English"], fill="white")


def onclick():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    french_word()


windows = Tk()
windows.minsize(width=800, height=526)
windows.title("Flashy Flash Cards")
windows.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = windows.after(3000, count_down)

canvas = Canvas(width=820, height=540, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = PhotoImage(file="card_front.png")
canvas_image = canvas.create_image(415, 270, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)

title_text = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
new_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))

card_back = PhotoImage(file="card_back.png")
right = PhotoImage(file="right.png")
wrong = PhotoImage(file="wrong.png")

right_button = Button(image=right, highlightthickness=0, command=onclick)
right_button.grid(column=1, row=1)
right_button.config(padx=50, pady=50)

wrong_button = Button(image=wrong, highlightthickness=0, command=french_word)
wrong_button.grid(column=0, row=1)
wrong_button.config(padx=50, pady=50)

french_word()

mainloop()
