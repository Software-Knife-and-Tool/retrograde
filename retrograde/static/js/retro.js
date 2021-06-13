var Retro = {

    panels: [
        'console-panel',
        'event-panel',
        'gra-afch-panel',
        'retrograde-panel',
        'status-panel',
        'watchdog-panel'
    ],
    
    seconds_clock: function () {

        function clock () {
            // one second intervals

            var now = new Date()
            var h = now.getHours()
            var m = now.getMinutes()
            var s = now.getSeconds()

            h = h > 12 ? h - 12 : h
            m = m < 10 ? '0' + m : m
            s = s < 10 ? '0' + s : s

            document.getElementById("date").innerHTML = h + ":" + m + ":" + s
            setTimeout(function() { clock() }, 1000)
        }

        clock()
    },

    recv_json: function (json) {
        const { id, value } = json
        document.getElementById(id).innerHTML = value
    },

    hide_panels: function () {
        this.panels.forEach(item => {
            document.getElementById(item).style.display = 'none'
        })
    },

    ui: function () {
        document.getElementById('toggle-button').onclick =
            () => { socket.emit('json', {webapp: 'toggle-button'})}
        document.getElementById('soft-reset').onclick =
            () => { socket.emit('json', {webapp: 'soft-reset'})}
        document.getElementById('hard-reset').onclick =
            () => { socket.emit('json', {webapp: 'hard-reset'})}

        document.getElementById('status').onclick =
            () => {
                    this.hide_panels()
                    document.getElementById('status-panel').style.display = ''
            }
        document.getElementById('retrograde').onclick =
            () => {
                    this.hide_panels()
                    document.getElementById('retrograde-panel').style.display = ''
            }
        document.getElementById('console').onclick =
            () => {
                    this.hide_panels()
                    document.getElementById('console-panel').style.display = ''
            }
        document.getElementById('events').onclick =
            () => {
                    this.hide_panels()
                    document.getElementById('event-panel').style.display = ''
            }
        document.getElementById('gra-afch').onclick =
            () => {
                    this.hide_panels()
                    document.getElementById('gra-afch-panel').style.display = ''
            }
        document.getElementById('watchdog').onclick =
            () => {
                    this.hide_panels()
                    document.getElementById('watchdog-panel').style.display = ''
            }

        this.hide_panels()
        document.getElementById('status-panel').style.display = ''
    },
    
    init: function () {
        this.ui()
        this.seconds_clock()
    }
}
