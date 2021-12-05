$(document).ready(function() {
    $(".checkSerial").on('click', function() {
        var serial = $('#snumber1').val();
        $.ajax({
            url: "/checkSerial",
            type: "POST",
            data: { serial: serial },
            success: function(data) {
                $(specs).replaceWith(data)
            }
        });
    });
});

$(document).ready(function() {
    $(".updateRow").on('click', function() {
        var currentRow = $(this).closest("tr");
        var id = currentRow.find("td:eq(0)").text();
        var status = currentRow.find("td:eq(5)").find("option:selected").text();
        var pr = currentRow.find("td:eq(6)").find("input").val();
        var po = currentRow.find("td:eq(7)").find("input").val();
        var requestDate = currentRow.find("td:eq(8)").find("input").val();
        var receiveDate = currentRow.find("td:eq(9)").find("input").val();
        console.log(id);
        $.ajax({
            url: "/reqUpdate",
            type: "POST",
            data: { id: id, status: status, pr: pr, po: po, requestDate: requestDate, receiveDate: receiveDate }
        });
    });
});