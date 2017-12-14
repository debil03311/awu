# aw/u/
A terminal client for [danger/u/](https://dangeru.us/)


## Installation
You're going to need `requests`, `json` and `colored` to get this to work properly.
```sh
$ git clone https://github.com/isvinc3s/awu.git
$ cd awu
$ python3 awu.py
```
If you want to run it as a regular command:
```
$ chmod +x awu.py
$ sudo cp ./awu.py /usr/local/bin/awu
```


## Documentation
Here's how to navigate around danger/u/ with aw/u/

### Boards
First of all you need to select a board to browse with the `board` command.

For example, if you wanted to browse /burg/ you would type `board burg`.
Once you have selected a board, the prompt will change from `aw/u/ >> ` to the board you selected.

### Threads
Once you're here, you can view active threads with the `thread list` command.

You select a thread by its ID, displayed to the left of it (e.g. `thread 62930`).
Now, once again, the prompt will change from the board to the thread ID.

The number displayed on the right side of the thread is the number of replies it has. 
Entering the thread doesn't affect this.

If you want to create a thread, use `thread start` on the desired board and fill out the prompts.

### Thread replies
Use the `show` command to display the thread replies.
To reply to the thread, simply type `post` and fill out the prompts.

### Other notes
- To go from a thread back to the board, or from a board back to aw/u/, use the `back` or `up` commands.
- Keep in mind you can\'t have multiple lines in the content of your thread or reply.
- Use ^C to cancel the reply or thread creation.
- Stickied threads are displayed in yellow
- If you reply with anything other than "burg" on a /burg/ thread, angry burg will be posted.


## To do
- Make it so that you can browse more pages of a board
- Display thread title when you show the replies
- ~~No color mode (I'm probably too retarded to do that so don't expect it to ever be a thing)~~ (Added in 1.1)
- Clean up the code (lol I definetly won't do this)
