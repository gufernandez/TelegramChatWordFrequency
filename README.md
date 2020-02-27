# TelegramChatWordFrequency

## Content

A Python script to obtain a table with all messages of a Telegram Chat. It will contain the timestamp, the sender, the content and the type (text or sticker) of each message.

R script to obtain a table with the frequency of the most used words for each user.

Another Python script to obtain the frequency of a specific word or phrase.

The final tables can be used with any intent, just for the information or to do some kind of dashboard.

## First Steps

### Setup Python

  - Download and install Python 3
  - Install pip
  - Install pandas library with pip

  pip install pandas


### Setup R

  - Download R (https://cran.r-project.org)

### Download the Telegram History

  1. Download the Telegram for desktop (https://desktop.telegram.org/);
  2. Log in;
  3. Select the chat you want to download;
  4. Click on the three dots on the upper right;
  5. Select "Export chat history"
  6. Select the options for the download and click

## messagesReader.py

This script read all the html files from the folder exported by Telegram and export the messages to an Excel table or to text files.

The Excel version will output one unique file .xlsx that contains a table with the timestamp, the name of the sender, the content of the message and its type (Text, Gif or Sticker). This table is ideal to analyze the messages sent over time and control it as desired.

The text version will output one file for each person of the chat. Each line of it is a message sent by the user in chronological order. This one is ideal to be used by the R script and obtain the Document Term Matrix of each user.

To run it put the history folder exported by Telegram on the 'storage' folder and then:

```shell
  py messagesReader.py [-h] [--outputFile OUTPUTFILE] [--type {xlsx,txt}] FOLDER
```

FOLDER: Name of the history folder located in the storage/ directory
--outputFile OUTPUTFILE: Name of the output file with table. If the text version is chosen then the name of each file will be the name of the senders.
--type: Xlsx will output one Excel file with a table of the messages. Txt will output two text file for each user, one with all text messages and the other with all stickers sent.



### (UNDER DEVELOPMENT...)
