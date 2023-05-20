recording = false


eel.expose(test_access)
function test_access()
{
    eel.python_log("Accessible!");
}

eel.expose(show_error)
function show_error(error_message)
{
    let error_text = document.getElementById("error_message")
    error_text.innerHTML = error_message
}

eel.expose(switch_to_console)
function switch_to_console()
{
    document.location.href = "main.html"
}