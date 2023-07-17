
function show_del() {

    var checkBox  = document.getElementById("service_check");
    var del = document.getElementById("service_change_hide");
        if (checkBox.checked == true) {
            del.style.display = "block";
        } else {
            del.style.display = "none";
        }

}
