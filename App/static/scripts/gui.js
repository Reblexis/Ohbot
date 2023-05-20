eel.expose(showCameraFeed);
function showCameraFeed(val)
{
    let elem = document.getElementById('bg');
    elem.src = "data:image/jpeg;base64," + val
}

eel.expose(hideCameraFeed);
function hideCameraFeed()
{
    let elem = document.getElementById('bg');
    elem.src = ""
}