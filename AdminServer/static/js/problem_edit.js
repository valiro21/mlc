
$('document').ready(function () {
   $('#new-dataset-form').validate({
      rules: {
          name: {
              required: true
          },
          'time-limit': {
              required: false,
              number: true,
              range: [0.00, 60.0]
          },
          'memory-limit': {
              required: false,
              number: true,
              range: [0.00, 1024.0]
          }
      },
      messages: {
          name: "A name is required for the dataset.",
          'time-limit': 'Must be a number between 0 and 60 (seconds)',
          'memory-limit': 'Must be a number between 0 and 1024 (MB)'
      }
   });
});

deleteItem = function (itemName, id) {
    if (confirm('Are you sure you want to delete this ' + itemName + '?') === false){
        return;
    }

    $.ajax({
        url: '/' + itemName + '/delete',
        type: 'post',
        data: {
            id: id
        },
        error: function () {
            $('#error-message').html('An error has occured.');

            $('#error-container').removeClass('hidden');
            $('#success-container').addClass('hidden');
        },
        success: function (result, statusText, xhr) {
            console.log('Received ' + xhr.status);

            if (xhr.status === 200){
                $('#success-message').html('Success!');
                $('#success-container').removeClass('hidden');
                $('#error-container').addClass('hidden');

                // delete the row in table
                $('#' + itemName + '-row-' + id).remove();
            }
            else{
                $('#error-message').html(result);
                $('#success-container').addClass('hidden');
                $('#error-container').removeClass('hidden');
            }
        }
    });
};
