#from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content

print("TEST ONE")
print(get_file_content("calculator", "main.py"))

print("TEST TWO")
print(get_file_content("calculator", "pkg/calculator.py"))

print("TEST THREE")
print(get_file_content("calculator", "/bin/cat"))
#print(get_file_content("calculator", "lorem.txt"))

'''
print("TEST ONE")
print(get_files_info("calculator", "."))

print("TEST TWO")
print(get_files_info("calculator", "pkg"))

print("TEST THREE")
print(get_files_info("calculator", "/bin"))

print("TEST FOUR")
print(get_files_info("calculator", "../"))
'''
