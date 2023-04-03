import os

class_to_keep = 2
data_dir = 'path'

for filename in os.listdir(data_dir):
    if filename == "classes.txt":
        print("classes.txt passed")
        continue
    if filename.endswith('.txt'):
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'r') as file:
            lines = file.readlines()
        with open(filepath, 'w') as file:
            for line in lines:
                line_parts = line.split()
                class_num = int(line_parts[0])
                if class_num == class_to_keep:
                    line_parts[0] = str(0)
                else:
                    continue
                file.write(' '.join(line_parts) + '\n')

print("process done")
