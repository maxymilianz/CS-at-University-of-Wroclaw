def tabliczka(x1, x2, y1, y2):
    firstLine = '\t'

    for i in range(x1, x2 + 1):
        firstLine += str(i) + '\t'

    print(firstLine)

    for i in range(y1, y2 + 1):
        line = str(i) + '\t'

        for j in range(x1, x2 + 1):
            line += str((i * j)) + '\t'

        print(line)