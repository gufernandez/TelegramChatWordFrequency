#! python3

import re
import pandas as pd
import argparse

def checkForDiv (text):
    divRegex = re.compile(r'<div');
    divCloseRegex = re.compile(r'</div');

    foundDiv = divRegex.findall(text);

    if (foundDiv):
        return 1;
    else:
        foundClosedDiv = divCloseRegex.findall(text);
        if (foundClosedDiv):
            return -1;
        else:
            return 0;

def main(args):

    folderName = args.path;
    outputName = args.output;
    outputType = args.type;

    fileBase = "storage\\" + folderName + "\\messages";

    fileNumber = 1;
    readingFiles = True;
    readError = False;
    allMessages = [];

    if (outputType == 'txt'):
        senderList = [];

    while (readingFiles):

        if (fileNumber == 1):
            fileString = fileBase + '.html';
        else:
            fileString = fileBase + str(fileNumber) + '.html';

        try:
            htmlFile = open(fileString, "r", encoding="utf-8");
        except:
            if (fileNumber == 1):
                print("Non existant file.");
                readError = True;
            else:
                print("Finished reading.");
            readingFiles = False;
            continue;


        print("Reading File: " + fileString);
        fileObject = htmlFile.readlines();

        dateRegex = re.compile(r'title=\"(\d+\.\d+\.\d+ \d+:\d+:\d+)\"');
        textRegex = re.compile(r'class=\"text\"');
        messageRegex = re.compile(r'id=\"message\d+\"');
        nameRegex = re.compile(r'class=\"from_name\"');
        joinedRegex = re.compile(r'joined');
        stickerRegex = re.compile(r'href=\"stickers/(.+)\">');

        step = 0;
        divCount = 0;
        foundName = "Null";
        isJoined = False;

        for line in fileObject:

            # FIND A MESSAGE
            if (step == 0):
                foundMessage = messageRegex.findall(line);

                if (foundMessage):
                    divCount = 0;
                    newMessage = [];

                    if (joinedRegex.findall(line)):
                        isJoined = True;
                    else:
                        isJoined = False;

                    step = 1;

            # FIND AND APPEND THE DATE
            elif (step == 1):
                foundDate = dateRegex.findall(line);

                if (foundDate):
                    divCount += 1;

                    if (outputType == 'xlsx'):
                        newMessage.append(foundDate[0]);

                    step += 1;
                else:
                    divCount += checkForDiv(line);

                    if (divCount < 0):
                        step = 0;

            # FIND THE SENDER
            elif (step == 2):
                if (isJoined):
                    newMessage.append(str(sender));
                    step = 4;
                else:
                    foundName = nameRegex.findall(line);
                    if (foundName):
                        divCount += 1;
                        step += 1;

                    else:
                        divCount += checkForDiv(line);
                        if (divCount < 0):
                            step = 0;

            # APPEND THE SENDER
            elif (step == 3):
                sender = line[:-1];

                newMessage.append(str(sender));
                if (sender not in senderList):
                    senderList.append(sender);

                step += 1;

            # FIND THE TEXT
            elif (step == 4):
                textLabel = textRegex.findall(line);
                if (textLabel):
                    divCount += 1;
                    step += 1;

                else:
                    stickerFound = stickerRegex.findall(line);
                    if (stickerFound):
                        divCount += 1;

                        if (outputType == 'xlsx'):
                            newMessage.append(str(stickerFound[0]));
                            newMessage.append("sticker");
                        step = 6;
                    else:
                        divCount += checkForDiv(line);
                        if (divCount < 0):
                            step = 0;

            elif (step == 5):
                messageText = line[:-1];
                messageText = messageText.lower();
                
                newMessage.append(str(messageText));
                if (outputType == 'xlsx'):
                    newMessage.append("text");
                step += 1;

            if (step == 6):
                allMessages.append(newMessage);
                step = 0;

        htmlFile.close();
        fileNumber += 1;

    if (readError):
        return;

    print("Writing output file");

    if (outputType == 'xlsx'):
        df = pd.DataFrame.from_records(allMessages);
        df.to_excel("storage\\" + outputName + ".xlsx");

    else:
        for sender in senderList:
            outputPath = "storage\\" + outputName + "_" + sender.strip() + ".txt";

            with open(outputPath, "w+", encoding="utf-8") as outputFile:
                for line in allMessages:
                    if (line[0] == sender and len(line) > 1):
                        outputFile.write(line[1]+"\n");

    print("Finished!");
    return;

def parse_arguments():

    parser = argparse.ArgumentParser(description='Create a file with all the messages from a chat.');

    parser.add_argument('path');
    parser.add_argument('output');
    parser.add_argument('--type', '-t', default='xlsx', choices=['xlsx', 'txt']);
    return parser.parse_args();


if __name__ == "__main__":
    arguments = parse_arguments();
    main(arguments);
