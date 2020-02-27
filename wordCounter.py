#! python3

import re
import pandas as pd
import argparse

def main(args):

    filePath = "storage\\" + args.path;
    wordList = args.words;

    try:
        chatFile = open(filePath, "r", encoding="utf-8");
    except:
        print("Non existant file.");
        return;

    targets = [];
    targetCount = {};
    regs = {};

    for targetWord in wordList:
        targets.append(targetWord);
        targetCount[targetWord] = 0;
        re_str = r''+ re.escape(targetWord);
        regs[targetWord] = re.compile(re_str);

    print(targets);
    print(targetCount);
    print(regs);
    print("Reading File:" + filePath);
    fileObject = chatFile.readlines();

    for line in fileObject:

        for word in targets:
            foundWord = regs[word].findall(line);
            if (foundWord):
                for matches in foundWord:
                    targetCount[word] += 1;


    chatFile.close();

    for word in targets:
        print(word + ": " + str(targetCount[word]));

def parse_arguments():

    parser = argparse.ArgumentParser(description='');

    parser.add_argument('path');
    parser.add_argument('words', nargs='+');
    return parser.parse_args();

if __name__ == "__main__":
    arguments = parse_arguments();
    main(arguments);
