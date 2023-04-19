import main
import sys

# flag == 10 cork
# flag == 0 no pneumonia
# flag == 1 bacterial pneumonia
# flag == 2 viral pneumonia
# flag == 3 covid pneumonia
answer = main.connector_n()
print(f"Answer : {answer}")

file = open(r'E:\Neuro\xyz.txt','w')
file.write(f"{answer}")
file.close()