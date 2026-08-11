import serial;import sys;import math;import os;from datetime import datetime,timedelta;import time;import random #2025se8mo-tnhan@enersev from datetime import timedelta;
def crc16mb2(r:bytearray,n):
    t=[0x0000,0xA001];c=0xFFFF;#i=0;print(str(i)+"Cn"+str(n)+" BAn"+str(len(r)))
    for i in range(n):
        c^=r[i]
        for _ in range(8):
            x=c&1;c>>=1;c^=t[x]
    return c.to_bytes(2,byteorder='little')
def crc16ok(r:bytearray,n):
    c=crc16mb2(r,n)
    if r[n]==c[0] and r[n+1]==c[1]:return 1
    else:return 0
def mbResLen(fc,dn):
    match fc:
        case 1|2:return math.ceil(dn/8)  #+5
        case 3|4:return 2*dn    
        case _:return 0
ssMbLog="";sFnLog=""
#def mbLog():global ssMbLog,sFnLog;      #time.sleep(0.001);return 0
#    if sFnLog=="" or ssMbLog=="":return 0 #time.sleep(0.0005);
#    with open(sFnLog,"a") as f:f.write(ssMbLog+"\n") #if 0<(r%10)
#    ssMbLog="";return 1     #print(ssMbLog);
def mbSlaveResCrc(id,r): #2025se29mo
    n=len(sys.argv);ts=int(time.time())
    for i in range(n-2):
        aa=sys.argv[i+2].split(',');an=len(aa)
        if an<2:continue     
        if int(aa[0])==id:
            j=aa[1].find("ms")
            if 0<j and (r%10==4 or r%10==9):return int(aa[1][0:j]) #2025de26fri
            if r%5==1 or r%5==4: #crc r%10==2  2026apri29we 2026jun2tu
                if aa[1]=='c' or aa[1]=='cn' or  aa[1]=='nc':return 1 
            if r%5==3 or r%5==2: #noA r%10==7
                if aa[1]=='n' or aa[1]=='cn' or  aa[1]=='nc':return 2
    return 0    
def mbRqFind(rq,n):
    i=0;r=[1,2]
    if n<9:return r
    while True:
        n-=1;i+=1
        if n<8:return r
        r=rq[i:];c=crc16mb2(r,n-2)    
        if r[n-2]==c[0] and r[n-1]==c[1]:return r
def mbRRx14w3(p,rq:bytearray,n,c1,td,r): #2025no19we
    rs=bytearray(13);rs[0]=rq[0];rs[1]=rq[1]
    rs[2]=8;rs[3]=7; rs[4]=6
    rs[5]=0;rs[6]=1; rs[7]=0;rs[8]=0; rs[9]=0;rs[10]=0
    c=crc16mb2(rs,11);rs[11]=c[0];rs[12]=c[1];return rs
def mbRRx14w11(p,rq:bytearray,n,c1,td,r): #2025no120thu
    rs=bytearray(29);rs[0]=rq[0];rs[1]=rq[1]
    rs[2]=24;rs[3]=13;rs[4]=6 		#RefType
    rs[5]=0; rs[6]=98;rs[7]=0;		#ChanNum=x0062=98
    rs[8]=1;rs[9]=0;rs[10]=r%2  	#EvtType=1 EvtNum=x0000/1
    if 49<rq[0]:rs[10]+=12          #EvtNum=12,13
    rs[11]=rs[12]=rs[13]=0;rs[14]=1	#msRef542pON>>Evt
    rs[15]=rs[16]=rs[17]=rs[18]=0	#optPM   #cp56time=7bytes
    rs[19]=0x19;rs[20]=6;rs[21]=0x12;rs[22]=0xb;rs[23]=0x10;rs[24]=0xa0;rs[25]=0x28;rs[26]=0
    c=crc16mb2(rs,27);rs[27]=c[0];rs[28]=c[1];return rs
