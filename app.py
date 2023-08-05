## variables
#name = "Ahmed"
#age = 20
#hobbies = ["Reading", "Code Refactoring", "Writing"]
#print(name)
#print(age)
#print(hobbies)

## input
#name = input("Enter Your Name: ")
#age  = int(input("Enter Your Age: "))
#print(type(name), name)
#print(type(age), age)

## Arithmetic Operations
#print(2 + 3)
#print(4 - 2)
#print(9 / 2)
#print(9 // 2)
#print (9 % 2)

## Conditions
#age  = int(input("Enter Your Age: "))
#if age > 20:
#	print("You Are a Grown person Now go Study Physics")
#elif age >= 18:
#	print("You Are an Adult go Play Valorant")
#elif age == 16:
#	print("You Are in mid situation Now Go Delete TikTok")
#else :
#	print("You Still a child go Play some Minecraft")

## Loops
#x = 1
#while x < 10:
#	print(x)
#	x += 1

#for i in range(10):
#	print(i)

#for i in range(2, 10, 2):
#	print(i)

#colors = ["red", "blue", "white"]
#for color in colors:
#	print("My Favorite Color is: " + color)
#print("red" in colors)

# Functions
#def double(num):
#	return num * 2

#def getNumber(message):
#	try:
#		return int(input(message))
#	except:
#		return 0

#def printHelp():
#	print("Welcome To Our App")
#	print("Developed by Cyberus")

#print(double(2))
#print(getNumber("Enter Your Age: "))
#print(getNumber(message="Enter Your Age: "))
#printHelp()

# Import Example
#import math

#print(math.sqrt(4))


#from flask import Flask, request

#app = Flask(__name__)

#@app.route("/hello")
#def hello():
#    return "Hello World!"

#@app.route("/say-my-name", methods=["POST", "GET"])
#def say_my_name():
#    return "Hello: " + request.args.get("name")



#if __name__ == "__main__":
#    app.run(debug=True)



from flask import Flask, request

app = Flask(__name__)

students = []

@app.route("/add-student", methods=["POST"])
def add_student():
    name = request.json["name"]
    age = request.json["age"]
    students.append({"name": name, "age": age})
    return "User Added Successfully"


@app.route("/get-students")
def get_students():
    return students



if __name__ == "__main__":
    app.run(debug=True)
