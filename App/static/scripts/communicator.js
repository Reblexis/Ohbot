eel.expose(test_access)
function test_access()
{
    eel.python_log("Accessible!");
}

function show_error(error_message)
{
    let error_text = document.getElementById("error_message")
    error_text.innerHTML = error_message
}

function switch_to_console()
{
    document.location.href = "main.html"
}