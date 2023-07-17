function device_change_data(device,device_remove_hide,device_type_value,device_inv_value,device_ident_value,device_text_value) {

    number_device = document.getElementById("number_device").getAttribute("value")
    
    var i = 0;
    while (i < number_device) {
        var checkBox  = document.getElementById(device.id)
        var del = document.getElementById("device_change_hide");
        if (checkBox.checked == true) {
            del.style.display = "block";

           // Показать кнопку удаление устройства
            document.getElementById(device_remove_hide.id).setAttribute("style","display: block;");
            // Получить и дабавить имя сервиса 
            var device_ident_value =  document.getElementById(device_ident_value.id).getAttribute("value")
            document.getElementById("device_ident_change").setAttribute("value",device_ident_value);
            // Получить и дабавить старое имя сервиса 
            // var service_name =  document.getElementById(service_name_value.id).getAttribute("value")
            document.getElementById("device_ident_old").setAttribute("value",device_ident_value);
            //  Получить и дабавить url сервиса 
            var device_inv_value = document.getElementById(device_inv_value.id).getAttribute('value');
            document.getElementById("device_inv_change").setAttribute("value",device_inv_value);
            
            var device_type_value = document.getElementById(device_type_value.id).getAttribute('value');
            document.getElementById("device_type_name_change").setAttribute("value",device_type_value);


             //  Получить и дабавить текст сервиса 
            var device_text_value = document.getElementById(device_text_value.id).value;
            var device_text_change = document.getElementById("device_text_change")
            device_text_change.value=device_text_value
            // // Получить и дабавить владельца сервиса 
            // var service_owner_value = document.getElementById(service_owner_value.id).getAttribute("value")
            // document.getElementById("service_owner_change").setAttribute("value",service_owner_value);
        } else {
            del.style.display = "none";
            document.getElementById(device_remove_hide.id).setAttribute("style","display: none;");
        }
        i++;
        // var service_name =  document.getElementById("service_name_value"+i).getAttribute("value")
        // document.getElementById("service_name_change").setAttribute("value",service_name);

    }

    // number_service = document.getElementById("number_service").getAttribute("value")
    // var i = 0;
    // while (i <= number_service) {
    //     // Получить и дабавить имя сервиса 
    //     var service_name =  document.getElementById("service_name_value"+i).getAttribute("value")
    //     document.getElementById("service_name_change").setAttribute("value",service_name);

    //     console.log(i);
    //     i++;
    //   }
    // // Получить и дабавить имя сервиса 
    // var service_name =  document.getElementById("service_name_value").getAttribute("value")
    // document.getElementById("service_name_change").setAttribute("value",service_name);
    // //  Получить и дабавить url сервиса 
    // var service_url_value = document.getElementById("service_url_value").getAttribute("value")
    // document.getElementById("service_url_change").setAttribute("value",service_url_value);
    // //  Получить и дабавить текст сервиса 
    // var service_text_value = document.getElementById("service_text_value").value;
    // var service_text_change = document.getElementById("service_text_change")
    // service_text_change.value=service_text_value
    // // Получить и дабавить владельца сервиса 
    // var service_owner_value = document.getElementById("service_owner_value").getAttribute("value")
    // document.getElementById("service_owner_change").setAttribute("value",service_owner_value);
    
        
//     var service_data = {
//         "service_name": service_name,
//         "service_url": service_url
//     }

// $.ajax({
//     type: 'POST',
//     url: '/service_send_data',
//     data: JSON.stringify(service_data),
//     contentType: 'application/json',
//     dataType: 'text',
//     // success: function(result) {
//     //     numRows.innerHTML = result.rows; 
//     // }  
// });
}
