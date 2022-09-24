function welcome_hotkey(event){
    if (event.keyCode==32){
        preStroop()
        }
}

function exercise_hotkey(event){
    if (event.keyCode==32){
        prcss="frm";
    }
    else if (event.keyCode==82){
        tr_arr=arr.sort(function(){return Math.random()-0.5}); 
    }
    preStroop();
}

function Stroop_hotkey(event){
    if (event.keyCode==68||event.keyCode==70||event.keyCode==74||event.keyCode==75){
        et=new Date().getTime();
        if (prcss=="frm"){
            data.rt[i]=et-st;
            data.keydown[i]=event.keyCode;
        }
        $("#trial").hide();
        window.removeEventListener("keydown",Stroop_hotkey);
        i+=1;
        setTimeout(preStroop,800);
    }
}