const labels = [];

const dataTemperature = {
    labels: [],
    datasets: [
        {
            label: "Grad Celsius",
            data: [],
            borderColor: 'rgb(0,0,102)',
            backgroundColor: 'rgb(143,204,255)',
        
        },
    ]
};

const dataPressure = {
    labels: [],
    datasets: [
        {
            label: "hPa",
            data: [],
            borderColor: 'rgb(0,0,102)',
            backgroundColor: 'rgb(143,204,255)',

        },
    ]
};

const getConfigTemperature = (id) => {
    return {
        type: 'line',
        data: dataTemperature,
        id: id,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                }
            },
            scales: {
                y: {
                    suggestedMin: 15,
                    suggestedMax: 28
                }
            }
        }
    }
}

const getConfigPressure = (id) => {
    return {
        type: 'line',
        data: dataPressure,
        id: id,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                }
            },
            scales: {
                y: {
                    suggestedMin: 920,
                    suggestedMax: 1050
                }
            }
        }
    }
}



let id = 0;
const createChart = (htmlelement) => {
    console.log("init char", htmlelement)
    // config=createConfig(...)

    let temp;

    switch (htmlelement.id) {
        case "temperatureChart":
            temp = {
                key: htmlelement.id,
                chart: new Chart(htmlelement, getConfigTemperature(id))
            }
            break;
        case "pressureChart":
            temp = {
                key: htmlelement.id,
                chart: new Chart(htmlelement, getConfigPressure(id))
            }
            break;
    }


    console.log(temp)
    charts.push(temp)
    id++;
}
const charts = [];

const getChart = (key) => {
    console.log(charts);
    return charts.find(x => x.key == key).chart;
}

const getData = async () => {
    const response = await fetch("http://192.168.0.132:5001/weatherdata");
    const data = await response.json();
    return data;
}

const getWeatherString = async () => {
    const response = await fetch("http://192.168.0.132:5001/weatherstring");
    return response.text();
}

const setDataToChart = (data) => {
    let chartTemp = getChart("temperatureChart");
    let chartPress = getChart("pressureChart");
    console.log(chartTemp, chartPress)


    for (let i = data.length -1 ; i >= 0; i--) {
        let weatherdata = data[i];

        chartTemp.data.labels.push(parseDate(weatherdata.datetime));
        chartTemp.data.datasets[0].data.push(weatherdata.temperature);
        chartTemp.update();

        chartPress.data.labels.push(parseDate(weatherdata.datetime));
        chartPress.data.datasets[0].data.push(weatherdata.pressure);
        chartPress.update();
    }
}

function parseDate(dateToParse) {
    var date = new Date(dateToParse);

    const months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"];
    let month = months[date.getMonth()];

    return date.getDate() + "." + month + ". " + date.getHours() + ":" + getMinute(date.getMinutes()) + " Uhr";
}

function setAltitude(data) {
    var altitudeLabel = document.getElementById("altitude-label");

    altitudeLabel.innerHTML = data[data.length - 1].altitude + " Meter";
}

function setWeatherData(weatherString) {
    var weatherStringLabel = document.getElementById("weather-string");

    weatherStringLabel.innerHTML = weatherString;
}

function getMinute(number) {
    if (number < 10) {
        return '0' + number;
    }
    return number;
}
