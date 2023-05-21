function showCameraFeed(val)
{
    let elem = document.getElementById('bg');
    elem.src = "data:image/jpeg;base64," + val
}

function hideCameraFeed()
{
    let elem = document.getElementById('bg');
    elem.src = ""
}