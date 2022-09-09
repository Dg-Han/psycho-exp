var total=0;
var trial=0;
var i=-1;
var data={
    bart:new Array(24),
    SBPS_S:new Array(24)
        }

function BART(){
    if (i>=0){
    data.SBPS_S[i]=$("input[type=radio][name=sbps_s]:checked").val()
    if (data.SBPS_S[i]==undefined){
        alert("请选择描述与你当前状态的符合程度");
        return
        }
    }
    i+=1;
    if (i==24){
        end();
        return
    }
    window.removeEventListener('keydown',SBPS_hotkey);
    var c=document.getElementById("balloon");
    cc=c.getContext("2d")
    cc.clearRect(0,0,c.width,c.height);
    draw_balloon(trial);
    hide("welcome");
    show_earn();
    show("bart");
    window.addEventListener('keydown', BART_hotkey);
    hide("sbps");
}

function pump(){
    trial+=1;
    if (trial>trial_set[i]){
        alert("由于充气过多，气球爆炸了！本轮收益清零。")
        trial=-1
        SBPS()
    }
    else{
        draw_balloon(trial);
    }
    show_earn();
    document.getElementById("pump").blur();
}

function SBPS(){
    window.removeEventListener('keydown', BART_hotkey);
    if (trial>0){
        total+=trial
    }
    data.bart[i]=trial;
    trial=0
    var s=document.getElementById("sbps_p");
    s.innerText=SBPS_Q[i];
    $("input[name=sbps_s]").removeAttr("checked");
    hide("bart");
    window.addEventListener('keydown', SBPS_hotkey);
    show("sbps");
}

function end(){
    hide("sbps");
    content=JSON.stringify(data);
    var blob=new Blob([content], {type: "text/plain; charset=utf-8"});
    saveAs(blob, "result.json");
    show("end");
}