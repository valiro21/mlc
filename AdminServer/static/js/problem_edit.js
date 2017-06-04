
deleteDataset = function (datasetId) {
    $.ajax({
       url: '/dataset/delete',
       type: 'post',
       data: {
           datasetId: datasetId
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
               $('#dataset-row-' + datasetId).remove();
           }
           else{
               $('#error-message').html(result);
               $('#success-container').addClass('hidden');
               $('#error-container').removeClass('hidden');
           }
       }
    });
};

loadEditModal = function (datasetId) {
    $('#dataset-id').text(datasetId);
    $('#edit-dataset-modal').modal();
};
