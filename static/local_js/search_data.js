$(document).ready(function(){
    $("#search_data").on("keyup", function() {
      var value = $(this).val().toLowerCase();
      $("#accordionExample tr").filter(function() {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
      });
    });
  });