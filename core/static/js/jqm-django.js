
$("#submitButton").click(function() {
    if ($("#textarea").val() == "correct") {
        alert("Validated...");
        return true;
    }

    alert("Not Valid");
    return false;
});
