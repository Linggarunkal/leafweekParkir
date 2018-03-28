function checkInput(obj) 
{
    var pola = "^";
    pola += "[0-9]*";
    pola += "$";
    rx = new RegExp(pola);

    if (!obj.value.match(rx))
    {
        if (obj.lastMatched)
        {
            obj.value = obj.lastMatched;
        }
        else
        {
            obj.value = "";
        }
    }
    else
    {
        obj.lastMatched = obj.value;
    }
}