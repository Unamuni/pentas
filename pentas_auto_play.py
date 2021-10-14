#!/Users/karai/opt/anaconda3/bin/python3

# imports

import numpy as np
import time
import os

from pentas import Pentas

import importlib
import pickle
from datetime import datetime

num_of_games=1
line_clear_bonus=3

for game_no in range(num_of_games):
    start_time = time.time()
    print('Game #: ', game_no, ' started.')

    p=Pentas.init_new_game()
    game_continue=1

    while(game_continue):

        cur_p=p[-1]['current_piece']
        nex_p=p[-1]['next_piece']

        sa=10000
        sol=[]

        latest_brd=Pentas.latest_board(p)
        possible_pos1=Pentas.derive_possible_moves(latest_brd,cur_p)

        for var_num, var in enumerate(possible_pos1):
            if not var==[]:
                for pos in var:

                    brd=Pentas.apply_piece(latest_brd,cur_p,var_num,pos)
                    brd, clear_lines = Pentas.check_if_line_cleared(brd)

                    
                    possible_pos2=Pentas.derive_possible_moves(brd,nex_p)
            
                    for var_num2, var2 in enumerate(possible_pos2):
                        if not var2==[]:
                            for pos2 in var2:

                                brd2=Pentas.apply_piece(brd,nex_p,var_num2,pos2)
                                brd2, clear_lines2 = Pentas.check_if_line_cleared(brd2)
                                # current score
                                sa2=Pentas.calc_surface_area(brd2)-(clear_lines-clear_lines2)*line_clear_bonus
                                
                                # compare the current score and the current best
                                if sa2==sa:
                                    # add a new candidate 
                                    sol.append([[var_num,pos],[var_num2,pos2]]) 
                                elif sa2<sa:
                                    # update the cost function minimum
                                    sa=sa2 
                                    # register a new candidate 
                                    # the old ones are purged
                                    sol=[[[var_num,pos],[var_num2,pos2]]] 

        if(sol==[]):
            for var_num, var in enumerate(possible_pos1):
                if not var==[]:
                    for pos in var:
                        sol=[[[var_num,pos]]]     

        if(sol==[]):
            Pentas.display_board(p)
            print("+++++++++++++++++")
            print("+++++++END+++++++")
            print("+++++++++++++++++")
            end_time = time.time()
        
            timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
            print(timestr,' score: ',p[-1]['score'])
            print(end_time-start_time, '[sec] for ', p[-1]['turn'])
            print((end_time-start_time)/p[-1]['turn'], '[turns/sec]')

            if not os.path.exists('log'):
                os.mkdir('log')

            fp = open('./log/'+timestr+'.log','wb')
            pickle.dump(p,fp)
            fp.close()

            game_continue=0
        else:
            s=sol[-1] # pick the last solution i.e. the most bottom right 
            #Pentas.display_board(p,-1,s[0]) # next move preview        
            p=Pentas.execute_a_turn(p,p[-1]['current_piece'],s[0][0],s[0][1])
            #Pentas.display_board(p,turn=-1) # check the result
            print('turn: {turn}, score: {score}'.format(turn=p[-1]['turn'],score=p[-1]['score']))
            #print("")
