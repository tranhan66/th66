#2025oc17fri tnhan@enersev
import serial;import sys;import math;import os;from datetime import datetime,timedelta;import time;import json;import requests
def mbSlaveAd2id(a):
    if a<20:return a-9      # 1,10  2,11  3,12  4,13  5,14  6,15
    if a<30:return a-13     # 7,20  8,21  9,22 10,23 11,24 12,25  
    if a<40:return a-17     #13,30 14,31 15,32 16,33 17,34 18,35
    if a<50:return a-21     #19,40 20,41 21,42 22,43 23,44 24,45
    if a<60:return a-25     #25,50 26,51 27,52 28,53
    if a<70:return a-31     #29,60
    if a<80:return a-40     #30,70 31,71
    if a<90:return a-48     #32,80 33,81
def sisgwngStatus(sla):
    pd={"Refresh":"Refresh","NoPort":"1","NoEqt":"1"};url="http://10.10.10.109/cgi-bin/Diagnostique"#;hdrs={"Content-type":"application/x-www-form-urlencoded"} #\r\n
    pd["NoPort"]=int(sys.argv[2]);pd["NoEqt"]=mbSlaveAd2id(sla);#print(json.dumps(pd)) 
    try:
        res=requests.post(url,data=pd) #,headers=hdrs)
        if res.status_code==200:#print(f"{res.text}")#print(f"StatusCode:{res.status_code}")print(f"ResHeaders:{res.request.headers}") #2seeSentHdrs
            rt=res.text;i=rt.find("without answer = </TD>");ss=rt[i+22:i+830];ns=ss.split(' ')
            rs="MBslave"+str(pd["NoEqt"])+","+str(sla)+","+ns[3]+","+ns[16]+","+ns[78] #print(f"{ns[3]},{ns[16]},{ns[78]}\n")
            if "FAIL" in rt:rs+=",FAIL" 
            else:rs+=",CORRECT"
            return rs #+"\n")
        else:return "SisGwNGerr" #print(f"StatusCode:{res.status_code}") 
    except requests.exceptions.RequestException as e:return "SisGwNGerr" #print(f"ERR:{e}")
def spCheck(p,sport): 
    n0=0;td=0;c1=0;c2=0;r=0;t0=datetime.now() #2025oc23thu
    while True:
        time.sleep(0.001);n=p.inWaiting();time.sleep(0.001) #2025nov13thu
        if n<1:n0=0;c1=0;c2=0;continue  #t0=datetime.now();mbLog();
        if n0<n:n0=n;c1=0;continue
        if n0==n:c1+=1 
        if 2<c1:    #2>4>-2025no25 3<c1 2025oc28tu if n<8:c2+=1;continue
            r+=1;dt=datetime.now();ts=dt.strftime("%H%M%S.%f");fn=dt.strftime("%Y%m%d-%H")+"-SPmoni-"+sport+".txt"
            rq=p.read(n);t1=datetime.now();td=(t1-t0).microseconds;t0=t1 #2025oc23thu
            if os.path.exists(fn)==False:
                with open(fn,"a") as f:f.write("hhmmss,us,frame,sz,c1,c2,r,Eqt,Sla,noAns,crc,fail\n")    
            sla=rq[0]    
            with open(fn,"a") as f:f.write(ts+","+str(td)+","+rq.hex()+","+str(n)+","+str(c1)+","+str(c2)+","+str(r)+"\n") #+","+sisgwngStatus(sla)
            n0=0;c1=0;c2=0;continue
sport=sys.argv[1];c="stty -F /dev/"+sport+" 19200 cs8 -parenb -cstopb raw"; #c="MODE "+sport+": 19200,n,8,1";# baud=int(sys.argv[2]) a=sys.argv[3]
try:
    ec=os.system(c);print(c+"\t ec"+str(ec))
    sp=serial.Serial("/dev/"+sport,19200,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=0)
    #if hasattr(sp,'set_low_latency_mode'):sp.set_low_latency_mode(True);print("setLowLatencyModeTrue\n") #2025de9tu@e77 sp.set_buffer_size(rx_size=256,tx_size=256) #2025de5fri 
    print("sp="+str(sp)+"\n");  #tty.setraw(sp.fileno());
    print(sp.get_settings());   spCheck(sp,sport)
except serial.SerialException as e:     print(f"ERRopeningSP:{e}")
except KeyboardInterrupt:print("CtlC")
finally:sp.close() #cmd="stty -F /dev/"+sport+" -raw";ec=os.system(cmd);print(cmd+"\t ec"+str(ec)+" close\n");ty
