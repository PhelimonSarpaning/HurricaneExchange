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



$('#sellSharesModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal

  //Get stock info from sell button
  var name = button.data('whatever').name
  price = button.data('whatever').price
  var ticker = button.data('whatever').ticker
  var max = button.data('whatever').max

  $('#id_shares_amount').attr({'max': max})

  // Update the modal's content
  var modal = $(this)

  //Pass stock information to modal
  modal.find('.form-group #stock_name').text(name)
  modal.find('.form-group #stock_price').text('$'+price)
  modal.find('#stock_ticker').val(ticker)
  modal.find('.form-group #shares_available').text(max)
})

$('#sellSharesModal').on('hide.bs.modal', function (event) {
  clearFields()
})
