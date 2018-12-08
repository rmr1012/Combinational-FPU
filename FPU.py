import struct
import random
import numpy as np
import contextlib
import io
import sys



@contextlib.contextmanager
def mute():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout

def neg(bini):
    bino=''
    for bi in bini:
        bino+=str(int(not bool(int(bi))))
    return bino
def pureAdd(cin,a,b):
    a=a.zfill(len(b))
    b=b.zfill(len(a))
    a=a.zfill(len(b))
    lenn=len(a)
    a_rev=a[::-1]
    b_rev=b[::-1]
    CO=cin
    c=''
    # print(a_rev,b_rev)
    for index in range(len(a_rev)):
        bs=int(a_rev[index]) + int(b_rev[index]) + int(CO)
        # print(bs)
        # print("C:",c)
        if (bs==3):
            c+="1"
            CO=1
        elif (bs==2):
            c+="0"
            CO=1
        elif (bs==1):
            c+="1"
            CO=0
        else:
            c+="0"
            CO=0
    # if CO:
    #     c+="1"
    return int(CO),c[::-1].zfill(lenn)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
def rr(num):
    return int(31-num)
def mm(num):
    return int(23-num)
def expComp(a_exp, b_exp):
    if (int(a_exp,2) > int(b_exp,2)):
        print("a exp is bigger by ",int(a_exp,2) - int(b_exp,2))
        return True,int(a_exp,2) - int(b_exp,2)
    else:
        print("b exp is bigger by ",int(b_exp,2) - int(a_exp,2))
        return False,int(b_exp,2) - int(a_exp,2)
def shiftMant(largeGuy, bits, a_mant,b_mant):
    #print(a_mant, b_mant)
    if (largeGuy):
        print("shifting b right by ",bits)
        b_mant_s=b_mant[mm(23):mm(bits-1)].zfill(24) # shouhld be bits but python
        a_mant_s=a_mant
    else:
        print("shifting a right by ",bits)

        a_mant_s=a_mant[mm(23):mm(bits-1)].zfill(24)
        b_mant_s=b_mant
    return a_mant_s,b_mant_s
dd={0:'-',1:'+'}
dt={"0":1,"1":0}
def mantALU(a,b,sign1,sign2,a_sign,b_sign,dominance):
    print("adding shifted mant")
    print("sign1",dd[sign1], "sign2",dd[sign2])
    # a_int=int(a,2)
    # b_int=int(b,2)
    agree=not(sign1 ^ sign2)
    if agree:
        sign=not sign1
    else:
        print("signs disagree, choosing dominance sign")
        if dominance:
            sign=sign2
        else:
            sign=sign1

    if sign1 and sign2:
        of,c=pureAdd(0,a,b)  # add one to round idk why
    elif sign1 and not sign2:
        of,c=pureAdd(0,a,neg(b))
    elif not sign1 and sign2:
        of,c=pureAdd(0,neg(a),b)
    elif not sign1 and not sign2:
        of,c=pureAdd(0,neg(a),neg(b))

    print("raw result\t",c)

    #switch({of,sign,agree})
    #case 101:
        #c=c+1;
        #c={sign1,c[24:1]}
    if of and not sign and agree:
        print("Overflow detected agree")
        of1,c=pureAdd(0,c,'1') # add one to C
        c=str(int(sign1))+c[:-1]
    #case 100:
        #c=c+1;
        #c={sign1,c[24:1]}
        #of=0
    elif of and not sign and not agree:
        print("Overflow detected not agree")
        of=0

    #case 11x:
        #sign = !sign;
        #c=c+1

    elif of and sign:
        print("Underflow detected, going to negative")

        sign=1-sign # flip signbit
        of,c=pureAdd(0,c,'1') # add one to C
    #case 011:
        #of=1
        #c={sign1,c[24:1]}
    elif not of and sign and agree:
        of=1
        print("no Underflow for matched sub")
        c=str(int(sign1))+c[:-1]


    if sign: # if negative
        c=neg(c)
        print("negating result")

    print("C no Supp:\t",c)

    return str(int(sign)),of,c
def prioirityEncoder(c_mant):
    for index, char in enumerate(c_mant):
        if char=="1":
            print("need to normalize by ",index, " bits")
            return index
def normalizeMant(c_mant,bits,c_sign,exp_t):
    print("shifting c_mant left by ",bits,"bits")
    c_mant_s=c_mant[bits:]+(bits*str((1-int(c_sign)) and int(exp_t)) )
    return c_mant_s
def FPU(a,b,addSign=True):
    print("------------------ new PFU op ------------------")
    abin=bin(int(a, 16))[2:].zfill(32)
    bbin=bin(int(b, 16))[2:].zfill(32)

    print(abin,bbin)
    a_sign=abin[rr(31)]
    b_sign=bbin[rr(31)]
    a_exp=abin[rr(30):rr(22)]# should be 23 but python
    b_exp=bbin[rr(30):rr(22)]# should be 23 but python
    a_mant="1"+abin[rr(22):rr(-1)] # hsould be 0 but python // also add hidden bit
    b_mant="1"+bbin[rr(22):rr(-1)]# hsould be 0 but python  // also add hidden bit
    print(a_sign,a_exp,a_mant)
    print(b_sign,b_exp,b_mant)
    dominance,howmuch=expComp(a_exp,b_exp) # dominance True -> a False -> b

    a_mant_s, b_mant_s = shiftMant(dominance,howmuch,a_mant,b_mant)
    print(a_sign,a_exp,a_mant_s)
    print(b_sign,b_exp,b_mant_s)

    c_sign,overflow , c_mant=mantALU(a_mant_s,b_mant_s, not int(a_sign) , int(b_sign)^addSign, a_sign, b_sign,dominance)
    print("result mant \t" , c_mant)
    if dominance:
        c_exp=a_exp
    else:
        c_exp=b_exp


    bits=prioirityEncoder(c_mant)
    print("adjusting exp for overflow ...",overflow)

    c_exp_s=bin(int(c_exp,2)-bits+overflow)[2:].zfill(8) #
    c_mant_s=normalizeMant(c_mant,bits,c_sign,c_exp_s[0])



    print(c_sign,c_exp_s,c_mant_s)
    c=c_sign+c_exp_s+c_mant_s[1:] # take out hidden bit
    return c
    ##
