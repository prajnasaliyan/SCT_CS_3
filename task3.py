import tkinter as tk
from tkinter import ttk
import random
import string
import re

# -----------------------------
# PASSWORD STRENGTH CALCULATION
# -----------------------------
def calculate_strength(password):
    score = 0

    # Length Score
    length = len(password)
    if length >= 12:
        score += 40
    elif length >= 8:
        score += 25
    elif length >= 5:
        score += 10

    # Variety Score
    if re.search(r"[a-z]", password):
        score += 10
    if re.search(r"[A-Z]", password):
        score += 10
    if re.search(r"[0-9]", password):
        score += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 20

    # All mixed bonus
    if (re.search(r"[a-z]", password) and re.search(r"[A-Z]", password) and
        re.search(r"[0-9]", password) and re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) and
        length >= 12):
        score += 10

    return min(score, 100)


# -----------------------------
# UPDATE OUTPUT COLORS
# -----------------------------
def update_strength(event=None):
    password = entry.get()
    score = calculate_strength(password)

    progress['value'] = score

    # Custom output color levels
    if score < 30:
        color = "#FF1E1E"   # bright red
        text = "Very Weak"
    elif score < 50:
        color = "#FF6A00"   # orange
        text = "Weak"
    elif score < 70:
        color = "#FFCC00"   # yellow
        text = "Medium"
    elif score < 90:
        color = "#4D9FFF"   # blue
        text = "Strong"
    else:
        color = "#23D160"   # neon green
        text = "Very Strong"

    # Update output label with new colors
    strength_label.config(text=f"Strength: {text} ({score}%)",
                          fg=color, bg="#101820")

    # Update progress bar color
    progress_style.configure("Custom.Horizontal.TProgressbar", background=color)

    # Update suggestion box
    suggestion_box.config(state="normal")
    suggestion_box.delete(1.0, tk.END)

    # Custom suggestions
    if len(password) < 8:
        suggestion_box.insert(tk.END, "- Use at least 8 characters\n")
    if not re.search(r"[A-Z]", password):
        suggestion_box.insert(tk.END, "- Add uppercase letters (A-Z)\n")
    if not re.search(r"[a-z]", password):
        suggestion_box.insert(tk.END, "- Add lowercase letters (a-z)\n")
    if not re.search(r"[0-9]", password):
        suggestion_box.insert(tk.END, "- Include numbers (0-9)\n")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestion_box.insert(tk.END, "- Add special characters (!,@,#,$,...)\n")

    suggestion_box.config(state="disabled")


# -----------------------------
# GENERATE STRONG PASSWORD
# -----------------------------
def generate_password():
    length = 14
    characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}<>?"
    password = "".join(random.choice(characters) for _ in range(length))

    entry.delete(0, tk.END)
    entry.insert(0, password)
    update_strength()


# -----------------------------
# TOGGLE PASSWORD VISIBILITY
# -----------------------------
def toggle_password():
    if entry.cget("show") == "":
        entry.config(show="*")
        eye_button.config(text="👁")
    else:
        entry.config(show="")
        eye_button.config(text="🔒")


# -----------------------------
# GUI DESIGN (New Colors)
# -----------------------------
root = tk.Tk()
root.title("Colorful Password Strength Checker")
root.geometry("520x520")
root.config(bg="#101820")  # dark blue-black

title = tk.Label(root, text="Advanced Password Strength Checker",
                 font=("Arial", 18, "bold"), fg="#F2F2F2", bg="#101820")
title.pack(pady=10)

entry_frame = tk.Frame(root, bg="#101820")
entry_frame.pack(pady=10)

entry = tk.Entry(entry_frame, show="*", font=("Arial", 14),
                 width=28, bd=2, bg="#1A1A1A", fg="white", insertbackground="white")
entry.grid(row=0, column=0, padx=5)

eye_button = tk.Button(entry_frame, text="👁", font=("Arial", 12, "bold"),
                       command=toggle_password, bg="#303030", fg="white")
eye_button.grid(row=0, column=1)

generate_button = tk.Button(root, text="Generate Strong Password",
                            command=generate_password, bg="#007BFF", fg="white",
                            font=("Arial", 12, "bold"))
generate_button.pack(pady=10)

# Progress bar styling
progress_style = ttk.Style()
progress_style.theme_use("clam")
progress_style.configure("Custom.Horizontal.TProgressbar",
                         troughcolor="#333333", thickness=20)

progress = ttk.Progressbar(root, style="Custom.Horizontal.TProgressbar", length=350)
progress.pack(pady=15)

strength_label = tk.Label(root, text="Strength: ---", font=("Arial", 16, "bold"),
                          fg="white", bg="#101820")
strength_label.pack()

suggestion_title = tk.Label(root, text="Suggestions to Improve:",
                            font=("Arial", 15, "bold"), fg="#F2F2F2", bg="#101820")
suggestion_title.pack(pady=5)

# Suggestions box with new colors
suggestion_box = tk.Text(root, height=8, width=55, bg="#0F292F",
                         fg="#66FCF1", font=("Arial", 11))
suggestion_box.pack()
suggestion_box.config(state="disabled")

entry.bind("<KeyRelease>", update_strength)

root.mainloop()
