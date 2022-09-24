/* this js file relys on jquery and underscore*/
'use strict';

var i=0;
var data={
    pid:undefined,
    mode:new Array(72),
    keydown:new Array(72),
    rt:new Array(72),
    st:undefined,
    et:undefined,
    }
var st, et, settings;
var prcss="exe";
var exe_set={"0":{text:"绿", color:"#FF0000", type:"conflict", correct:68},
             "1":{text:"蓝", color:"#00FF00", type:"conflict", correct:70},
             "2":{text:"黄", color:"#0000FF", type:"conflict", correct:74},
             "3":{text:"红", color:"#FFFF00", type:"conflict", correct:75},
             "4":{text:"天", color:"#FFFF00", type:"unrel", correct:75},
             "5":{text:"伟", color:"#0000FF", type:"unrel", correct:74},
             "6":{text:"北", color:"#00FF00", type:"unrel", correct:70},
             "7":{text:"良", color:"#FF0000", type:"unrel", correct:68}};
data.st=new Date().getTime();

$.ajax({
    type:"GET",
    url:"https://dg-han.github.io/psycho-exp/stroop/data/settings.json",
    dataType:"json",
    success:function(data){
        settings=data;
    },
});

var arr=_.range(72);
var tr_arr=arr.sort(function(){return Math.random()-0.5});
var earr=_.range(8);
var etr_arr=earr.sort(function(){return Math.random()-0.5});
window.addEventListener("keydown",welcome_hotkey);

function preStroop(){
    if (i==0){
        $("#welcome").hide();
        window.removeEventListener("keydown",welcome_hotkey);
        window.removeEventListener("keydown",exercise_hotkey);
    }
    else if ((i>=8)&&(prcss=="exe")){
        exe_end();
        return
    }
    else if ((i>=72)&&(prcss=="frm")){
        end();
        return
    }
    set_focus();
    $("#prepare").show();
    setTimeout(Stroop,800);
}

function Stroop(){
    $("#prepare").hide();
    if (prcss=="frm"){
        data.mode[i]=settings[tr_arr[i]];
        set_stroop(tr_arr[i]);
    }
    else{
        set_stroop(etr_arr[i],"exe");
    }
    window.addEventListener("keydown",Stroop_hotkey);
    $("#trial").show();
    st=new Date().getTime();
}

function exe_end(){
    $("#trial").hide();
    $("#title").hide();
    $("#instruct").html(`练习结束！如果熟悉实验流程，按空格键进入正式实验；<br>
    如果还需熟悉反应按键，可按“R”键继续练习。<br>
    正确反应：<br>
    如果字的颜色是“红色”，请按下“D”键；<br>
    如果字的颜色是“绿色”，请按下“F”键；<br>
    如果字的颜色是“蓝色”，请按下“J”键；<br>
    如果字的颜色是“黄色”，请按下“K”键；<br>`);
    i=0;
    $("#welcome").show();
    window.addEventListener("keydown",exercise_hotkey);
}

function end(){
    data.et=new Date().getTime();
    $("#trial").hide();
    $("#end").show();
    var result=JSON.stringify(data);
    var blob=new Blob([result], {type: "text/plain; charset=utf-8"});
    saveAs(blob, "result.json");
    var cache=calc();
    var message=`本次实验中，您色词无关组的平均反应时为 ${cache.unrel_t} ms, 正确率为 ${cache.unrel_crt} %<br>色词干扰组的平均反应时为 ${cache.conflict_t} ms, 正确率为 ${cache.conflict_crt} %<br>下面是Stroop效应的简单解释:<br>Stroop（颜色）效应是在报告呈现文字颜色的任务中，当字义与颜色相矛盾时，相较于字义与颜色无关时需要的时间更长。<br>即说明字义对于判断颜色的任务产生了干扰，说明字义可能是在判断颜色之前自动加工的。`;
    $("#explain").html(message);
    $("#end").show();
}

function calc(){
    let unrel_t=0; let conflict_t=0; let unrel_crt=0; let conflict_crt=0;
    for (let i=0; i<72; i++){
        if (data.mode[i]["type"]=="unrel"){
            unrel_t+=data.rt[i];
            if (data.mode[i].correct==data.keydown[i]){
                unrel_crt+=1
            }
        }
        else if (data.mode[i]["type"]=="conflict"){
            conflict_t+=data.rt[i];
            if (data.mode[i].correct==data.keydown[i]){
                conflict_crt+=1;
            }
        }
    }
    return {unrel_t:(unrel_t/36).toFixed(2),unrel_crt:(100*unrel_crt/36).toFixed(2),conflict_t:(conflict_t/36).toFixed(2),conflict_crt:(100*conflict_crt/36).toFixed(2)};
}