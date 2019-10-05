$(window).on('load',function(){
    $('#messageModal').modal('show');
});

function clearFields(){
  $('#id_shares_amount').attr({'placeholder': 1})
  $('#id_shares_amount').val('1')
  $('#id_shares_amount').end()
  $("#total").val('$0.00')
}

clearFields();



$('#exampleModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal

  //Get stock info from buy button
  var name = button.data('whatever').name
  price = button.data('whatever').price
  var ticker = button.data('whatever').ticker

  //calculate stock available
  var max = button.data('whatever').max
  var sold = button.data('whatever').sold
  var available = max - sold

  $('#id_shares_amount').attr({'max': available})

  // Update the modal's content
  var modal = $(this)

  //Pass stock information to modal
  modal.find('.form-group #stock_name').text(name)
  modal.find('.form-group #stock_price').text('$'+price)
  modal.find('#stock_ticker').val(ticker)
  modal.find('.form-group #shares_available').text(max)
  updateTotal()
})

$('#exampleModal').on('hide.bs.modal', function (event) {
  clearFields()
})
