# TelegramChatWordFrequency

## Content

A Python script to obtain a table with all messages of a Telegram Chat. It will contain the timestamp, the sender, the content and the type (text or sticker) of each message.

R script to obtain a table with the frequency of the most used words for each user.

Another Python script to obtain the frequency of a specific word or phrase.

The final tables can be used with any intent, just for the information or to do some kind of dashboard.

## First Steps

### Setup Python

  1. Download and install Python 3;
  2. Install pip;
  3. Install pandas library with pip: &nbsp;&nbsp;&nbsp;&nbsp;`pip install pandas`.

### Setup R

  1. Download and install [R](https://cran.r-project.org);
    * Add its folder to the PATH environment variable if you want;
  2. Install the Text Mining package: &nbsp;&nbsp;&nbsp;&nbsp;`Rscript -e "install.packages('tm', repos='https://cran.rstudio.com')"`
    * Run it with admin/sudo permissions and with the path to Rscript, if it's not in the PATH variable.

### Download the Telegram History

  1. Download [Telegram for Desktop](https://desktop.telegram.org/);
  2. Log in;
  3. Select the chat you want to download;
  4. Click on the three dots on the upper right;
  5. Select "Export chat history";
  6. Define the limit as the maximum value (1500 MB) to get all data;
    * Choose Stickers and GIFs if you want.
  7. Click on "Export".

## messagesReader.py

This script read all the html files from the folder exported by Telegram and export the messages to an Excel table or to text files.

The Excel version will output one unique file .xlsx that contains a table with the timestamp, the name of the sender, the content of the message and its type (Text, Gif or Sticker). This table is ideal to analyze the messages sent over time and control it as desired.

The text version will output one file for each person of the chat. Each line of it is a message sent by the user in chronological order. This one is ideal to be used by the R script and obtain the Document Term Matrix of each user.

To run it put the history folder exported by Telegram on the 'storage' folder and then:

```shell
  py messagesReader.py [-h] [--outputFile OUTPUTFILE] [--type {xlsx,txt}] FOLDER
```

 * `FOLDER`: Name of the history folder located in the storage/ directory.
 * `--outputFile OUTPUTFILE`: Name of the output file with table. If the text version is chosen then t he name of each file will be the name of the senders.
 * `--type`: Xlsx will output one Excel file with a table of the messages. Txt will output two text file for each user, one with all text messages and the other with all stickers sent.

## wordCounter.py

This script looks for all occurrences of a list of words in a text file. It is case sensitive. The output with the frequency of each word is displayed in the terminal.

To run it put the text file in the 'storage' folder and then:

```shell
  py wordCounter.py [-h] FILE WORDS [words ...]
```

* `FILE`: Name of the file located in the storage/ directory.
* `WORDS`: List of terms to look for. They should be separated by spaces and inside quotes.
    * Example: &nbsp;&nbsp;&nbsp;&nbsp;`'py file "hello" "world" "hello world"'`

## wordFreq.R

This script will obtain the [Document Term Matrix](https://en.wikipedia.org/wiki/Document-term_matrix) of a text file.

To achieve a better result, it removes pontuation, extra white spaces, stop words of the chosen language, numbers and the terms: "hrefhttps", "href", "https" due to links shared in chats. It also replaces special characters like "/", "@" and "\\|" for spaces.

If you want to ignore these transformations use the mode "raw" and the matrix will be created without the text treatment. This mode is useful to analyze the frequency of stickers and GIFs in a chat.

To run it put the text file in the 'storage' folder and the:

```shell
    Rscript wordFreq.R FILE MODE LANG OUTPUT
```
