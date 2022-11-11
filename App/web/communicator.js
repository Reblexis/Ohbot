recording = false

function record()
{
    if(!recording)
        document.getElementById("record_stop_button").src = "media/images/stop_recording.png";
    else
        document.getElementById("record_stop_button").src = "media/images/record.png";
    recording = !recording
    eel.record(recording);
}

eel.expose(test_access)
function test_access()
{
    eel.python_log("Accessible!");
}