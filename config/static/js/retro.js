var Retro = {

    seconds_clock: function () {

        // one second intervals
        function clock () {
            var now = new Date()
            var h = now.getHours()
            var m = now.getMinutes()
            var s = now.getSeconds()

            document.getElementById("hdr-date").innerHTML = h + ":" + m + ":" + s
            setTimeout(function() { clock() }, 1000)
        }

        clock()
    },

    recv_json: function (json) {
        console.log(json)

        const { id, value } = json
        document.getElementById(id).innerHTML = value
    },

    ui: function () {
        document.getElementById('check').onclick =
            () => {
                var wap = document.getElementById('access-point').value
                var password = document.getElementById('password').value
                document.getElementById('ap-status').innerHTML = 'checking: ' + wap + ' ' + password
                socket.emit('json', {webapp: { wap: wap, password: password }})
            }

        document.getElementById('commit').onclick =
            () => { socket.emit('json', {webapp: 'host'})}
    },
    
    init: function () {
        this.ui()
        this.seconds_clock()
    }
}
