function show_date() {
    var d = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    document.getElementById('date').innerText = d.toLocaleDateString(undefined, options) + ' ' + d.toLocaleTimeString();
    setTimeout(function(){ show_date(); }, 1000);
}

function show_host() {
    document.getElementById('host').innerText = window.location.hostname;
}

function show_version() {
    document.getElementById('version').innerText = "0.0.1";
}

function show_nfc() {
    document.getElementById('nfc-status').innerText = "inactive";
}

show_date();
show_host();
show_version();
show_nfc();
