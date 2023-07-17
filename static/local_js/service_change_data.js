function service_change_data(service,service_remove_hide,service_name_value,service_url_value,service_text_value,service_owner_value) {
    // var service_check_value = document.getElementById("service_name");
    // var service_name_change = document.getElementById("service_name_change");
    // var service_check = document.getElementById("service_check");
    // var service_url_value = document.getElementById("service_url_value");
    // var service_url = document.getElementById("service_url").value;
    // var service_text = document.getElementById("service_text").value;
    // var service_owner = document.getElementById("service_owner").value;
    // var inv_number = parseInt(document.getElementById("inv_number").value);

    // var checkBox  = document.getElementById("service_check");
    // var del = document.getElementById("service_change_hide");
    //     if (checkBox.checked == true) {
    //         del.style.display = "block";
    //     } else {
    //         del.style.display = "none";
    //     }

    number_service = document.getElementById("number_service").getAttribute("value")
    
    var i = 0;
    while (i < number_service) {
        var checkBox  = document.getElementById(service.id)
        console.log(checkBox);
        var del = document.getElementById("service_change_hide");
        if (checkBox.checked == true) {
            del.style.display = "block";

           // Показать кнопку удаление сервиса 
            document.getElementById(service_remove_hide.id).setAttribute("style","display: block;");
            // Получить и дабавить имя сервиса 
            var service_name =  document.getElementById(service_name_value.id).getAttribute("value")
            document.getElementById("service_name_change").setAttribute("value",service_name);
            // Получить и дабавить старое имя сервиса 
            var service_name =  document.getElementById(service_name_value.id).getAttribute("value")
            document.getElementById("service_name_old").setAttribute("value",service_name);
            //  Получить и дабавить url сервиса 
            var service_url_value = document.getElementById(service_url_value.id).getAttribute('value');
            document.getElementById("service_url_change").setAttribute("value",service_url_value);
             //  Получить и дабавить текст сервиса 
            var service_text_value = document.getElementById(service_text_value.id).value;
            var service_text_change = document.getElementById("service_text_change")
            service_text_change.value=service_text_value
            // Получить и дабавить владельца сервиса 
            var service_owner_value = document.getElementById(service_owner_value.id).getAttribute("value")
            document.getElementById("service_owner_change").setAttribute("value",service_owner_value);
        } else {
            del.style.display = "none";
            document.getElementById(service_remove_hide.id).setAttribute("style","display: none;");
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
