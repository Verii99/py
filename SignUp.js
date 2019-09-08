$(function() {
    $('#btnReg').click(function() {

        $.ajax({
            url: '/Reg',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});