def fh(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]
def hf(h):
    return struct.unpack('!f', bytes.fromhex(h))[0]
def fatTest(iters):
    fc=0
    typeBin=[0,0,0,0]
    signMatchBin=0

    FA=[]
    for i in range(iters):
        a=np.float32(np.exp(random.uniform(-5,5)))
        b=np.float32(np.exp(random.uniform(-5,5)))
        op=random.randint(0,1) # 1 + , 0 -
        with mute():
            res=FPU(fh(a),fh(b),op)
        if op:
            c=a+b
            print(a," (+) ",b," = ",c)

        else:
            c=a-b
            print(a," (-) ",b," = ",c)
        sign1=True if a >=0 else False
        signb=True if b >=0 else False
        sign2=signb ^ 1-op
        signc=True if c >=0 else False
        if(sign1 and sign2):
            type="+ +"
            ntype=0
        if(sign1 and not sign2):
            type="+ -"
            ntype=1
        if(not sign1 and sign2):
            type="- +"
            ntype=2
        if(not sign1 and not sign2):
            type="- -"
            ntype=3

        flt=hf(hex(int(res,2))[2:])
        print(flt)
        signf=True if flt >=0 else False
        pnp=abs(flt - c)/c <= .000001
        print(bcolors.OKGREEN+"Pass" if pnp else bcolors.FAIL+"Fail")
        print(bcolors.ENDC)
        if not pnp:
            signMatchBin+=0 if signf==signc else 1
            typeBin[ntype]+=1
            FA.append([a,b,op,c,flt,type,signf==signc])
            fc=fc+1
    print((iters-fc)*100/iters,"% passed")

    import csv
    with open("output.csv", "w") as f:

        writer = csv.writer(f)
        writer.writerows([["a","b","op","c","output","type","sign Match"]])
        writer.writerows(FA)
    print(typeBin)
    print(signMatchBin)
    return FA
def testFA(FA,iter):
    for index,line in enumerate(FA):
        if index>=iter:
            return
        a=line[0]
        b=line[1]
        op=line[2]
        res=FPU(fh(a),fh(b),op)
        if op:
            c=a+b
            print(a," (+) ",b," = ",c)
        else:
            c=a-b
            print(a," (-) ",b," = ",c)
        flt=hf(hex(int(res,2))[2:])
        print(flt)
        pnp=int(hex(int(res,2))[2:],16) - int(fh(c),16) <=100
        print(bcolors.OKGREEN+"Pass" if pnp else bcolors.FAIL+"Fail")
        print("expected \t",bin(int(fh(c), 16))[2:].zfill(32))
        print("got      \t",res)
        print(bcolors.ENDC)

FA=fatTest(10000)
testFA(FA,2)

# for failure in FA
    #fh(2.3324536)
# a = "45fe99e5" #8147.236864
# b = "460d87ad" #9057.919371
# answer = "46866a50"
# c=FPU(a,b)
#
# print(bcolors.FAIL,"case (+) + (+)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
#
#
# a = "449ebbc8" #1269.868163
# b = "c60eb709" #-9133.758561
# answer = "c5f5bf20"
# c=FPU(a,b)
# print(bcolors.FAIL,"case (+) + (-)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
#
# a = "c5c59cbd" #-6323.592462
# b = "4473d9dc" #975.404050
# answer = "c5a72182"
# c=FPU(a,b)
# print(bcolors.FAIL,"case (-) + (+)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
#
# a = "c52e0fb7" #-2784.982189
# b = "c5aae686" #-5468.8154
# answer = "c600f731"
# c=FPU(a,b)
# print(bcolors.FAIL,"case (-) + (-)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
#
# a = "46159c46" #9575.068354
# b = "4616c38b" #9648.885352
# answer = "c293a280"
# c=FPU(a,b,False)
# print(bcolors.FAIL,"case (+) - (+)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
#
# a = "44c50430" #1576.130817
# b = "c617a7b6" #-9705.927818
# answer = "4630483c"
# c=FPU(a,b,False)
# print(bcolors.FAIL,"case (+) - (-)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
#
# a = "c6158eae" #-9571.669482
# b = "4597ae0d" #4853.756487
# answer = "c66165b5"
# c=FPU(a,b,False)
# print(bcolors.FAIL,"case (-) - (+)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
#
# a = "c5fa1670" #-8002.804689
# b = "c4b15ba1" #-1418.863386
# answer = "c5cdbf88"
# c=FPU(a,b,False)
# print(bcolors.FAIL,"case (-) - (-)")
# print(bin(int(answer, 16))[2:].zfill(32)==c,bcolors.ENDC)
# print("expected \t",bin(int(answer, 16))[2:].zfill(32))
# print("got      \t",c)
