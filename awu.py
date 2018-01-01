#!/usr/bin/env python3

import sys
import argparse
import requests
import json
from colored import fg, bg, attr

version = "1.2"
boards = [ 'a', 'burg', 'cyb', 'd', 'lain', 'mu', 'new', 'tech', 'test', 'u', 'v', 'all' ]

# Initial colors
class colors:
    main   = 'blue'
    second = 'red'
    sticky = 'yellow'
    title  = 'purple_1b'



'''
"""     arg check
'''

parser = argparse.ArgumentParser()

parser.add_argument('-v', '--version', 
        help='Display current version',
        action="store_true")

parser.add_argument('-n', '--nocolor', 
        help='Disable the color scheme',
        action="store_true")

parser.add_argument('--colors',  
        type=str,
        nargs=4,
        help='Set a custom color scheme (hex codes). Use quotes.')

args = parser.parse_args()

if args.version:
    print('v1.1')
    sys.exit()

if args.nocolor:
    def fg(a):
        return ""
    def attr(a):
        return ""

if args.colors:
    colors.main   = args.colors[0]
    colors.second = args.colors[1]
    colors.sticky = args.colors[2]
    colors.title  = args.colors[3]


'''
"""     functions
'''

def board( boardname ):
    while True:
        # Board prompt
        userin = input('\n%s/%s' % ( fg(colors.second), fg(colors.main) ) + str(boardname) + 
                '%s/%s >> %s' % ( fg(colors.second), fg(colors.main), attr('reset') ))

        if "thread" in userin:
            if " list" in userin:
                # Thread counter
                tc = 0
                # Get front page threads from the API
                t = json.loads( requests.get("https://dangeru.us/api/v2/board/" + boardname + "?page=0").text )

                # If the thread counter exceeds 18 (max posts on a page), stop the counter and print the boards
                while tc < 20:
                    if ( t[tc]['is_locked'] == True ):
                        if ( t[tc]['sticky'] == True ):
                            th_color = colors.sticky
                        else:
                            th_color = "red"

                    elif ( t[tc]['sticky'] == True):
                        th_color = colors.sticky

                    else:
                        th_color = colors.main

                    # Please don't look at this I'm fucking retarded.
                    print('%s' % (fg(colors.second)),   str( t[tc]['post_id'] ) , 
                            '%s' % (fg(th_color)),  str( t[tc]['title'].encode('utf-8') )[2:][:-1] ,
                            '%s' % (fg(colors.second)), str( t[tc]['number_of_replies'] ) , 
                            '%s' % (attr('reset')) )

                    tc += 1

            elif " start" in userin:
                try:
                    th_subject = input('%sSubject >> %s' % ( fg(colors.main), fg(colors.second) ))
                    th_content = input('%sContent >> %s' % ( fg(colors.main), attr('reset') ))
                    th_confirm = input('%sConfirm (%sy%s/%sN%s) >> %s' % ( 
                        fg(colors.main), fg(colors.second),
                        fg(colors.main), fg(colors.second), 
                        fg(colors.main), fg(colors.second) ))

                    if th_confirm == "y" or th_confirm == "Y":
                        requests.post('https://dangeru.us/post', data = {'board': boardname, 'title': th_subject, 'comment': th_content})
                        print('> Thread created.')

                except KeyboardInterrupt:
                    pass

            elif len(userin) > 10:
                while True:
                    # Thread prompt
                    threadno = userin.split(' ')[1:][0]
                    threadnoC = '%s' % (fg(colors.second)) + userin.split(' ')[1:][0] 
                    th_userin = input('\n' + threadnoC + '%s >> %s' % ( fg(colors.main), attr('reset') ))

                    if th_userin == "show":
                       
                        # Thread meta from API
                        meta = json.loads(
                                requests.get("https://dangeru.us/api/v2/thread/" + threadno + "/metadata").text )

                        # Thread title
                        print( '\n%s[%s'      % (fg(colors.main),fg(colors.title)), 
                                meta['title'] + 
                                '%s]%s'       % (fg(colors.main),attr('reset')) )
                        
                        # Reply counter
                        rc = 0

                        # Get thread replies from the API
                        reps = json.loads( requests.get("https://dangeru.us/api/v2/thread/" + threadno + "/replies").text )

                        try:
                            while True:
                                try:
                                    cap = reps[rc]['capcode']
                                    is_capcode = '%s' % (fg(colors.second)) + str(cap)

                                except KeyError:
                                    is_capcode = '%sAnonymous' % (fg(colors.main))

                                # Please don't look at this either I'm fucking retarded
                                try:
                                    print(  '\n' + str(is_capcode),
                                            '%s(%s'       % (fg(colors.main), fg(colors.second))     + str(reps[rc]['hash']) +
                                            '%s)  No. %s' % (fg(colors.main), fg(colors.second))     + str(reps[rc]['post_id']) +
                                            '\n%s| %s'    % (fg(colors.main), attr('reset')) + str(reps[rc]['comment']) )
                                except UnicodeEncodeError:
                                    print(  '\n' + str(is_capcode),
                                            '%s(%s'       % (fg(colors.main), fg(colors.second))     + str(reps[rc]['hash']) +
                                            '%s)  No. %s' % (fg(colors.main), fg(colors.second))     + str(reps[rc]['post_id']) +
                                            '\n%s| %s'    % (fg(colors.main), attr('reset')) + str(reps[rc]['comment'].encode("utf-8") )[2:][:-1] )

                                rc += 1

                        except IndexError:
                            pass

                    elif th_userin == 'post':
                        try:
                            print("%sType your reply lines here, enter a single \".\" to end%s" % ( fg(colors.main), attr('reset') ))
                            reply = []
                            while True:
                                user_input = input('%sContent >> %s' % ( fg(colors.main), attr('reset') ));
                                if user_input == ".": break
                                reply.append(user_input)
                            post_content = "\n".join(reply)
                            post_confirm = input('%sConfirm (%sy%s/%sN%s) >> %s' % (
                                fg(colors.main), fg(colors.second),
                                fg(colors.main), fg(colors.second),
                                fg(colors.main), fg(colors.second) ))

                            if post_confirm == "y" or post_confirm == "Y":
                                requests.post('https://dangeru.us/reply', data = {'board': boardname, 'parent': threadno, 'content': post_content})
                                print('> Reply posted')

                        except KeyboardInterrupt:
                            pass

                    elif th_userin == 'back' or th_userin == 'up':
                        break

                    elif th_userin == 'exit' or th_userin == 'quit':
                        sys.exit()

                    else:
                        print('aw/u/:', th_userin +": unrecognized command")

            else:
                print("Example usage: thread list")
                print("               thread 61204")

        elif userin == "back" or userin == "up":
            break

        elif userin == "exit" or userin == "quit":
            sys.exit()

        else:
            print('aw/u/:', userin + ': unrecognized command')

