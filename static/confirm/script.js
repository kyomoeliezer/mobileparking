// Add your javascript here
$(function() {
  $('.form-confirm').submit(function(event) {
    event.preventDefault();
    var form = $(this)[0];

    $.confirm({
      columnClass: 'col-md-4',
      theme: 'white',
      title: '',
      content: 'do stuff',
      confirmButton: 'Ok',
      cancelButton: 'Cancel',
      confirmButtonClass: 'btn-success',
      cancelButtonClass: 'btn-danger',
      confirm: function() {
        //Submit the form
        form.submit();
        please_wait();
      },
      cancel: function() {
        //Do nothing
      }
    });
  });
});