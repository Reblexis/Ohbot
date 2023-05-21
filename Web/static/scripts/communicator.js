
function test_access()
{

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