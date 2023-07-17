function select_service(service,service_name_value,service_url_value,service_text_value,service_owner_value) {


  number_service = document.getElementById("number_service").getAttribute("value")


  let div_insert_service = document.querySelector('.div_insert_service');

  let input1 = document.createElement("input")
  let input2 = document.createElement("input")
  let input3 = document.createElement("input")
  let input4 = document.createElement("input")
  
  
  var i = 0;
  var id = 0
  while (i < number_service) {
      var checkBox  = document.getElementById(service.id)
      if (checkBox.checked == true) {
        id = (Math.random())
       
        var service_name = document.getElementById(service_name_value.id).getAttribute("value")      
        input1.innerHTML = service_name;
        input1.id = service_name;
        input1.className = 'form-control um_margin_add_serv_dev'
        input1.setAttribute("name", 'service_name_'+id);
        input1.setAttribute("type", "text");
        input1.setAttribute("value", service_name);
        input1.setAttribute("readonly", true);
        div_insert_service.append(input1)

        id = (Math.random())
        var service_url = document.getElementById(service_url_value.id).getAttribute("value")      
        input2.innerHTML = service_url;
        input2.id = service_url;
        input2.className = 'form-control um_margin_add_serv_dev'
        input2.setAttribute("name", 'service_url_'+id);
        input2.setAttribute("type", "text");
        input2.setAttribute("value", service_url);
        input2.setAttribute("style","display: none;");
        div_insert_service.append(input2)
        
        id = (Math.random())
        var service_text = document.getElementById(service_text_value.id).getAttribute("value")      
        input3.innerHTML = service_text;
        input3.id = service_text;
        input3.className = 'form-control um_margin_add_serv_dev'
        input3.setAttribute("name", 'service_text_'+id);
        input3.setAttribute("type", "text");
        input3.setAttribute("value", service_text);
        input3.setAttribute("style","display: none;");
        div_insert_service.append(input3)

        id = (Math.random())
        var service_owner = document.getElementById(service_owner_value.id).getAttribute("value")      
        input4.innerHTML = service_owner;
        input4.id = service_owner;
        input4.className = 'form-control um_margin_add_serv_dev'
        input4.setAttribute("name", 'service_owner_'+id);
        input4.setAttribute("type", "text");
        input4.setAttribute("value", service_owner);
        input4.setAttribute("style","display: none;");
        div_insert_service.append(input4)


      } else {

          var service_name = document.getElementById(service_name_value.id).getAttribute("value")
          var service_url = document.getElementById(service_url_value.id).getAttribute("value")
          var service_text = document.getElementById(service_text_value.id).getAttribute("value")
          var service_owner = document.getElementById(service_owner_value.id).getAttribute("value")
          document.getElementById(service_name).remove();
          document.getElementById(service_url).remove();
          document.getElementById(service_text).remove();
          document.getElementById(service_owner).remove();
      }
      i++;
      id++;
  } 
     


}

