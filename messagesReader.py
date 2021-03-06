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

    folderName = args.FOLDER;
    outputName = args.outputFile;
    outputType = args.type;

    fileBase = "storage\\" + folderName + "\\messages";

    fileNumber = 1;
    readingFiles = True;
    readError = False;
    allMessages = [];

    if (outputType == 'txt'):
        senderList = [];
        stickerSenders = [];
        gifSenders = [];

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
        gifRegex = re.compile(r'href=\"video_files/(.+)\">');
        otherSenders = re.compile(r' via @');

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

                special = otherSenders.findall(line);

                if (special):
                    step = 0;
                else:
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

                        newMessage.append(str(stickerFound[0]));
                        newMessage.append("sticker");
                        if (sender not in stickerSenders):
                            stickerSenders.append(sender);

                        step = 6;
                    else:
                        gifFound = gifRegex.findall(line);
                        if (gifFound):
                            divCount += 1;

                            newMessage.append(str(gifFound[0]));
                            newMessage.append("gif");
                            if (sender not in gifSenders):
                                gifSenders.append(sender);

                            step = 6;

                        else:
                            divCount += checkForDiv(line);
                            if (divCount < 0):
                                step = 0;

            elif (step == 5):
                messageText = line[:-1];
                messageText = messageText.lower();

                newMessage.append(str(messageText));
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
            outputBase = "storage\\" + sender.strip();

            outputFileText = open(outputBase+'_text.txt', "w+", encoding="utf-8");
            if (sender in stickerSenders):
                outputFileSticker = open(outputBase+'_sticker.txt', "w+", encoding="utf-8");

            if (sender in gifSenders):
                outputFileGif = open(outputBase+'_gif.txt', "w+", encoding="utf-8");

            for line in allMessages:
                if (line[0] == sender and len(line) > 2):
                    if (line[2] == 'text'):
                        outputFileText.write(line[1]+"\n");
                    elif (line[2] == 'sticker'):
                        outputFileSticker.write(line[1]+"\n");
                    else:
                        outputFileGif.write(line[1]+"\n");

    print("Finished!");
    return;

def parse_arguments():

    parser = argparse.ArgumentParser(description='Create a file with all the messages from a chat.');

    parser.add_argument('FOLDER', help='Name of the history folder located in the storage/ directory');
    parser.add_argument('--outputFile', '-o', default='MessagesOutput', help='Name of the output file with table. If the text version is chosen then the name of each file will be the name of the senders.');
    parser.add_argument('--type', '-t', default='xlsx', choices=['xlsx', 'txt'], help='Xlsx will output one Excel file with a table of the messages. Txt will output two text file for each user, one with all text messages and the other with all stickers sent.');
    return parser.parse_args();


if __name__ == "__main__":
    arguments = parse_arguments();
    main(arguments);
