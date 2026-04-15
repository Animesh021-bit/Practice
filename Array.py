# file=open('Examlple.txt','r')
# # line=file.readline()
# print(line.strip())
# line=file.readline()
# # print(line.strip())
# while line:
#     print (line.strip()) #.strip removes the new line character
#     line=file.readline()
# file.close()

file =open("Example1.txt",'w')
lines=['First line\n','Second line\n','Third line\n']
file.writelines(lines)
file.close()