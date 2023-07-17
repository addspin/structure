$(document).ready(function(){
    $("#service_name_search").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#service_search label").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });