function show(eId, ...args){
    c=document.getElementById(eId);
    c.style.display="inline";
    for (var j=0, len=(args).length; j<len; j++){
        c=document.getElementById(args[j]);
        c.style.display="inline";
    }
}

function hide(eId, ...args){
    c=document.getElementById(eId);
    c.style.display="none";
    for (var j=0, len=(args).length; j<len; j++){
        c=document.getElementById(args[j]);
        c.style.display="none";
    }
}

function draw_balloon(r){
    var c=document.getElementById("balloon");
    var b=c.getContext("2d");
    b.fillStyle="#FF0000";
    b.beginPath();
    b.arc(c.width/2,c.height/2,5+2*r,0,2*Math.PI,true);
    b.closePath();
    b.fill();
}

function show_earn(){
    p=document.getElementById("total");
    p.innerText="总收益:\n"+(total/100).toString();
    p=document.getElementById("trial");
    p.innerText="本轮收益:\n"+(trial/100).toString();
}