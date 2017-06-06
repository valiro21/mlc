$('document').ready(function(){
    /* validation */
    $("#add-problem").submit(submitForm);

    /* form submit */
    function submitForm(){
        var data = $("#add-problem").serialize();
        var contestName = $('#contest-name').val();
        $.ajax({
            type : 'POST',
            url  : '/contest/' + contestName + '/add_problem',
            data : data,
            success :  function(data) {
                var item = $('#error');
                item.text(data);
                item.addClass('alert-success');
                item.removeClass('alert-danger');
            },
            error : function (xhr, status, error) {
                var item = $('#error');
                item.text(xhr.responseText);
                item.addClass('alert-danger');
                item.removeClass('alert-success');
            }
        });
        return false;
    }
});

removeProblemFromContest = function (problemId) {
    var contestName = $('#contest-name').val();
    $.ajax({
        url: '/contest/' + contestName + '/remove_problem',
        type: 'post',
        data: {
            id: problemId
        },
        error : function (xhr, status, error) {
            var item = $('#error');
            item.text(xhr.responseText);
            item.addClass('alert-danger');
            item.removeClass('alert-success');
        },
        success: function (result, statusText, xhr) {
            var item = $('#error');
            item.text(xhr.responseText);
            item.addClass('alert-success');
            item.removeClass('alert-danger');

            $('#problem-row-' + problemId).remove();
        }
    });
};


