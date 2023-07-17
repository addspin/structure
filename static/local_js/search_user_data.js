$(document).ready(function(){
    $("#search_user").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#search_user_data label").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });