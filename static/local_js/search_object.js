$(document).ready(function(){
    $("#search_data").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#remove_from_user label").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });