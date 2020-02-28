#! python3

import re
import pandas as pd
import argparse

def main(args):

    filePath = "storage\\" + args.FILE;
    wordList = args.WORDS;

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

    parser = argparse.ArgumentParser(description='Obtain the number of times a word or phrase is used in a text (case sensitive)');

    parser.add_argument('FILE', help="Name of the file located on the storage/ folder");
    parser.add_argument('WORDS', nargs='+', help="List of terms to look for. They should be separated by spaces and inside quotes. Example: 'py file \"hello\" \"world\" \"hello world\"'");
    return parser.parse_args();

if __name__ == "__main__":
    arguments = parse_arguments();
    main(arguments);