def mbRs(p,rq,n,c1,td,r): 
    global ssMbLog,sFnLog;d=0;rs=rq #2025nov25tu@e77  # if rq[0]==80:return 0 #2025no25tu-DEif
    if rq[1]==5 or rq[1]==6 or rq[1]==20 or rq[1]==21:rs=rq #2025no20th
    elif rq[1]==16: #2025no25tu@e77
        rs=bytearray(8);rs[0]=rq[0];rs[1]=rq[1];rs[2]=rq[2];rs[3]=rq[3];rs[4]=rq[4];rs[5]=rq[5]
        c=crc16mb2(rs,6);rs[6]=c[0];rs[7]=c[1]
    else: #2025no24mo
        dn=rq[4]*256+rq[5];dn2=mbResLen(rq[1],dn);rs=bytearray(dn2+5);rs[0]=rq[0]
        if dn2<1:rs[1]=0x95; rs[2]=1    #FcNotSupported
        else:    rs[1]=rq[1];rs[2]=dn2&0xff #2025se29mo-tnhan@ens
        for i in range(dn2):
            if r%2==0:rs[i+3]=0     #i+1
            else:     rs[i+3]=0     #xff #2025no25tu =0-sepam-timestamp
        d=mbSlaveResCrc(rs[0],r)
        if d<9:c=crc16mb2(rs,dn2+3);rs[dn2+3]=c[0];rs[dn2+4]=c[1]+d #2025se29mo
    if rq[1]==20 and rq[9]==3: rs=mbRRx14w3(p,rq,n,c1,td,r)  #2025no19we
    if rq[1]==20 and rq[9]==11:rs=mbRRx14w11(p,rq,n,c1,td,r) #2025no20th
    dt=datetime.now();ts=dt.strftime("%H%M%S.%f")
    sli=1.0 #2025de3we +dt.minute%5 #0.003+random.random()/50 #26=1.75>40ms  110=1.75>10ms if r%10==5:sli+=0.01 #2025oc16thu-ThLinhENS
    if 9<d:sli=d #2025de26fri
    if d!=2:time.sleep(sli/1000.0);p.write(rs);time.sleep(0.001);p.flush();#time.sleep(0.001) #time.sleep(0.0001);2025no25tu-2025se26fri sli*=1000;dt=datetime.now();ts=dt.strftime("%H%M%S.%f")
    sli+=1;ssMbLog=ts+","+rq.hex()+","+str(c1)+","+str(td)+","+str(r)+f",{sli:.1f}ms" #ts+","+ if d==1:ssMbLog+=",crc+1"    if d==2:ssMbLog+=",noAnswer"
    if d==1:ssMbLog+=",crc+1" 
    if d==2:ssMbLog+=",noAnswer"
    with open(sFnLog,"a") as f:f.write(ssMbLog+"\n")
    return 1
def mbRss(p,rq,n,c1,td,r):
    nn=len(rq);i0=0;i1=8;rr=0
    while True:
        if nn<i1:return rr
        r1=rq[i0:i1];c=crc16mb2(r1,i1-i0-2)
        if rq[i1-2]==c[0] and rq[i1-1]==c[1]:
            if 0<rr:mbRs(p,r1,n,c1,td,r) #2025nov10mo
            i0=i1;i1+=8;rr+=1;time.sleep(0.01) #10ms-2025oc29we 
        else:i1+=1;continue
def mbRes(p,rq:bytearray,n,c1,td,r):
    global ssMbLog,sFnLog,sport;d=0;dt=datetime.now();ts=dt.strftime("%H%M%S.%f");sFnLog=dt.strftime("%Y%m%d-%H")+"mbRtuSlav_"+sport+".txt"
    if rq[0]==0:
        with open(sFnLog,"a") as f:f.write(ts+","+rq.hex()+","+str(c1)+","+str(td)+","+str(r)+",BroadcastMsg\n")
        if 8<n:return mbRs(p,rq[1:],n-1,c1,td,r) #2025nov5we
        return 0 #2025se22mo@e77
    c=crc16mb2(rq,n-2)
    if rq[n-2]!=c[0] or rq[n-1]!=c[1]:
        with open(sFnLog,"a") as f:f.write(ts+","+rq.hex()+","+str(c1)+","+str(td)+","+str(r)+",CRCer="+c.hex()+"\n")
        return mbRss(p,rq,n,c1,td,r)    #0 #2025oc7mo   r1=mbRqFind(rq,n);if len(r1)<8:return 0;else:rq=r1
    return mbRs(p,rq,n,c1,td,r) #2025oc14tu
    if rq[1]==20 or rq[1]==21:rs=rq
    else:
        dn=rq[5];dn2=mbResLen(rq[1],dn);rs=bytearray(dn2+5);rs[0]=rq[0]
        if dn2<1:rs[1]=0x95; rs[2]=1    #FcNotSupported
        else:    rs[1]=rq[1];rs[2]=dn2&0xff #2025se29mo-tnhan@ens
        for i in range(dn2):
            if r%2==0:rs[i+3]=0 #i+1
            else:     rs[i+3]=0xff
        d=mbSlaveResCrc(rs[0],r)    
        c=crc16mb2(rs,dn2+3);rs[dn2+3]=c[0];rs[dn2+4]=c[1]+d #2025se29mo
    if d!=2:time.sleep(0.002);p.write(rs);p.flush();time.sleep(0.0005) #2025se26fri
    ssMbLog=ts+","+rq.hex()+","+str(c1)+","+str(td)+","+str(r)
    if d==1:ssMbLog+=",crc+1" 
    if d==2:ssMbLog+=",noAnswer"
    with open(sFnLog,"a") as f:f.write(ssMbLog+"\n")
    return 1    #+","+rs.hex()+",r"+str(r);print(ss);#with open(fn,"a") as f:f.write(ss+"\n") #if 0<(r%10): 
