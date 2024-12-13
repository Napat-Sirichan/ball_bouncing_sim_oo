
# import turtle

# # เตรียมเต่าและหน้าจอ
# screen = turtle.Screen()
# t = turtle.Turtle()
# b = turtle.Turtle()

# # Animation
# t.speed(5)
# screen.tracer(1)

# # Event
# screen.listen()
# screen.onkey(lambda: t.forward(100), "Up")  # กดลูกศรขึ้นเพื่อเคลื่อนที่
# screen.onkey(lambda: t.left(90), "Left")
# screen.onkey(lambda: t.right(90), "Right")

# # Input Method
# name = screen.textinput("Name", "What's your name?")
# print(f"Hello, {name}!")
# b.speed("fastest")

# t.setx(50)
# t.setposition(100,-50)
# b.circle(100)
# t.dot(10)
# b.color("blue", "yellow")  # ตั้งสีเส้นเป็น blue และสีเติมเป็น yellow

# b.begin_fill()  # เริ่มต้นการเติมสี
# b.circle(50)    # วาดวงกลมที่มีรัศมี 50
# b.end_fill()    # เติมสีด้านในวงกลม
# b.setposition(100,-50)
# b.begin_fill()  # เริ่มต้นการเติมสี
# b.circle(50)    # วาดวงกลมที่มีรัศมี 50
# b.end_fill()    # เติมสีด้านในวงกลม
# # Keep the window open
# screen.mainloop()

import turtle

screen = turtle.Screen()
screen.setup(600, 400)
pen = turtle.Turtle()
pen.penup()

# Draw a box:
pen.goto(-100, 20)
pen.pendown()
for _ in range(2):
    pen.forward(200)
    pen.right(90)
    pen.forward(40)
    pen.right(90)
pen.penup()

# This will store the user input:
user_input = []

def type_key(char):
    user_input.append(char)
    refresh_text()

def refresh_text():
    pen.goto(-90, 0)  # inside the box
    pen.color("black")
    pen.clear()
    pen.write("".join(user_input), font=("Arial", 16, "normal"))

def backspace():
    if user_input:
        user_input.pop()
        refresh_text()

# Listen for keys a-z and a backspace
import string
for letter in string.ascii_lowercase:
    screen.onkeypress(lambda c=letter: type_key(c), letter)
for digit in string.digits:
    screen.onkeypress(lambda c=digit: type_key(c), digit)

screen.onkeypress(backspace, "BackSpace")
screen.listen()
turtle.done()
