// Make search icon clickable
$(document).on("click", "svg.search-submit", function (e) {
  $('#search-form').submit()
})

// Toggle visibility of date filter form
$("#show-form").on("click", function (e) {
  $('#date-form').toggle()
})

// Preserve 'q' query string and set 'page' to 1 if 'page' is in url
$('#search-form').on('submit', function (e) {
  e.preventDefault();

  var url = new URL(window.location.href);
  if(url.searchParams.has('page')){
    url.searchParams.set("page", 1)
  }
  url.searchParams.set("q", $('input[type="search"]').val()); // setting your param
  var newUrl = url.href;
  window.location.href = newUrl;
})

// Preserve 'start_date' and 'end_date' query strings and set 'page' to 1 if 'page' is in url
$('#date-form').on('submit', function (e) {
  e.preventDefault();

  var url = new URL(window.location.href);
  if(url.searchParams.has('page')){
    url.searchParams.set("page", 1)
  }
  url.searchParams.set("start_date", $('input[name="start_date"]').val()); // setting your param
  url.searchParams.set("end_date", $('input[name="end_date"]').val());
  var newUrl = url.href;
  window.location.href = newUrl;

})

// Jquery datepicker function
$(function() {
  var from = $('input[name="start_date"]')
      .datepicker({
        dateFormat: "dd-mm-yy",
        changeMonth: true,
        changeYear: true,
        numberOfMonths: 2,
        autoclose: true
      })
      .on( "change", function() {
        to.datepicker( "option", "minDate", $(this).datepicker('getDate'));
      }),
    to = $('input[name="end_date"]').datepicker({
      dateFormat: "dd-mm-yy",
      changeMonth: true,
      changeYear: true,
      numberOfMonths: 2,
      autoclose: true
    })
    .on("change", function() {
      from.datepicker( "option", "maxDate", $(this).datepicker('getDate'));
    });
});

// Makes delete icon clickable
$(document).on("click", "svg.delete", function (e) {
  e.preventDefault();
  var taskUrl = $(this).attr('data-url');
  $.ajax({
    type: "POST",
    url: taskUrl,
    data: {
      csrfmiddlewaretoken: csrf_token,
      action: "post",
    },
    success: function (response) {
      updateTodoList()
    },
    error: function (response) {
    },
  });
});

function updateTodoList() {
  var url = window.location.href
  $.ajax({
    type: "GET",
    url: url,
    success: function (response) {
      $('.todo-list').empty()
      response = $($.parseHTML(response)).find('.todo-list').children()
      $('.todo-list').append(response)
    },
    error: function (response) {
      pageNumber = parseInt(url.split('page=')[1]) - 1
      window.location.replace("?page=" + pageNumber.toString());
    },
  });
}
