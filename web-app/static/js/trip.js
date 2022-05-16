var app = new Vue({
    el: '#app',
    data: {
        trip: null,
        vehicleId: null,
        tripId: null,
        imgs: []
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
        this.trip = response;
    },

    methods: {}
});