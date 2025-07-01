#from functions.get_files_info import get_files_info
#from functions.get_file_content import get_file_content
#from functions.write_file import write_file
from functions.run_python import run_python_file

print("TEST ONE")
print(run_python_file("calculator", "main.py"))

print("TEST TWO")
print(run_python_file("calculator", "tests.py"))

print("TEST THREE")
print(run_python_file("calculator", "../main.py"))

print("TEST FOUR")
print(run_python_file("calculator", "nonexistent.py"))
'''
print("TEST ONE")
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

print("TEST TWO")
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

print("TEST THREE")
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
'''

'''
print("TEST ONE")
print(get_file_content("calculator", "main.py"))

print("TEST TWO")
print(get_file_content("calculator", "pkg/calculator.py"))

print("TEST THREE")
print(get_file_content("calculator", "/bin/cat"))
#print(get_file_content("calculator", "lorem.txt"))
'''

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
