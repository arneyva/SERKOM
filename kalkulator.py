import tkinter as tk
from tkinter import messagebox
import sqlite3

class CalculatorApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title('Kalkulator Serkom Programmer')
        self.root.geometry('500x500')
        self.root.resizable(False, False)

        # Setup database connection
        self.db = sqlite3.connect('lsp_calculator.db')
        self.cursor = self.db.cursor()

        # Create table if not exists
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expression TEXT,
                result TEXT
            )
        """)

        self.histories = self.fetch_history()  # Fetch history from database
        self.expression = ''

        # UI setup
        self.setup_ui()

    def fetch_history(self):
        self.cursor.execute("SELECT expression, result FROM history ORDER BY id DESC")
        return self.cursor.fetchall()

    def insert_history(self, expression, result):
        self.cursor.execute("INSERT INTO history (expression, result) VALUES (?, ?)", (expression, result))
        self.db.commit()

    def delete_all_history(self):
        self.cursor.execute("DELETE FROM history")
        self.db.commit()
        self.histories = []
        self.update_history_expression('')
        self.update_expression('')

    def update_expression(self, new_expression):
        self.expression_label.config(text=new_expression)
        self.expression = new_expression

    def update_history_expression(self, new_history_expression):
        self.history_expression_label.config(text=new_history_expression)

    def calculate_expression(self, expression):
        try:
            # Replace 'x' with '*' for multiplication
            expression = expression.replace('x', '*')
            
            # Evaluate the expression
            result = str(eval(expression))
            
            if result.endswith('.0'):
                result = result[:-2]
            
            self.update_expression(result)
            self.update_history_expression(expression)
            self.histories.insert(0, (expression, result))
            self.insert_history(expression, result)  # Insert into database
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def button_action(self, button_value):
        if button_value == 'AC':
            if self.expression == '':
                self.delete_all_history()
            self.expression = ''
            self.update_expression(self.expression)
        elif button_value == '<':
            self.expression = self.expression[:-1]
            self.update_expression(self.expression)
        elif button_value == '=':
            self.calculate_expression(self.expression)
        else:
            self.expression += button_value
            self.update_expression(self.expression)

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title('History')
        history_window.geometry('250x300')
        history_window.resizable(False, False)

        main_frame = tk.Frame(history_window, bg='#d1d5db')
        main_frame.pack(expand=True, fill='both')

        for i, (expr, result) in enumerate(self.histories):
            expr_label = tk.Button(main_frame, text=f'{expr} = ', command=lambda x=expr: self.update_expression(x), bg='#d4d4d8', fg='#52525b')
            expr_label.grid(row=i, column=0, pady=2, sticky='e')
            result_button = tk.Button(main_frame, text=result, command=lambda x=result: self.update_expression(x), bg='#d4d4d8', fg='#52525b')
            result_button.grid(row=i, column=1, padx=(0, 5), pady=2, sticky='w')
        
        history_window.transient(self.root)
        history_window.grab_set()
        history_window.focus()
        self.root.wait_window(history_window)

    def setup_ui(self):
        container_frame = tk.Frame(self.root, bg='#d4d4d8')
        container_frame.pack(expand=True, fill='both')

        history_expression_frame = tk.Frame(container_frame, bg='#d4d4d8')
        history_expression_frame.pack(fill='x')

        expression_frame = tk.Frame(container_frame, bg='#d4d4d8')
        expression_frame.pack(expand=True, fill='both')

        button_frame = tk.Frame(container_frame, bg='#d4d4d8')
        button_frame.pack(fill='x', padx=2, pady=2)
        button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # Label
        button_history = tk.Button(
            history_expression_frame, text='History', anchor='w',
            command=self.show_history
        )
        button_history.pack(side='left', padx=5, pady=(5, 0))

        self.history_expression_label = tk.Label(
            history_expression_frame, text='', font=('Helvetica', 14, 'bold'),
            anchor='e', fg='#a1a1aa'
        )
        self.history_expression_label.pack(side='right', padx=5, pady=(5, 0))

        self.expression_label = tk.Label(
            expression_frame, text='', font=('Helvetica', 16, 'bold'),
            anchor='e', fg='#52525b'
        )
        self.expression_label.pack(expand=True, fill='both', padx=5)

        # Buttons
        buttons = [
            'AC', '<', '%', '/',
            '7', '8', '9', 'x',
            '4', '5', '6', '-',
            '1', '2', '3', '+',
            '0', '.', '=',
        ]

        row, col = 0, 0
        for button in buttons:
            btn = tk.Button(
                button_frame, text=button, font=('Helvetica', 16, 'bold'),
                bg='#e4e4e7', fg='#52525b',
                command=lambda x=button: self.button_action(x)
            )
            if button == '0':
                btn.grid(row=row, column=col, columnspan=2, padx=1, pady=1, ipady=5, sticky='we')
                col += 1
            else:
                btn.grid(row=row, column=col, padx=1, pady=1, ipady=5, sticky='we')
            col += 1
            if col == 4:
                col = 0
                row += 1

    def close(self):
        self.db.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
    app.close()
