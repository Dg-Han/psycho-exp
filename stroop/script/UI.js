/* this js file relys on jquery */

function set_stroop(trial){
    var p=$("#char").get(0);
    if (prcss=="frm"){
        p.innerText=settings[trial].text;
        p.style.color=settings[trial].color;
    }
    else if (prcss=="exe"){
        p.innerText=exe_set[trial].text;
        p.style.color=exe_set[trial].color;
    }
}

function set_focus(){
    var c=$("#focus").get(0);
    var cc=c.getContext("2d");
    cc.clearRect(0,0,c.width,c.height);
    cc.fillStyle="#000000";
    cc.fillRect(c.width/2-5, c.height/2-25, 10, 50);
    cc.fillRect(c.width/2-50, c.height/2-2.5, 100, 5);
}