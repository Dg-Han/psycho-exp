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
data.st=new Date().getTime();

$.ajax({
    type:"GET",
    url:"https://dg-han.github.io/psycho-exp/stroop/data/settings.json",
    dataType:"json",
    success:function(data){
        settings=JSON.parse(data);
    },
})

var arr=_.range(72);
var tr_arr=arr.sort(function(){return Math.random()-0.5});
window.addEventListener("keydown",welcome_hotkey);

function preStroop(){
    if (i==0){
        $("#welcome").hide();
        window.removeEventListener("keydown",welcome_hotkey);
    }
    else if (i>=72){
        end();
        return
    }
    set_focus();
    $("#prepare").show();
    setTimeout(Stroop,800);
}

function Stroop(){
    $("#prepare").hide();
    data.mode[i]=settings[tr_arr[i]];
    set_stroop(tr_arr[i]);
    window.addEventListener("keydown",Stroop_hotkey);
    $("#trial").show();
    st=new Date().getTime();
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