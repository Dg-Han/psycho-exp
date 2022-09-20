function welcome_hotkey(event){
    if (event.keyCode==32){
            preStroop()
        }
}

function Stroop_hotkey(event){
    if (event.keyCode==68||event.keyCode==70||event.keyCode==74||event.keyCode==75){
        et=new Date().getTime();
        data.rt[i]=et-st;
        data.keydown[i]=event.keyCode;
        $("#trial").hide();
        window.removeEventListener("keydown",Stroop_hotkey);
        i+=1;
        setTimeout(preStroop,800);
    }
}