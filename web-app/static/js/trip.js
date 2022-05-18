var app = new Vue({
    el: '#app',
    data: {
        trip: null,
        vehicleId: null,
        tripId: null,
        start_time_str: "",
        end_time_str: "",
        imgs: [],
        v_colors: {
            "vgx": "blue",
            "vgy": "green",
            "vgz": "red",
        },
        a_colors: {
            "agx": "blue",
            "agy": "green",
            "agz": "red",
        },
        r_colors: {
            "yaw": "blue",
            "pitch": "green",
            "roll": "red"
        },
        bat_h_colors: {
            "bat": "red",
            "h": "blue"
        }
    },

    mounted: async function() {
        const urlParams = new URLSearchParams(window.location.search);
        this.vehicleId = urlParams.get('vehicleId');
        this.tripId = urlParams.get('tripId');

        var headers = new Headers();
        headers.append("x-api-key", config.apiToken);
        const url = config.apiHost + "/trip/" + this.vehicleId + "/" + this.tripId;
        var requestOptions = {method: 'GET', headers: headers};
        let response = await fetch(url, requestOptions);
        response = await response.json();
        console.log('Response', response);
        this.trip = response
        this.start_time_str = new Date(this.trip["start_time"] + " UTC").toLocaleString();
        this.end_time_str = new Date(this.trip["end_time"] + " UTC").toLocaleString();

        await Vue.nextTick();
        this.create_chart('velocities', this.v_colors, 'Velocities');
        this.create_chart('accelerations', this.a_colors, 'Accelerations');
        this.create_chart('rotations', this.r_colors, 'Yaw, Pitch and Roll');
        this.create_chart('bat_and_h', this.bat_h_colors, 'Battery and Height');
    },

    methods: {
        create_chart: function(divId, colorsDict, title) {
            var xs = unpack(this.trip.steps, "dt");
            var data = [];
            for (const [key, value] of Object.entries(colorsDict)) {
                let trace = {
                    type: "scatter",
                    mode: "lines",
                    name: key,
                    x: xs,
                    y: unpack(this.trip.steps, key),
                    line: {color: value}
                }
                data.push(trace);
            }
            var layout = {
                title: title,
                paper_bgcolor: "#2c2c2c", 
                plot_bgcolor: "#2c2c2c",
                font: {
                    color: "#fafafa",
                    family: '"Dosis", sans-serif'
                },
                yaxis: {
                    tickcolor: "#fafafa",
                    gridcolor: "rgba(255,255,255,0.6)",
                },
                xaxis: {
                    tickcolor: "#fafafa",
                    gridcolor: "rgba(255,255,255,0.6)",
                }
            };
            Plotly.newPlot(divId, data, layout);
        }
    }
});


function unpack(rows, key) {
    return rows.map(function(row) { return row[key]; });
}