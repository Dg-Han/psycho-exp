function BART_hotkey(event){
    if (event.keyCode==32){
            pump()
        }
        else if (event.keyCode==13){
            SBPS()
        }
}

function SBPS_hotkey(event){
    if (event.keyCode==13){
        BART()
    }
}