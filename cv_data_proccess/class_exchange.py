import os

class_to_replace = 1  # the class you want to replace
new_class = 0  # the new class you want to use
data_dir = 'trai/labels'

for filename in os.listdir(data_dir):

    if filename.endswith('.txt'):
        if filename == "classes.txt":
            print("classes.txt passed")
            continue
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()
        with open(filepath, 'w') as file:
            for line in lines:
                line_parts = line.split()
                class_num = int(line_parts[0])
                if class_num == class_to_replace:
                    line_parts[0] = str(new_class)
                file.write(' '.join(line_parts) + '\n')

print("Process done")
