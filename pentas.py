import numpy as np

class Pentas:


    ##### Class variables #####    
    boardsize_v=8
    boardsize_h=8

    boardsize=[boardsize_v, boardsize_h]

    ###########################
    ##### Piece utilities #####    
    ###########################

    pieces= [
        [
            "ooooo" #I
        ],
        [
            "oooo", #L
            "oxxx"
        ],
        [
            "oooo", #Y
            "xoxx"
        ],
        [
            "xooo", #N
            "ooxx"
        ],
        [
            "xox", #X
            "ooo",
            "xox"
        ],
        [
            "oxx", #F
            "ooo",
            "xox"
        ],
        [
            "oxx", #T
            "ooo",
            "oxx"
        ],
        [
            "oxx", #V
            "oxx",
            "ooo"
        ],
        [
            "oxx", #Z
            "ooo",
            "xxo"
        ],
        [
            "oxx", #W
            "oox",
            "xoo"
        ],
        [
            "oox", #P
            "ooo"
        ],
        [
            "oxo", #U
            "ooo"
        ]
    ]

    ##### Private functions for piece manipuration
    ##### They are needed only at when the class was imported

    # convert the original "o","x" list to 0,1 array
    def __convert_piece_in_array(piece_str_array):
        ret=[]

        for elem in piece_str_array:
            ret2=[]
            for elem1 in elem:
                ret3=[]
                for ii in elem1:
                    aa=0
                    if ii=='o':
                        aa=1
                    ret3.append(aa)
                
                ret2.append(ret3)

            ret.append(ret2)

        return(ret)

    def __convert_to_piece_poslist(piece_array_list):
        # geometrical operations for the piece arrays (expressed by 0,1)
        def __piece_h_mirror(piece_array):
            return np.array([np.flip(ii) for ii in piece_array],dtype=int)
            
        def __piece_v_mirror(piece_array):
            return np.flip(piece_array)
            
        def __piece_transpose(piece_array):
            return piece_array.T
            
        def __piece_cw90(piece_array):
            return __piece_h_mirror(__piece_transpose(piece_array))
            
        def __piece_ccw90(piece_array):
            return piece_transpose(__piece_h_mirror(piece_array))
            
        # returns if an array can be found in the array_list or not
        def __array_is_in(ary, array_list):
            ret=False
            for ii in array_list:
                if np.array_equal(ii,ary):
                    ret=True
            return ret

        # from the 0/1 piece variations into position list
        def __convert_piece_variation_to_poslist(piece_array):
            sP=np.shape(piece_array)
            ind=np.array([])
    
            for ii, row in enumerate(piece_array): #rows loop
                ind=np.concatenate((ind,(row*np.arange(1,len(row)+1)+(ii*8)*row).astype('int')))

            ret = (np.trim_zeros(np.unique(ind))-1).astype('int')

            return ret

        # produce all the piece variations (rotation/mirror) from the piece array
        def __piece_variations(piece_array):
            p  = np.array(piece_array)
            pT = __piece_transpose(p)

            plist=[p]
            if not __array_is_in(pT,plist):
                plist.append(pT)

            for ii in range(3): # 90deg, 180deg, 270deg rotation of p and pT
                p = __piece_cw90(p)
                if not __array_is_in(p,plist):
                    plist.append(p)

                pT= __piece_cw90(pT)
                if not __array_is_in(pT,plist):
                    plist.append(pT)
    
            pos_list =[]
            for p in plist:
                pos_list.append(__convert_piece_variation_to_poslist(p))

            return(pos_list)

        ret=[]
        for piece_array in piece_array_list:
            ret.append(__piece_variations(piece_array))
        return ret

    ##### Class variables. They use the above private functions
    piece_array    =__convert_piece_in_array(pieces)

    piece_array_vmax = max(map(len, piece_array))
    piece_array_hmax = max([max(map(len,ii)) for ii in piece_array])

    piece_poslist  = __convert_to_piece_poslist(piece_array)
    
    ##### Class method (public)
    def pick_piece():
        return np.random.randint(0, len(Pentas.pieces))


    #############################
    ##### Display utilities #####    
    #############################

    ##### Class method (public)
    def display_board(turns, turn=-1, placement=[]):
        # Pentas.display_board(p) just display the latest board
        # Pentas.display_board(p,turn) display a specified turn
        # Pentas.display_board(p,placement=[0,[0,0]]) display with a placement

        h=Pentas.boardsize_h
        v=Pentas.boardsize_v
        t=turns[turn]
        brd=t['board']
        brd_list=np.reshape(brd, (h,v)).tolist()

        display=[]
        display = Pentas.__display_board_preparation(display,brd_list)
        display = Pentas.__display_add_piece(display,t['current_piece'],'current')
        display = Pentas.__display_add_piece(display,t['next_piece'],'next')
        display = Pentas.__display_add_stats(display,t)

        if len(placement)==2:
            var=placement[0]
            pos=placement[1]
            char='#'
            display = Pentas.__display_piece_preview(display,t['current_piece'],var,pos,char)
            
        for ii in display:
            print(ii)
            
    ##### Class method (private)
    def __display_board_preparation(display,brd_list):
        display = ['  '+' '.join(map(str,range(Pentas.boardsize_h)))]

        for ii in range(0,Pentas.boardsize_v):
            board_str = ' '.join(map(str,brd_list[ii]))
            board_str=board_str.replace('0',u'\u2591')
            board_str=board_str.replace('1',u'\u2588')

            display.append(str(ii)+' '+board_str)

        return(display)

    def __display_add_piece(display,piece_no, caption):

        piece = Pentas.piece_array[piece_no]
        vmax=Pentas.piece_array_vmax
        hmax=Pentas.piece_array_hmax
        
        display[0] = display[0]+('  '+caption+' '*(hmax*2))[0:hmax*2+2]
        for ii in range(vmax):
            if ii<len(piece):
                piece_str = ' '.join(map(str,piece[ii]))
                piece_str = piece_str.replace('0', ' ')
                piece_str = piece_str.replace('1',u'\u2588')
            else:
                piece_str=''

            piece_str = piece_str+' '*(hmax*2)
            piece_str = piece_str[0:hmax*2]

            display[ii+1]= display[ii+1] + '  '+piece_str+' '*(7-len(piece_str))
        return(display)

    def __display_add_stats(display,turn):
        v=Pentas.boardsize_v
        display[v-2] = display[v-2] + '  Turn: '  +str(turn['turn'])
        display[v-1] = display[v-1] + '  Score: ' +str(turn['score'])
        display[v-0] = display[v-0] + '  Lines: '+str(turn['lines'])

        return(display)

    def __display_piece_preview(display,piece,var,pos,char):
        poslist = Pentas.piece_poslist[piece][var]

        pos_v=pos[0]
        pos_h=pos[1]

        for ii in poslist:
            v=int(ii/Pentas.boardsize_v)+pos_v
            h=int(ii % Pentas.boardsize_v)+pos_h
            display[v+1]=display[v+1][0:h*2+2]+char+' '+display[v+1][h*2+4:]

        return(display)


    ###########################
    ##### Board utilities #####    
    ###########################

    ##### Board Class method (public)
    def derive_possible_moves(board,piece):
        h=Pentas.boardsize_h
        v=Pentas.boardsize_v

        possible_move=[]

        for ii, piece_pos in enumerate(Pentas.piece_poslist[piece]):
            # determine the piece size for this variation
            v_size = int(np.max(np.ceil((piece_pos+1)/h)))
            h_size = int(np.max(piece_pos % h))+1
            
            pmove=[]

            # Scan piece for possible positions
            for posv in range(v-v_size+1):
                for posh in range(h-h_size+1):
                    block_ofs = posh+h*posv

                    if np.prod(board[piece_pos+block_ofs])==1:
                    #for ii in piece_pos:
                        # if even a single block is already taken for this piece variation
                        # block is goning to be 0
                    #    block = block * board[ii+block_ofs]
                    
                        # The piece variation could be placed
                    #if block == 1:
                        pmove.append([posv,posh])

            possible_move.append(pmove)

        return possible_move
    
    def apply_piece(board,piece,variation,position):
        piece_pos=Pentas.piece_poslist[piece][variation]
        new_board = np.copy(board)

        posv=position[0]
        posh=position[1]

        block_ofs = posh+Pentas.boardsize_h*posv
    
        #for ii in piece_pos:
        #    new_board[ii+block_ofs] = 0

        new_board[piece_pos+block_ofs]=0
        
        return new_board

    def check_if_line_cleared(board):
        h = Pentas.boardsize_h
        v = Pentas.boardsize_v
        
        num_cleared_lines = 0
        new_board = np.copy(board).reshape((v,h))

        for vnum,line in enumerate(new_board):
            if np.sum(line)==0:
                num_cleared_lines = num_cleared_lines + 1
                new_board=np.vstack((np.ones(h,dtype=int),np.delete(new_board,vnum,0)))

        new_board = new_board.reshape((v*h))
        return new_board, num_cleared_lines

    # static parts for the surface area calc
    aryA0 = np.zeros((boardsize_v, 1),int)
    aryA1 = np.ones( (boardsize_v, 1),int)
    aryB  = np.zeros((boardsize_v, 2),int)
    
    def calc_surface_area(board):
        brd=board.reshape(Pentas.boardsize_h,Pentas.boardsize_v)    
        A=np.concatenate([Pentas.aryA0,brd,Pentas.aryA0],1)
        B=np.concatenate([brd,Pentas.aryB],1)
        sumH=sum(np.abs(A-B).flatten().tolist())

        brdT=brd.T
        A=np.concatenate([Pentas.aryA1,brdT,Pentas.aryA0],1)
        B=np.concatenate([brdT,Pentas.aryB],1)
        sumV=sum(np.abs(A-B).flatten().tolist())

        return(sumH+sumV)

    ###########################
    ##### Board utilities #####    
    ###########################

    def init_new_game():
        turns=[{
            'turn': 0,
            'board': np.array([1]*Pentas.boardsize_v*Pentas.boardsize_h),
            'score': 0,
            'lines': 0,
            'current_piece': Pentas.pick_piece(),
            'next_piece': Pentas.pick_piece()
        }]
        return(turns)


    def execute_a_turn(turns,piece,variation,position,turn=-1):
        if turn == -1:
            # determine explicit turn no for the turn = -1
            turn=turns[-1]['turn']

        # record this move
        turns[turn]["placement"]=[variation,position]

        board = turns[turn]['board']
        new_board = Pentas.apply_piece(board,piece,variation,position)
        new_board, clear_lines = Pentas.check_if_line_cleared(new_board)

        piece_pos = Pentas.piece_poslist[piece][variation]
        new_turn = turn+1
        new_score=turns[turn]['score']+len(piece_pos)+clear_lines*8
        #new_score
        new_lines=turns[turn]['lines']+clear_lines
        new_current_piece=turns[turn]['next_piece']
        new_next_piece=Pentas.pick_piece()

        turns=turns[0:turn+1]
        turns.append(
            {
                'turn': new_turn,
                'board': new_board,
                'score': new_score,
                'lines': new_lines,
                'current_piece': new_current_piece,
                'next_piece': new_next_piece
            }
        )

        return(turns)


    def latest_board(turns):
        return(turns[-1]['board'])
