#!/usr/bin/python3

from tkinter import *
from tkinter import ttk 

import logging
import sys

class Calculator:
    def __init__(self, master):
        # Configure logger
        self.config_logger()

        # Root window
        master.title('Calculator')
        master.geometry("400x400")
        #master.resizable(False, False)
        master.configure(background = '#887784')
        
        # The grid_rowconfigure('all', weight=1) syntax is not supported in Tkinter. 
        # The 'all' argument can ONLY be used with grid_columnconfigure.
        master.grid_columnconfigure(0, weight=1)
        master.grid_rowconfigure   (0, weight=1)

        # Title bar icon
        self.window_icon = PhotoImage(file='images/calculator_icon.png')
        master.iconphoto(True, self.window_icon)

        self.style = ttk.Style()
        self.style.configure('TFrame')
        self.style.configure('TButton', height=8, width=8, font=('Arial', 11))
        self.style.configure('TEntry', font=('Helvetica', 19))

        # Frames inside the main window
        self.frame_calculator = ttk.Frame(master, padding=5)
        self.frame_calculator.grid(row=0, column=0, sticky='nsew')

        # Configure the grid cell to expand when user resizes window
        self.frame_calculator.grid_rowconfigure   (index=0, weight=1)
        self.frame_calculator.grid_columnconfigure(index=0, weight=1)
        self.frame_calculator.grid_rowconfigure   (index=1, weight=1)

        # TODO - Add history of executed expressions and their results
        # self.frame_memory = ttk.Frame(master)
        # self.frame_memory.grid(row=0, column=2)
        # Memory frame
        # self.text_memory = Text(self.frame_memory, state=DISABLED)
        # self.text_memory.pack(fill=BOTH, expand=True)

        # Frames inside calculator frame
        # Display result and expression to evaluate
        self.frame_result  = ttk.Frame(self.frame_calculator)
        self.frame_result.grid(row = 0, column = 0, sticky='nsew')
        # Frame to hold the buttons
        self.frame_buttons = ttk.Frame(self.frame_calculator)
        self.frame_buttons.grid(row = 1, column = 0, sticky='nsew')

        # Configure the grid cell to expand when user resizes window
        self.frame_result.rowconfigure   (index=0, weight=1)
        self.frame_result.columnconfigure(index=0, weight=1)
        self.frame_result.rowconfigure   (index=1, weight=1)

        # Expression to pass on to the eval() function
        self.expression     = StringVar(value='')
        self.display_result = DoubleVar(value=0) 
        # Tkinter variable which helps in event handling - automatically update the Entry widget whenever the value changes. 
        # But need to use set() and get() to assign and retrieve values.

        self.result           = 0 # Normal python variable - easy to assign and get values
        self.calculation_done = True

        # Display expression
        self.entry_display_expression = ttk.Entry(self.frame_result, textvariable=self.expression, state='readonly', justify='left',
                                                    font=('Helvetica', 12))
        self.entry_display_expression.grid(row = 0, column = 0, sticky='nsew')

        # Display result
        self.entry_display_result = ttk.Entry(self.frame_result, textvariable=self.display_result, state='readonly', justify='right', 
                                                font=('Helvetica', 20))
        self.entry_display_result.grid(row = 1, column = 0, sticky='nsew')

        # Buttons
        # Row 0
        self.row_id = 0
        ttk.Button(self.frame_buttons, text = '7', command = lambda: self.button_press('7')).grid(row = self.row_id, column = 0)
        ttk.Button(self.frame_buttons, text = '8', command = lambda: self.button_press('8')).grid(row = self.row_id, column = 1)
        ttk.Button(self.frame_buttons, text = '9', command = lambda: self.button_press('9')).grid(row = self.row_id, column = 2)
        ttk.Button(self.frame_buttons, text = '÷', command = lambda: self.button_press('/')).grid(row = self.row_id, column = 3)

        # Row 1
        self.row_id += 1
        ttk.Button(self.frame_buttons, text = '4', command = lambda: self.button_press('4')).grid(row = self.row_id, column = 0)
        ttk.Button(self.frame_buttons, text = '5', command = lambda: self.button_press('5')).grid(row = self.row_id, column = 1)
        ttk.Button(self.frame_buttons, text = '6', command = lambda: self.button_press('6')).grid(row = self.row_id, column = 2)
        ttk.Button(self.frame_buttons, text = 'x', command = lambda: self.button_press('*')).grid(row = self.row_id, column = 3)
        
        # Row 2
        self.row_id += 1
        ttk.Button(self.frame_buttons, text = '1', command = lambda: self.button_press('1')).grid(row = self.row_id, column = 0)
        ttk.Button(self.frame_buttons, text = '2', command = lambda: self.button_press('2')).grid(row = self.row_id, column = 1)
        ttk.Button(self.frame_buttons, text = '3', command = lambda: self.button_press('3')).grid(row = self.row_id, column = 2)
        ttk.Button(self.frame_buttons, text = '-', command = lambda: self.button_press('-')).grid(row = self.row_id, column = 3)
        
        # Row 3
        self.row_id += 1
        ttk.Button(self.frame_buttons, text = 'x²', command = lambda: self.button_press('square')).grid(row = self.row_id, column = 0)
        ttk.Button(self.frame_buttons, text = '0' , command = lambda: self.button_press('0')     ).grid(row = self.row_id, column = 1) 
        ttk.Button(self.frame_buttons, text = '•' , command = lambda: self.button_press('.')     ).grid(row = self.row_id, column = 2)      
        ttk.Button(self.frame_buttons, text = '+' , command = lambda: self.button_press('+')     ).grid(row = self.row_id, column = 3)
        
        # Row 4
        self.row_id += 1
        ttk.Button(self.frame_buttons, text = '√x' , command = lambda: self.button_press('square_root')).grid(row = self.row_id, column = 0)
        ttk.Button(self.frame_buttons, text = '('  , command = lambda: self.button_press('(')          ).grid(row = self.row_id, column = 1)
        ttk.Button(self.frame_buttons, text = ')'  , command = lambda: self.button_press(')')          ).grid(row = self.row_id, column = 2) 
        ttk.Button(self.frame_buttons, text = 'Ans', command = lambda: self.button_press('Ans')        ).grid(row = self.row_id, column = 3)
        #ttk.Button(self.frame_buttons, text = '1/x'    , command = lambda: self.button_press('reciprocal') ).grid(row = self.row_id, column = 1) 

        # Row 5
        self.row_id += 1
        ttk.Button(self.frame_buttons, text = 'CLEAR', command = lambda: self.button_press('clear')    ).grid(row = self.row_id, column = 0)
        ttk.Button(self.frame_buttons, text = '⌫'   , command = lambda: self.button_press('BackSpace')).grid(row = self.row_id, column = 1)
        ttk.Button(self.frame_buttons, text = '='    , command = lambda: self.button_press('=')        ).grid(row = self.row_id, column = 2, columnspan=2)

        # Keyboard bidings for the buttons
        master.bind("<Key>", self.keyboard_entry)
        
        # Set weights for each button inside frame_buttons, to make them expand with the window resize
        for row_id in range(self.frame_buttons.grid_size()[1]):
            self.frame_buttons.grid_rowconfigure(index=row_id, weight=1)
        for col_id in range(self.frame_buttons.grid_size()[0]):
            self.frame_buttons.grid_columnconfigure(index=col_id, weight=1)

        # Set padding for all the buttons
        for child in self.frame_buttons.winfo_children():
            child.grid_configure(padx = 3, pady = 3, sticky='nsew')


    def button_press(self, char):
        ''' Returns which button is pressed '''
        self.logger.info(f"Button: {char}, Expression: {self.expression.get()}")

        current_expr        = self.expression.get()  
        opening_brace_count = 0
        closing_brace_count = 0     

        #self.calculation_done = False
        if(current_expr != ''):            
            self.calculation_done = (current_expr[-1] == '=')

        if(char == 'clear'):
            self.clear()
            return
        elif(char == '='):
            if(not self.calculation_done): self.evaluate()
            return
        else:
            if(char == 'BackSpace'):
                if(current_expr != ''): 
                    current_expr = current_expr[:-1]
                
                self.entry_display_expression.configure(foreground='black')
            elif(char == 'square'):
                if(self.calculation_done): 
                    current_expr = f"({self.result})"

                current_expr += '**2'
            elif(char == 'square_root'):
                if(self.calculation_done): 
                    current_expr = f"({self.result})"

                current_expr += '**0.5'
            elif(char == 'Ans'):
                if(self.calculation_done):
                    current_expr  = f"({self.result})"
                else:
                    current_expr += f"({self.result})"
            elif(char == '('):
                if  ((self.result == 0) and (current_expr == '')):
                    current_expr = char
                elif(self.calculation_done):
                    current_expr = f"({self.result}"
                else:
                    current_expr += char
            elif(char == ')'):
                opening_brace_count = sum(1 for _ in current_expr if _ == '(')
                closing_brace_count = sum(1 for _ in current_expr if _ == ')')
                if((closing_brace_count < opening_brace_count)): #not self.calculation_done and
                    current_expr += char
            else:         
                if(self.calculation_done):
                    if(char.isdigit()):
                        current_expr = ''
                    else:
                        current_expr = str(self.result)

                current_expr += char

            #self.calculation_done = False

            self.display_expression(current_expr)
            
        self.logger.info(f"Current Expression = {current_expr}")        

    def display_expression(self, current_expr):
        ''' Send the expression to the display '''
        self.expression.set(value=current_expr)

    def keyboard_entry(self, event):
        ''' Detect keyboard entries '''
        self.logger.info(f"Keyboard entry     = {event.keysym} {event.char}")
        
        key_pressed = ''

        # Keyboard etry with only event.keysym and no event.char
        if  (event.keysym == 'Return'   ):  key_pressed = '='
        elif(event.keysym == 'BackSpace'):  key_pressed = 'BackSpace'
        elif(event.keysym == 'Escape'   ):  key_pressed = 'clear'

        elif event.char and event.char in "1234567890.+-*/=()":
            key_pressed = event.char
        
        else: # If any other key is pressed, don't do anything 
            return
        
        self.button_press(key_pressed)

    def clear(self):
        ''' Clear output '''
        self.expression.set(value='')
        self.result = 0
        self.display_result.set(value=0)
        self.entry_display_expression.configure(foreground='black')
        self.calculation_done = True

        self.logger.debug("Clearing outputs")

    def evaluate(self):
        ''' Evaluate the result ''' 
        expr = self.expression.get()

        if(expr == ''): return 0
        if(expr[-1] == '='): expr = (expr[:-1]).strip() # strip to remove the space(if any) btwn expression and =

        try:
            self.result = eval(expr)
            self.display_result.set(value=self.result)
            self.expression.set(value=f"{expr}=")
            #self.calculation_done = True
            self.entry_display_expression.configure(foreground='black')
        except:
            self.entry_display_expression.configure(foreground='red')
            self.logger.info('Invalid Entry')
        
        self.logger.info(f"Result: {self.expression.get()} {str(self.result)}")

    def config_logger(self):
        # Basic logger config       
        logging.basicConfig(filename="", 
                            format="%(levelname)-5s: %(filename)s(Func:%(funcName)-14s, Line:%(lineno)-3d): %(message)s")
        
        self.logger = logging.getLogger()  # Creating an object
        self.logger.setLevel(logging.INFO) # Setting the threshold of logger to DEBUG
        logging.StreamHandler(sys.stdout)  # Print logging to console output as well

def main():
    root = Tk()
    calculator = Calculator(root)
    root.mainloop()
    
if __name__ == "__main__": main()

"""
----- USE OF __MAIN__ -----

If this file is run independently by typing '>>> hello_app.py', 
    python detects that this module/file is run as main, i.e __name__ = __main__
    Thus, the main() function will get executed.
Else,
    this module can be imported in other top level files to be executed as a part 
    of another top level app
"""