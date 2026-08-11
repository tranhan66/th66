<?php //2025oc20mo tnhan@enersev  SisGwNG_diag2025oc22we.php
function d2s(){date_default_timezone_set("Asia/Ho_Chi_Minh");return date("Ymd");}
function t2s(){date_default_timezone_set("Asia/Ho_Chi_Minh");return date("His");}
$n=sizeof($argv);   if($n<3){echo "USAGE: php SisGwNG_diag2025oc20.php PortNumber MbRtuSlaveId,Addr\n";return;}$sleepSec=10/($n-2); #1>10seconds-2025nov3mo
$url="http://10.10.10.108/cgi-bin/Diagnostique";	
$b=['Refresh'=>'Refresh','NoPort'=>'1','NoEqt'=>'1'];$b['NoPort']=(string)$argv[1];var_dump($b);
while(true){$hd="hhmmss,id,Slav,noAns,crc,AnswEC,LastEC,LastRqSiz,LastRsSiz,noErr,status\n";$s1=$hd;
    for($i=2;$i<$n;$i++){$idAddr=explode(",",$argv[$i]);$b['NoEqt']=$idAddr[0];//$i-1;//$argv[$i];//echo $argv[$i]."\n";
        $ops=['http'=>['header'=>"Content-type: application/x-www-form-urlencoded\r\n",'method'=>'POST','content'=>http_build_query($b),],];
        $cxt=stream_context_create($ops);$res=file_get_contents($url,false,$cxt);if($res===false){echo d2s().t2s()."err\n";continue;}//var_dump($res);  
        $k="without answer = </TD>"; $p=strpos($res,$k);  $s=substr($res,$p+strlen($k),800);$a=explode(" ",$s);//print_r($a); 
        $fn="SisGwNG_port".$argv[1]."_".d2s().".txt";   if(file_exists($fn)===false)file_put_contents($fn,$hd,FILE_APPEND);//|LOCK_EX);
        $ss=t2s().",".$idAddr[0].",".$idAddr[1].",".$a[3].",".$a[16].",".$a[29].",".$a[40].",".$a[53].",".$a[66].",".$a[78];
        if(str_contains($res,"CORRECT"))$ss.=",CORRECT";//2025no27thu
        else{$ss.=",FAIL";file_put_contents($fn,$ss."\n",FILE_APPEND);}   $ss.="\n"; //|LOCK_EX);//echo $ss;
        $s1.=d2s();$s1.=$ss;sleep($sleepSec);}
    file_put_contents("SisGwNG_port".$argv[1].".txt",$s1,0);}  ?>
