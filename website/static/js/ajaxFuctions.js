function checkSerial() {
    var serial = $('#snumber1').val();
    $.ajax({
        url: "/checkSerial",
        type: "POST",
        data: serial,
        success: function(data) {
            $(specs).replaceWith(data)
        }
    });
}

$(document).ready(function() {
    $(".updateRow").on('click', function() {
        var currentRow = $(this).closest("tr");
        var status = currentRow.find("td:eq(4)").find("option:selected").text();
        var pr = currentRow.find("td:eq(5)").find("input").val();
        var po = currentRow.find("td:eq(6)").find("input").val();
        var requestDate = currentRow.find("td:eq(7)").find("input").val();
        var receiveDate = currentRow.find("td:eq(8)").find("input").val();
        $.ajax({
            url: "/reqUpdate",
            type: "POST",
            data: { status: status, pr: pr, po: po, requestDate: requestDate, receiveDate: receiveDate }
        });
    });
});