def mbRs2(p,rq:bytearray,n,c1,td,r):
    if n%8!=0 or rq[0]==0:return mbRes(p,rq,n,c1,td,r)	
    c=n//8
    if c<2:return mbRes(p,rq,n,c1,td,r) # ==1  2025oc1we 
    if sFnLog!="": 
        dt=datetime.now();ts=dt.strftime("%H%M%S.%f")
        with open(sFnLog,"a") as f:f.write(ts+","+rq.hex()+","+str(c1)+","+str(td)+","+str(r)+",2reqs\n")
    for j in range(c):
        i=j*8;mbRes(p,rq[i:i+8],8,c1,td,r)
    return c
def mbReq(p,r):
    n0=0;t0=datetime.now();td=0;c1=0
    while True:#sleep(0.05) 0.001 0.0005
        time.sleep(0.0005);n=p.inWaiting()
        if n==0:n0=0;c1=0;continue #mbLog();
        if n0<n:n0=n;c1=0;continue 
        if n0==n:c1+=1  
        if c1==1:t0=datetime.now();continue 
        td=(datetime.now()-t0).microseconds
        if td<700 or n<8:continue #c1<24  2025oc8we td<1000
        rq=p.read(n);return mbRes(p,rq,n,c1,td,r)   #mbRs2=2025oc7mo  2025se22mo@e77 if 20<n:p.reset_input_buffer();n0=n;c1=0;time.sleep(0.0002);continue
def mbRq1(p,r): #2025oc10fri
    global sport;n0=0;t0=datetime.now();td=0;c1=0
    while True:#sleep(0.05) 0.001 0.0005
        if 2<len(sys.argv) and "noise" in sys.argv[2] and t0.second%30==0:
            ns=234;nois=bytearray(ns)
            for i in range(ns):nois[i]=i+1 #bytearray([1,2,3,4,5,6,7,8,9,0])
            p.write(nois);p.flush() #2025nov21fri
        time.sleep(0.001);n=p.in_waiting;time.sleep(0.001);  #2025nov13thu inWaiting() #2025nov10mo sleep0.5>>1ms
        if n<0: #p.reset_input_buffer();
            fn="SPinw0_"+sport+".txt";er=t0.strftime("%Y%m%d%_H%M%S.%f")+","+str(n)
            with open(fn,"a") as f:f.write(er+"\n")
        if n<1:n0=0;c1=0;t0=datetime.now();continue #2025nov10mo n==0 >> n<1
        if n0<n:n0=n;c1=0;continue 
        if n0==n:c1+=1
        if 0<c1:    #2025no18tu=0 2025nov4tu-1-3-5
            if r<2 or 7<n:rq=p.read(n);td=(datetime.now()-t0).microseconds;return mbRes(p,rq,n,c1,td,r)   
rr=1;sport=sys.argv[1];cmd="stty -F /dev/"+sport+" 19200 cs8 -parenb -cstopb raw"; #baud=int(sys.argv[2]) a=sys.argv[3]
try:
    ec=os.system(cmd)
    sp=serial.Serial("/dev/"+sport,19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0) 
    ec=os.system(cmd);print(cmd+"\t ec"+str(ec)+" sp="+str(sp)+"\n");print(sp.get_settings()) #sp.reset_input_buffer();
    while True:#if a=="write":d2w=bytes([int(x) for x in sys.argv[4:]])sp.write(da2w);elif a=="read":
        if(0<mbRq1(sp,rr)):rr+=1                     #sp.read(8);      #print(d.hex());#' '.join([str(b) for b in d]))#rUpto8bytes
        #if d!=0:rr+=1;mbRes(sp,d,rr);   #c=crc16mb2(d,6);    print(d.hex()+" "+c.hex());  #if(d[6]==c[0] and d[7]==c[1]):i+=1;sp.write(mbRes(d))
except serial.SerialException as e:	print(f"ERRopeningSP:{e}")
except KeyboardInterrupt:print("CtlC")
finally:cmd="stty -F /dev/"+sport+" -raw";ec=os.system(cmd);print(cmd+"\t ec"+str(ec)+" close\n");sp.close();
