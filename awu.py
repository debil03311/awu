#!/usr/bin/env python3

import sys
import requests
import json
from colored import fg, bg, attr

version = "1.1"
boards = [ 'a', 'burg', 'cyb', 'd', 'lain', 'mu', 'new', 'tech', 'test', 'u', 'v', 'all' ]

try:
    if sys.argv[1] == "--help":
        print('Commands:')
        print('    --help      Show this list')
        print('    --version   Display version information')
        print('    --nocolor   Disable the color scheme')
    
    elif sys.argv[1] == "--version":
        print('v' + version)

    elif sys.argv[1] == "--nocolor":
        def fg(a):
            return ""
        def attr(a):
            return ""

        if sys.argv[2] == "xD I don't know how to make a good argument thing lol":
            pass

except IndexError:

    def board( boardname ):
        while True:
            # Board prompt
            userin = input('\n%s/%s' % ( fg('red'), fg('blue') ) + str(boardname) + 
                    '%s/%s >> %s' % ( fg('red'), fg('blue'), attr('reset') ))

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
                                th_color = "yellow"
                            else:
                                th_color = "red"

                        elif ( t[tc]['sticky'] == True):
                            th_color = "yellow"

                        else:
                            th_color = "blue"
                        
                        # Please don't look at this I'm fucking retarded.
                        print('%s' % (fg('red'))       , str( t[tc]['post_id'] ) , 
                                '%s' % (fg(th_color)) , str( t[tc]['title'].encode('utf-8') )[2:][:-1] ,
                                '%s' % (fg('red'))     , str( t[tc]['number_of_replies'] ) , 
                                '%s' % (attr('reset')) )

                        tc += 1

                elif " start" in userin:
                    try:
                        th_subject = input('%sSubject >> %s' % ( fg('blue'), fg('red') ))
                        th_content = input('%sContent >> %s' % ( fg('blue'), attr('reset') ))
                        th_confirm = input('%sConfirm (%sy%s/%sN%s) >> %s' % ( 
                            fg('blue'), fg('red'),
                            fg('blue'), fg('red'), 
                            fg('blue'), fg('red') ))

                        if th_confirm == "y" or th_confirm == "Y":
                            requests.post('https://dangeru.us/post', data = {'board': boardname, 'title': th_subject, 'comment': th_content})
                            print('> Thread created.')

                    except KeyboardInterrupt:
                        pass

                elif len(userin) > 10:
                    while True:
		        # Thread prompt
                        threadno = userin.split(' ')[1:][0]
                        threadnoC = '%s' % (fg('red')) + userin.split(' ')[1:][0] 
                        th_userin = input('\n' + threadnoC + '%s >> %s' % ( fg('blue'), attr('reset') ))

                        if th_userin == "show":
                            # Reply counter
                            rc = 0
                            # Get thread replies from the API
                            reps = json.loads( requests.get("https://dangeru.us/api/v2/thread/" + threadno + "/replies").text )

                            try:
                                while True:
                                    try:
                                        cap = reps[rc]['capcode']
                                        is_capcode = '%s' % (fg('red')) + str(cap)
                                    
                                    except KeyError:
                                        is_capcode = '%sAnonymous' % (fg('blue'))

                                    # Please don't look at this either I'm fucking retarded
                                    try:
                                        print(  '\n' + str(is_capcode),
                                                '%s(%s'       % (fg('blue'), fg('red'))     + str(reps[rc]['hash']) +
                                                '%s)  No. %s' % (fg('blue'), fg('red'))     + str(reps[rc]['post_id']) +
                                                '\n%s| %s'    % (fg('blue'), attr('reset')) + str(reps[rc]['comment']) )
                                    except UnicodeEncodeError:
                                         print(  '\n' + str(is_capcode),
                                                '%s(%s'       % (fg('blue'), fg('red'))     + str(reps[rc]['hash']) +
                                                '%s)  No. %s' % (fg('blue'), fg('red'))     + str(reps[rc]['post_id']) +
                                                '\n%s| %s'    % (fg('blue'), attr('reset')) + str(reps[rc]['comment'].encode("utf-8") )[2:][:-1] )

                                    rc += 1

                            except IndexError:
                                pass

                        elif th_userin == 'post':
                            try:
                                post_content = input('%sContent >> %s' % ( fg('blue'), attr('reset') ))
                                post_confirm = input('%sConfirm (%sy%s/%sN%s) >> %s' % (
                                        fg('blue'), fg('red'),
                                        fg('blue'), fg('red'),
                                        fg('blue'), fg('red') ))

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

    print('aw/u/ is version', version)
    print('Type `%shelp%s` or `%scommands%s` for a list of available commands.' % ( 
        fg('red'), attr('reset'),
        fg('red'), attr('reset') ))
    
    while True:
        userin = input('\n%saw%s/%su%s/%s >> %s' % ( 
            fg('blue'), fg('red'),
            fg('blue'), fg('red'),
            fg('blue'), attr('reset') ))

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
