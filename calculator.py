import os
import math
import keyboard
from colorama import Fore, init

init()

expression = ""
result = ""
cursor_pos = 0
last_result = ""
auto_start_from_result = False 

def safe_eval(expr):
    try:
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        allowed.update({
            "abs": abs,
            "round": round,
            "sqrt": math.sqrt
        })
        expr = expr.replace("^", "**")
        return str(eval(expr, {"__builtins__": {}}, allowed))
    except:
        return "Error"

def draw_calculator():
    global cursor_pos
    os.system('cls' if os.name=='nt' else 'clear')

    print(Fore.CYAN + "****************************************")
    print(Fore.GREEN + "*            CALCULATOR                *")
    print(Fore.CYAN + "****************************************")

    display_expr = expression
    if cursor_pos > len(display_expr):
        cursor_pos = len(display_expr)

    display_expr = display_expr[:cursor_pos] + "_" + display_expr[cursor_pos:]

    start = max(cursor_pos - 35, 0)
    display_expr_window = display_expr[start:start + 36]

    print(Fore.MAGENTA + f"* {display_expr_window.ljust(36)}*")

    display_result = result[:36] if result else ""
    print(Fore.GREEN + f"* {display_result.rjust(35)} *")

    print(Fore.CYAN + "****************************************")
    print(Fore.YELLOW + "*  [7] [8] [9]  [ / ]                 *")
    print("*  [4] [5] [6]  [ * ]                 *")
    print("*  [1] [2] [3]  [ - ]                 *")
    print("*  [0] [.] [=]  [ + ]                 *")
    print("*  [(] [)] [√]  [ ^ ]                 *")
    print("*  [C] Clear                             *")
    print(Fore.CYAN + "****************************************")


def handle_key(event):
    global expression, result, cursor_pos, last_result, auto_start_from_result

    key = event.name
    draw = False

    numbers = "0123456789"
    operators = "+-*/^"

    def insert_at_cursor(text):
        nonlocal draw
        global expression, cursor_pos
        expression = expression[:cursor_pos] + text + expression[cursor_pos:]
        cursor_pos += len(text)
        draw = True

    if len(key) == 1 and key in numbers + ".":
        if auto_start_from_result:
            if safe_eval(expression) == last_result:
                last_result = ""
                result = ""
                expression = ""
                cursor_pos = 0
            auto_start_from_result = False
        insert_at_cursor(key)

    elif key in operators:
        if auto_start_from_result:
            expression = last_result
            last_result = ""
            result = ""
            cursor_pos = len(expression)
            auto_start_from_result = False
        insert_at_cursor(key)

    elif key in ["enter", "="]:
        temp_res = safe_eval(expression)
        result = temp_res
        last_result = result
        auto_start_from_result = result != "Error"
        draw = True

    elif key == "backspace" and cursor_pos > 0:
        expression = expression[:cursor_pos-1] + expression[cursor_pos:]
        cursor_pos -= 1
        draw = True

    elif key == "left" and cursor_pos > 0:
        cursor_pos -= 1
        draw = True
    elif key == "right" and cursor_pos < len(expression):
        cursor_pos += 1
        draw = True

    elif key in ["esc", "c"]:
        expression = ""
        result = ""
        last_result = ""
        cursor_pos = 0
        auto_start_from_result = False
        draw = True

    elif key == "s":
        if auto_start_from_result:
            expression = last_result
            cursor_pos = len(expression)
            auto_start_from_result = False
        insert_at_cursor("sqrt()")
        cursor_pos -= 1

    elif key == "(":
        insert_at_cursor("()")
        cursor_pos -= 1
    elif key == ")":
        insert_at_cursor(")")

    if draw:
        draw_calculator()


draw_calculator()
keyboard.on_press(handle_key)
keyboard.wait()
