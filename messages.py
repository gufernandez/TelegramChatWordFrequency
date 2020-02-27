#! python3

import re
import pandas as pd

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

def main():

    fileBase = "C:\\Users\\goncalg4\\Downloads\\Telegram Desktop\\ChatExport_25_02_2020 - Pessoal\\messages";
    fileNumber = 1;
    allMessages = [];

    while (fileNumber <= 83):
        if (fileNumber == 1):
            fileString = fileBase + '.html';
        else:
            fileString = fileBase + str(fileNumber) + '.html';

        f = open(fileString, "r", encoding="utf-8");
        print("Reading File:" + fileString);
        f1 = f.readlines();

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

        for line in f1:

            # FIND A MESSAGE
            if (step == 0):
                foundMessage = messageRegex.findall(line);

                if (foundMessage):
                    # print(foundMessage);
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
                    # print(foundDate[0]);
                    divCount += 1;

                    newMessage.append(foundDate[0]);

                    step += 1;
                else:
                    divCount += checkForDiv(line);

                    if (divCount < 0):
                        step = 0;

            # FIND THE SENDER
            elif (step == 2):
                if (isJoined):
                    newMessage.append(sender);
                    step = 4;
                else:
                    foundName = nameRegex.findall(line);
                    if (foundName):
                        # print(foundName);
                        divCount += 1;
                        step += 1;

                    else:
                        divCount += checkForDiv(line);
                        if (divCount < 0):
                            step = 0;

            # APPEND THE SENDER
            elif (step == 3):
                sender = line[:-1];
                # print(sender);

                newMessage.append(sender);

                step += 1;

            # FIND THE TEXT
            elif (step == 4):
                textLabel = textRegex.findall(line);
                if (textLabel):
                    # print(textLabel);
                    divCount += 1;
                    step += 1;

                else:
                    stickerFound = stickerRegex.findall(line);
                    if (stickerFound):
                        divCount += 1;

                        newMessage.append(stickerFound[0]);
                        newMessage.append("sticker");
                        step = 6;
                    else:
                        divCount += checkForDiv(line);
                        if (divCount < 0):
                            step = 0;

            elif (step == 5):
                messageText = line[:-1];
                # print(messageText);

                newMessage.append(messageText);
                newMessage.append("text");
                step += 1;

            if (step == 6):
                allMessages.append(newMessage);
                step = 0;

        f.close();
        fileNumber += 1;

    df = pd.DataFrame.from_records(allMessages);
    df.to_excel("output.xlsx");

if __name__ == "__main__":
    main();
