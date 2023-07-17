function send_data() {
    // number_service = document.getElementById("number_service").getAttribute("value")
    // console.log(user_name);
    // var i = 0;
    // document.addEventListener("keydown", function(){
    // var x=event.keyCode || event.which;
    // if(x==13)
    // {
    // $("#user_name").on("keyup", function(event){
    // if (event.which == 13)
    // var hide = document.getElementById("hide_user_data");
    // if (hide.style.display == "none") {
    //     hide.style.display = "block";
    // }

        // $(document).ready(function() {
        // $('#user_name1').on('submit',function(e){  

        // var user_name = document.getElementById("user_name").value;
        // console.log(user_name);
        // var user_data = {
        //     'user_name': user_name
        // }

    //     $.ajax({
    //         data : {
    //             user_name : $('#user_name').val(),
    //         },
    //         type : 'POST',
    //         url : '/search'
    //       })
    //       .done(function(data){
    //         $('#hide_user_data').text(data.output).show();
    //       });
    //       e.preventDefault();
    //     });
    // })  
    // }
//
    
        $(document).ready(function() {
        $('#user_name_form').on('submit',function(e){  
            var form = $("#user_name_form");
        $.ajax({
                data : {
                    user_name : $('#user_name').val(),
                },
               
                data: form.serialize(),
                type: 'POST',
                url: '/service_send_data',
            //   })
                success: function(data) {
                console.log(data)      
                // Ajax call completed successfully
                // alert("Form Submited Successfully");
                $('#hide_user_data').text(data.service_data[1]);
              
                // JSON.stringify(data)

            },
              });
              e.preventDefault();
             
            });
        });
    }


//       $.ajax({
//             type: 'POST',
//             url: '/search',
//             // data: JSON.stringify(user_data),
//             contentType: 'application/json;',
//             data: JSON.stringify(user_data),
            
//             dataType: 'json',
//             success: function(result) {
//             // numRows.innerHTML = result.rows; 
//         }  
//         });
//     })
//     })  
    
// }

//     })
// }
    // var i = 0;
    // while (i < number_device) {
    //     var device_ident =  document.getElementById(device_ident_value.id).getAttribute("value")
    //     var device_data = {
    //         "device_ident": device_ident
    //     }


    //     $.ajax({
    //         type: 'POST',
    //         url: '/service_send_data',
    //         data: JSON.stringify(device_data),
    //         contentType: 'application/json',
    //         dataType: 'text',
    //     });
    //     i++;
    // }