print('\naw/u/ v' + version)
print('https://github.com/isvinc3s/awu')
print('Type `%shelp%s` or `%scommands%s` for a list of available commands.' % ( 
    fg(colors.second), attr('reset'),
    fg(colors.second), attr('reset') ))

while True:
    userin = input('\n%saw%s/%su%s/%s >> %s' % ( 
        fg(colors.main), fg(colors.second),
        fg(colors.main), fg(colors.second),
        fg(colors.main), attr('reset') ))

    if "board" in userin:
        if " list" in userin:
            print('/a/    - Anime & Manga')
            print('/burg/ - Burg')
            print('/cyb/  - Cyberpunk Life')
            print('/d/    - Doujin')
            print('/lain/ - Cyberpunk')
            print('/mu/   - Music')
            print('/new/  - News & Politics')
            print('/tech/ - Technology')
            print('/test/ - Awoo testing grounds')
            print('/u/    - Random')
            print('/v/    - Video games')
            print('/all/  - All')

        elif any( name in userin for name in boards ):
            try:
                board(str( userin.split(' ')[1:][0] ))
            except IndexError:
                print('Example usage: board list')
                print('               board cyb')

    elif userin == "commands" or userin == "help":
        print('board <option>       Enter a board')
        print('  list                 List available boards')
        print('  (name)               Enter the selected board')
        print('thread <option>      Enter or start a thread    (only works if you are on a board)')
        print('  start                Start a thread           (content must be one line)')
        print('  list                 List active threads')
        print('  (id)                 Enter the thread with the selected ID')
        print('show                 Show a thread\'s replies    (only works if you are in a therad)')
        print('post                 Reply to a thread          (only works if you are in a thread)')
        print('back                 Move up one level          (thread > board > aw/u/)')
        print('up                   Move up one level          (thread > board > aw/u/)')
        print('exit                 Terminate aw/u/')
        print('quit                 Terminate aw/u/')

    elif userin == "exit" or userin == "quit":
        sys.exit()

    else:
        print('aw/u/:', userin + ': unrecognized command')
