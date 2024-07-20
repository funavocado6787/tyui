from tkinter import *
from tkinter import messagebox as mb
import json

class AdminWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Admin Panel")
        self.master.geometry("300x150")

        self.label_username = Label(master, text="Username:")
        self.label_username.pack(pady=5)
        self.entry_username = Entry(master)
        self.entry_username.pack(pady=5)

        self.label_password = Label(master, text="Password:")
        self.label_password.pack(pady=5)
        self.entry_password = Entry(master, show="*")
        self.entry_password.pack(pady=5)

        self.button_login = Button(master, text="Login", command=self.login)
        self.button_login.pack(pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Check if username and password match the admin credentials
        if username == "admin" and password == "adminpassword":
            self.show_admin_options()
        else:
            mb.showerror("Error", "Invalid username or password")

    def show_admin_options(self):
        self.master.destroy()  # Close the admin login window

        # Create a new window for admin options
        admin_options_window = Tk()
        admin_options_window.title("Admin Options")
        admin_options_window.geometry("300x150")

        button_view_scores = Button(admin_options_window, text="View Scores", command=self.view_scores)
        button_view_scores.pack(pady=10)

        button_edit_questions = Button(admin_options_window, text="Edit Questions", command=self.edit_questions)
        button_edit_questions.pack(pady=10)

    def view_scores(self):
        try:
            with open('user_scores.json', 'r') as f:
                user_scores = json.load(f)
        except FileNotFoundError:
            mb.showerror("Error", "No scores found.")
            return

        # Create a new window to display scores
        score_window = Toplevel(self.master)
        score_window.title("Scores")

        # Display scores
        for username, data in user_scores.items():
            score_label = Label(score_window, text=f"{username}: {data['score']}")
            score_label.pack()

    def edit_questions(self):
        edit_window = Toplevel(self.master)
        edit_window.title("Edit Questions")
        edit_window.geometry("600x400")

        # Create widgets to edit questions
        label_title = Label(edit_window, text="Edit Questions", font=("Arial", 18, "bold"))
        label_title.pack(pady=10)

        # Add your editing components here, e.g., text boxes, buttons, etc.

class Quiz:
    def __init__(self, username):
        self.username = username
        self.q_no = 0
        self.display_title()
        self.display_question()
        self.opt_selected = IntVar()
        self.opts = self.radio_buttons()
        self.display_options()
        self.buttons()
        self.correct = 0
        self.data_size = len(question)

    def display_result(self):
        wrong_count = self.data_size - self.correct
        correct = f"Correct: {self.correct}"
        wrong = f"Wrong: {wrong_count}"
        score = int(self.correct / self.data_size * 100)
        result = f"Score: {score}%"
        mb.showinfo("Result", f"{result}\n{correct}\n{wrong}")
        self.save_score()

    def check_ans(self, q_no):
        if self.opt_selected.get() == answer[q_no]:
            return True

    def next_btn(self):
        if self.check_ans(self.q_no):
            self.correct += 1
        self.q_no += 1
        if self.q_no == self.data_size:
            self.display_result()
            gui.destroy()
        else:
            self.display_question()
            self.display_options()

    def buttons(self):
        next_button = Button(gui, text="Next", command=self.next_btn,
                             width=10, bg="blue", fg="white", font=("ariel", 16, "bold"))
        next_button.place(x=450, y=450)
        quit_button = Button(gui, text="Quit", command=gui.destroy,
                             width=5, bg="black", fg="white", font=("ariel", 16, " bold"))
        quit_button.place(x=900, y=550)

    def display_options(self):
        val = 0
        self.opt_selected.set(0)
        for option in options[self.q_no]:
            self.opts[val]['text'] = option
            val += 1

    def display_question(self):
        q_no = Label(gui, text=question[self.q_no], width=60,
                     font=('ariel', 16, 'bold'), anchor='w')
        q_no.place(x=70, y=100)

    def display_title(self):
        title = Label(gui, text="Mind Crafter's QUIZ",
                      width=60, bg="red", fg="white", font=("ariel", 20, "bold"))
        title.place(x=0, y=2)

    def radio_buttons(self):
        q_list = []
        y_pos = 150
        while len(q_list) < 4:
            radio_btn = Radiobutton(gui, text=" ", variable=self.opt_selected,
                                    value=len(q_list) + 1, font=("ariel", 14))
            q_list.append(radio_btn)
            radio_btn.place(x=100, y=y_pos)
            y_pos += 40
        return q_list

    def save_score(self):
        try:
            with open('user_scores.json', 'r') as f:
                user_scores = json.load(f)
        except FileNotFoundError:
            user_scores = {}

        if self.username not in user_scores:
            user_scores[self.username] = {'score': 0}

        user_scores[self.username]['score'] = int(self.correct / self.data_size * 100)

        with open('user_scores.json', 'w') as f:
            json.dump(user_scores, f)

def start_quiz(username):
    global gui
    gui_login.destroy()  # Destroy the login window
    gui = Tk()
    gui.geometry("1024x640")
    gui.title("Mind Crafter's Quiz")

    with open('data.json') as f:
        data = json.load(f)

    global question, options, answer
    question = data['question']
    options = data['options']
    answer = data['answer']

    quiz = Quiz(username)

def login():
    username = entry_username.get().strip()
    if username:
        start_quiz(username)
        gui.mainloop()  # Start the quiz mainloop
    else:
        mb.showerror("Error", "Username cannot be empty!")

def admin_login():
    admin_window = Tk()
    admin_window.title("Admin Login")
    admin_window.geometry("300x200")

    label_username = Label(admin_window, text="Username:")
    label_username.pack(pady=5)

    entry_username = Entry(admin_window)
    entry_username.pack(pady=5)

    label_password = Label(admin_window, text="Password:")
    label_password.pack(pady=5)

    entry_password = Entry(admin_window, show="*")
    entry_password.pack(pady=5)

    button_login = Button(admin_window, text="Login",
                          command=lambda: admin_authentication(entry_username.get(), entry_password.get(),
                                                               admin_window))
    button_login.pack(pady=10)


def admin_authentication(username, password, window):
    if username == "NinJa" and password == "NinJa":
        window.destroy()
        admin_panel = Tk()
        admin_panel.title("Admin Panel")
        admin_panel.geometry("300x150")

        label_title = Label(admin_panel, text="Welcome Admin!", font=("Arial", 14, "bold"))
        label_title.pack(pady=10)

        button_view_scores = Button(admin_panel, text="View Scores", command=view_scores)
        button_view_scores.pack(pady=5)

        button_edit_questions = Button(admin_panel, text="Edit Questions", command=edit_questions)
        button_edit_questions.pack(pady=5)

        admin_panel.mainloop()
    else:
        mb.showerror("Error", "Invalid username or password")


def view_scores():
    try:
        with open('user_scores.json', 'r') as f:
            user_scores = json.load(f)
    except FileNotFoundError:
        mb.showerror("Error", "No scores found.")
        return

    # Create a new window to display scores
    score_window = Tk()
    score_window.title("Scores")
    score_window.geometry("300x300")

    # Display scores
    for username, data in user_scores.items():
        score_label = Label(score_window, text=f"{username}: {data['score']}")
        score_label.pack()


def edit_questions():
    edit_window = Tk()
    edit_window.title("Edit Questions")
    edit_window.geometry("600x400")

    # Create widgets to edit questions
    label_title = Label(edit_window, text="Edit Questions", font=("Arial", 18, "bold"))
    label_title.pack(pady=10)

    # Add your editing components here, e.g., text boxes, buttons, etc.


# Create login window
gui_login = Tk()
gui_login.title("Login")
gui_login.geometry("300x200")

label_username = Label(gui_login, text="Username:")
label_username.pack(pady=10)

entry_username = Entry(gui_login, width=30)
entry_username.pack(pady=5)

button_login = Button(gui_login, text="Login", width=10, command=login)
button_login.pack(pady=10)

button_admin = Button(gui_login, text="Login as Admin", width=15, command=admin_login)
button_admin.pack(pady=5)

gui_login.mainloop()
