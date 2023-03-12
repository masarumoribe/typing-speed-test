from random_word import Wordnik
from tkinter import *
import time

BACKGROUND_COLOR = "#C3ACD0"

#Create random words class
r = Wordnik()

#Create a list of words
words = []

#Create score variable
score = 0

#Create function to keep track of time
def update_time(event):
    global start_time
    elpased_time = time.time() - start_time
    time_label.config(text=int(elpased_time))
    if elpased_time < 60:
        window.after(1000, update_time, event)
    else:
        input.config(state=DISABLED)
        wrong_word.config(text=f"Time's up! Your typing speed is {score} words per minute.")
        window.unbind("<space>")
        window.unbind("<Key>")

#Create random word
def generate_random_word():
    global word_id, word
    random_word = r.get_random_word(hasDictionaryDef="true", minCorpusCount=10, minDictionaryCount=10, maxLength=8)
    while random_word is None:
        random_word = r.get_random_word(hasDictionaryDef="true", minCorpusCount=10, minDictionaryCount=10, maxLength=8)
    word_id = canvas.create_text(200, 150, text=random_word, font=('Helvetica 24 bold'))
    words.append({'id': word_id, 'opacity': 1.0, 'y': 150})
    print(random_word)
    return random_word

#Create a function to compare the random word with the user input ionce the press space key
def space_clicked(event):
    global words, word, score
    print(words)
    input_word = input.get().strip()
    if input_word.lower() == word.lower():
        score += 1
        score_label.config(text=f'Score: {score}')
        print(input_word)
        print(word.lower())
        input.delete(0, "end")
        #Update the previous words opacities and y-positions
        for i, w in enumerate(words):
            w['y'] -= 40
            w['opacity'] -= 0.2
            canvas.itemconfig(w['id'], fill=f'grey{int(100*w["opacity"])}')
            canvas.coords(w['id'], 200, w['y'])
        #Remove the first word if its opacity is below a certain threshold
        if len(words) > 1 and words[0]['opacity'] < 0.1:
            canvas.delete(words[0]['id'])
            words = words[1:]
        word = generate_random_word()
        wrong_word.config(text="")
        
    else:
        wrong_word.config(text="Wrong spelling bitch!")

#Create and setup TKinter main window
window = Tk()
window.title("Typing Speed Test")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

canvas = Canvas(width=400, height=300, bd=4)
canvas.grid(row=0, column=0)

#Generate random word and print it
word = generate_random_word()

#Create label to keep track of time
time_label = Label(canvas, font=("Arial", 20))
canvas.create_window(100, 230, window=time_label)

#Create label for keeping the score
score_label = Label(canvas, text=f'Score: {score}', font=("Arial", 24))
canvas.create_window(300, 230, window=score_label)

#Create the text box for the user to type a word
input_frame = Frame(window, width=400, height=300, borderwidth=4, bg="#804674", padx= 107, pady=100)
input_frame.grid(row=1, column=0)

input = Entry(input_frame, bg="black")
input.grid(row=1, column=0)

#Create message when the word is wrongly typed
wrong_word = Label(input_frame, text="", bg="#804674")
wrong_word.grid(row=2, column=0)

#Bind the compare words after space click function to the entry widget
input.bind("<space>", space_clicked)

#Start the time counter
input.bind("<Key>", update_time)
start_time = time.time()

window.mainloop()