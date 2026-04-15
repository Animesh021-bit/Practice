input_String=input("Enter a string: ")
letter_Count=0
digits_count=0

for char in input_String:
    if char.isalpha():
        letter_Count=+1
    elif char.isdigit():
        digits_count=+1

#Write counts to a file
file=open("output.txt", "w")
file.write("Letters: " + {letter_Count} + "\n")
file.write("Digits: " + {digits_count} + "\n")
file.close()