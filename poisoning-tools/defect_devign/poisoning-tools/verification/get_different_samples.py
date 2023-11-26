import sys

def compare_files(file1, file2, output1, output2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2, \
         open(output1, 'w') as out1, open(output2, 'w') as out2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

        # Compare the lines at corresponding positions
        for i in range(len(lines1)):
            line1 = lines1[i].strip()
            line2 = lines2[i].strip()

            if line1 != line2:
                out1.write(line1 + '\n')
                out2.write(line2 + '\n')

# Check if four arguments (file1, file2, output1, output2) are provided
if len(sys.argv) == 5:
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    output1 = sys.argv[3]
    output2 = sys.argv[4]

    compare_files(file1, file2, output1, output2)
else:
    print("Please provide four arguments: file1, file2, output1, output2.")

