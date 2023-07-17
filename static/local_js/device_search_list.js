$(document).ready(function(){
    $("#device_name_search").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#device_search label").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });