function select_device(device,device_ident_value,device_inv_value,device_type_value,device_text_value) {


  number_device = document.getElementById("number_device").getAttribute("value")


  let div_insert_device = document.querySelector('.div_insert_device');
  // let div = document.createElement("div")
  let input1 = document.createElement("input")
  let input2 = document.createElement("input")
  let input3 = document.createElement("input")
  let input4 = document.createElement("input")
  
  var i = 0;
  while (i < number_device) {
      var checkBox  = document.getElementById(device.id)
      if (checkBox.checked == true) {
        id = (Math.random() * 100)
        var device_ident_value =  document.getElementById(device_ident_value.id).getAttribute("value")
        input1.innerHTML = device_ident_value;
        input1.id = device_ident_value;
        input1.className = 'form-control um_margin_add_serv_dev'
        input1.setAttribute("name", 'device_ident_'+id);
        input1.setAttribute("type", "text");
        input1.setAttribute("value", device_ident_value);
        input1.setAttribute("readonly", true);
        div_insert_device.append(input1)

        id = (Math.random() * 100)
        var device_inv_value =  document.getElementById(device_inv_value.id).getAttribute("value")
        input2.innerHTML = device_inv_value;
        input2.id = device_inv_value;
        input2.className = 'form-control um_margin_add_serv_dev'
        input2.setAttribute("name", 'device_inv_'+id+1);
        input2.setAttribute("type", "text");
        input2.setAttribute("value", device_inv_value);
        input2.setAttribute("style","display: none;");
        div_insert_device.append(input2)

        id = (Math.random() * 100)
        var device_type_value =  document.getElementById(device_type_value.id).getAttribute("value")
        input3.innerHTML = device_type_value;
        input3.id = device_type_value;
        input3.className = 'form-control um_margin_add_serv_dev'
        input3.setAttribute("name", 'device_type_'+id+1);
        input3.setAttribute("type", "text");
        input3.setAttribute("value", device_type_value);
        input3.setAttribute("style","display: none;");
        div_insert_device.append(input3)

        id = (Math.random() * 100)
        var device_text_value =  document.getElementById(device_text_value.id).getAttribute("value")
        input4.innerHTML = device_text_value;
        input4.id = device_text_value;
        input4.className = 'form-control um_margin_add_serv_dev'
        input4.setAttribute("name", 'device_text_'+id+1);
        input4.setAttribute("type", "text");
        input4.setAttribute("value", device_text_value);
        input4.setAttribute("style","display: none;");
        div_insert_device.append(input4)

      } else {

          var device_ident_value =  document.getElementById(device_ident_value.id).getAttribute("value")
          var device_inv_value =  document.getElementById(device_inv_value.id).getAttribute("value")
          var device_type_value =  document.getElementById(device_type_value.id).getAttribute("value")
          var device_text_value =  document.getElementById(device_text_value.id).getAttribute("value")
          document.getElementById(device_ident_value).remove();
          document.getElementById(device_inv_value).remove();
          document.getElementById(device_type_value).remove();
          document.getElementById(device_text_value).remove();
      }
      i++;
  } 
     


}

