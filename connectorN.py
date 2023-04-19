import main

def save_file():
    answer = main.connector_n()
    file = open('xyz.txt', 'w')
    file.write(f"{answer}")
    file.close()
