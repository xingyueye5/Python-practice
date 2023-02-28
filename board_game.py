board={'tl':' ','tm':' ','tr':' ','ml':' ','mm':' ','mr':' ','bl':' ','bm':' ','br':' '}
mmap={1: 'tl',2: 'tm',3: 'tr',4: 'ml',5: 'mm',6: 'mr',7: 'bl',8: 'bm',9: 'br'}   ##uesd to substitude the switch statement
num=1


def print_board(board):
    print(board['tl']+' | '+board['tm']+' | '+board['tr'])
    print('——|———|——')
    print(board['ml']+' | '+board['mm']+' | '+board['mr'])
    print('——|———|——')
    print(board['bl']+' | '+board['bm']+' | '+board['br'])


def layout(board,pos):       ##enter 'O' and 'X' in terns
    global num
    if pos>9:
        print('Invalid operation')
        return 0
    position=mmap[pos]
    if board[position]=='X' or board[position]=='O':
        print('Invalid operation')
        return 0
    elif num%2==1:
        board[position]='O'
        num=num+1
        return checkwin(board,pos)
    else:
        board[position]='X'
        num=num+1
        return checkwin(board,pos)


def checkwin(board,pos):            ##if ok, 0; if O wins, 1; if X wins,2
    if pos==1 or pos==9 or pos==5:
        if board['tl']=='X' and board['mm']=='X' and board['br']=='X':return 2
        elif board['tl']=='O' and board['mm']=='O' and board['br']=='O': return 1
    elif pos==3 or pos==7 or pos==5:
        if board['tr']=='X' and board['mm']=='X' and board['bl']=='X':return 2
        elif board['tr']=='O' and board['mm']=='O' and board['bl']=='O': return 1
    row=(pos-1)//3
    if pos%3!=0:col=pos%3
    else: col=3
    list=[0,0,0,0]
    for i in range(1,4):
        if board[mmap[row*3+i]]=='O':list[0]=list[0]+1
        if board[mmap[row*3+i]]=='X':list[1]=list[1]+1
        if board[mmap[i*3+col-3]]=='O':list[2]=list[2]+1
        if board[mmap[i*3+col-3]]=='X':list[3]=list[3]+1
    if list[0]==3 or list[2]==3:return 1
    elif list[1]==3 or list[3]==3: return 2
    else: return 0


if __name__=='__main__':
    print_board(board)
    print('Please enter your chess:')
    while(1):
        temp=int(input())
        res=layout(board,temp)
        print_board(board)
        if res!=0 or num==10:
            if res==1:
                print('O wins !')
            elif res==2:
                print('X wins !')
            else: print('Reach a draw!')
            print('Do you wanna restart ? y/n')
            choose=input()
            if choose=='y':
                board={'tl':' ','tm':' ','tr':' ','ml':' ','mm':' ','mr':' ','bl':' ','bm':' ','br':' '}
                num=1
                print_board(board)
                print('Please enter your chess:')
            else: break




