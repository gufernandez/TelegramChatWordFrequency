#! python3

import re
import pandas as pd

def main():

    filePath = "C:\\Users\\goncalg4\\Downloads\\Telegram Desktop\\test.txt";

    f = open(filePath, "r");
    print("Reading File:" + filePath);
    f1 = f.readlines();

    target1 = re.compile(r'te amo');
    target2 = re.compile(r'te amu');
    target3 = re.compile(r'ti amo');
    target4 = re.compile(r'ti amu');
    target5 = re.compile(r'tiamo');
    target6 = re.compile(r'tiamu');
    target7 = re.compile(r'teamo');
    target8 = re.compile(r'teamu');
    target9 = re.compile(r'tinhamu');
    target10 = re.compile(r'comer');


    wordCount1 = 0;
    wordCount2 = 0;
    wordCount3 = 0;
    wordCount4 = 0;
    wordCount5 = 0;
    wordCount6 = 0;
    wordCount7 = 0;
    wordCount8 = 0;
    wordCount9 = 0;
    wordCount10 = 0;

    for line in f1:

        foundWord1 = target1.findall(line);
        if (foundWord1):
            for word in foundWord1:
                wordCount1 += 1;

        foundWord2 = target2.findall(line);
        if (foundWord2):
            for word in foundWord2:
                wordCount2 += 1;

        foundWord3 = target3.findall(line);
        if (foundWord3):
            for word in foundWord3:
                wordCount3 += 1;

        foundWord4 = target4.findall(line);
        if (foundWord4):
            for word in foundWord4:
                wordCount4 += 1;

        foundWord5 = target5.findall(line);
        if (foundWord5):
            for word in foundWord5:
                wordCount5 += 1;

        foundWord6 = target6.findall(line);
        if (foundWord6):
            for word in foundWord6:
                wordCount6 += 1;

        foundWord7 = target7.findall(line);
        if (foundWord7):
            for word in foundWord7:
                wordCount7 += 1;

        foundWord8 = target8.findall(line);
        if (foundWord8):
            for word in foundWord8:
                wordCount8 += 1;

        foundWord9 = target9.findall(line);
        if (foundWord9):
            for word in foundWord9:
                wordCount9 += 1;

        foundWord10 = target10.findall(line);
        if (foundWord10):
            for word in foundWord10:
                wordCount10 += 1;

    f.close();

    print("Te Amo: " + str(wordCount1));
    print("Te Amu: " + str(wordCount2));
    print("Ti Amo: " + str(wordCount3));
    print("Ti Amu: " + str(wordCount4));
    print("Tiamo: " + str(wordCount5));
    print("Timu: " + str(wordCount6));
    print("Teamo: " + str(wordCount7));
    print("Teamu: " + str(wordCount8));
    print("Tinhamu: " + str(wordCount9));
    print("comer: " + str(wordCount10));


if __name__ == "__main__":
    main();
