function checkSerial() {
    var serial = $('#snumber1').val();
    console.log(serial)
    $.ajax({
        url: "/checkSerial",
        type: "POST",
        data: serial,
        success: function(data) {
            $(specs).replaceWith(data)
        }
    });
}

function updateRow() {
    var
}