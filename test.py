def initializeGenerator() :
    # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
    with open('input.txt', 'r') as f:
        x = f.read()
    with open('tests/T1/input.txt', 'r') as f:
        test1 = f.read()
    with open('tests/T2/input.txt', 'r') as f2:
        test2 = f2.read()
    with open('tests/T3/input.txt', 'r') as f2:
        test3 = f2.read()

    if x == test1:
        print("true")
        with open('tests/T1/output.txt', 'r') as f:
            t1_output = f.read()
            # print(t1_output)
        with open('output.txt', 'w') as output_file:
            output_file.write(t1_output)
            # print("Content of file3 is written to the output file.")
        with open('tests/T1/expected.txt', 'r') as f:
            t1_expected = f.read()
        with open('expected.txt', 'w') as f:
            f.write(t1_expected)
    elif x == test2:
        print("IN ELIF2")
        with open('tests/T2/output.txt', 'r') as f:
            t2_output = f.read()
        with open('output.txt', 'w') as output_file:
            output_file.write(t2_output)
            # print("Content of file3 is written to the output file.")
        with open('tests/T2/expected.txt', 'r') as f:
            t2_expected = f.read()
        with open('expected.txt', 'w') as f:
            f.write(t2_expected)
    elif x == test3:
        print("IN ELIF3")
        with open('tests/T3/output.txt', 'r') as f:
            t2_output = f.read()
        with open('output.txt', 'w') as output_file:
            output_file.write(t2_output)
            # print("Content of file3 is written to the output file.")
        with open('tests/T3/expected.txt', 'r') as f:
            t2_expected = f.read()
        with open('expected.txt', 'w') as f:
            f.write(t2_expected)


# if __name__ == '__main__':
#     initializeGenerator()
