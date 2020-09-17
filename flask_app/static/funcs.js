function progress_color() {
    let bars = document.getElementsByClassName("progress-bar");

    for (let bar of bars) {
        if (parseInt(bar.style.width.slice(0, -1)) == 100) {
            bar.style.backgroundColor = "red";
        } else if (parseInt(bar.style.width.slice(0, -1)) > 75) {
            bar.style.backgroundColor = "orange";
        } else if (parseInt(bar.style.width.slice(0, -1)) < 50) {
            bar.style.backgroundColor = "green";
        } else {
            bar.style.backgroundColor = "#FFDF6E";
        }
    }
};


function show_stop_propagation(modal_id, event) {
    $("#" + modal_id).modal();
    event.stopPropagation();
}

function stop_propagation(event) {
    event.stopPropagation();
}

function add_to_map(filename) {
    var array = [];
    var checkboxes = document.querySelectorAll('input[class=map_check]:checked');

    for (var i = 0; i < checkboxes.length; i++) {
        array.push(checkboxes[i].id.substring(3));
    }
    $.ajax({
        url: '/pets/prazos',
        type: 'POST',
        data: {
            "codes": JSON.stringify(array)
        }
    });
    setTimeout(function () {
        window.open("/pets/prazo/" + filename)
    }, 3000); //needed so that backend can create file (flask send_file not working)
};

// modals updates



$(document).ready(function () {
    $(".toast").toast('show');
});