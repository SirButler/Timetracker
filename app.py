import tkinter as tk
from tkinter import messagebox
import time
import sqlite3

class TopicTimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Topic Timer")
        
        self.current_topic = None
        self.start_time = None
        self.running = False

        self.setup_ui()
        self.refresh_topics()
        self.restore_state()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=10)

        self.topic_label = tk.Label(self.frame, text="Topic:")
        self.topic_label.grid(row=0, column=0, padx=5)

        self.topic_entry = tk.Entry(self.frame)
        self.topic_entry.grid(row=0, column=1, padx=5)

        self.add_button = tk.Button(self.frame, text="Add Topic", command=self.add_topic)
        self.add_button.grid(row=0, column=2, padx=5)

        self.topics_listbox = tk.Listbox(self.frame)
        self.topics_listbox.grid(row=1, column=0, columnspan=3, pady=10)
        self.topics_listbox.bind('<<ListboxSelect>>', self.select_topic)

        self.start_button = tk.Button(self.frame, text="Start Timer", command=self.start_timer, state=tk.DISABLED)
        self.start_button.grid(row=2, column=0, pady=5)

        self.stop_button = tk.Button(self.frame, text="Stop Timer", command=self.stop_timer, state=tk.DISABLED)
        self.stop_button.grid(row=2, column=1, pady=5)

        self.time_label = tk.Label(self.frame, text="Time Spent: 00:00:00")
        self.time_label.grid(row=2, column=2, pady=5)

    def add_topic(self):
        topic_name = self.topic_entry.get().strip()
        if topic_name:
            conn = sqlite3.connect('topics.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO topics (name) VALUES (?)", (topic_name,))
            conn.commit()
            conn.close()
            self.topic_entry.delete(0, tk.END)
            self.refresh_topics()

    def refresh_topics(self):
        self.topics_listbox.delete(0, tk.END)
        conn = sqlite3.connect('topics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM topics")
        topics = cursor.fetchall()
        conn.close()
        for topic in topics:
            self.topics_listbox.insert(tk.END, topic[1])

    def select_topic(self, event):
        selection = self.topics_listbox.curselection()
        if selection:
            self.current_topic = self.topics_listbox.get(selection[0])
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.time_label.config(text="Time Spent: 00:00:00")
            self.update_timer_label()

    def start_timer(self):
        self.running = True
        self.start_time = time.time()
        self.save_state()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.update_timer()

    def stop_timer(self):
        self.running = False
        end_time = time.time()
        elapsed_time = int(end_time - self.start_time)

        conn = sqlite3.connect('topics.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE topics SET total_time = total_time + ?, running = 0, start_time = 0 WHERE name = ?", (elapsed_time, self.current_topic))
        conn.commit()
        conn.close()

        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.time_label.config(text="Time Spent: 00:00:00")

    def update_timer(self):
        if self.running:
            elapsed_time = int(time.time() - self.start_time)
            hours, remainder = divmod(elapsed_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.config(text=f"Time Spent: {hours:02}:{minutes:02}:{seconds:02}")
            self.root.after(1000, self.update_timer)

    def save_state(self):
        if self.current_topic and self.running:
            conn = sqlite3.connect('topics.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE topics SET running = 1, start_time = ? WHERE name = ?", (int(self.start_time), self.current_topic))
            conn.commit()
            conn.close()

    def restore_state(self):
        conn = sqlite3.connect('topics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, start_time FROM topics WHERE running = 1")
        result = cursor.fetchone()
        conn.close()
        if result:
            self.current_topic, self.start_time = result
            self.running = True
            elapsed_time = int(time.time() - self.start_time)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.topics_listbox.select_set(self.topics_listbox.get(0, tk.END).index(self.current_topic))
            self.update_timer_label()
            self.update_timer()

    def update_timer_label(self):
        conn = sqlite3.connect('topics.db')
        cursor = conn.cursor()
        cursor.execute("SELECT total_time FROM topics WHERE name = ?", (self.current_topic,))
        result = cursor.fetchone()
        conn.close()
        if result:
            total_time = result[0]
            hours, remainder = divmod(total_time, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.time_label.config(text=f"Time Spent: {hours:02}:{minutes:02}:{seconds:02}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TopicTimerApp(root)
    root.mainloop()