const labels = [];

const data = {
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


const getConfig=(id)=>{
    return {
        type: 'line',
        data: data,
        id:id,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                }
            }
        }
}
}
let id=0;
const createChart=(htmlelement)=>{
    console.log("init char",htmlelement)
    // config=createConfig(...)
    const temp={
        key: htmlelement.id,
        chart:new Chart(htmlelement,getConfig(id))
    }
    console.log(temp)
    charts.push(temp)
    id++;
}
const charts=[];

const getChart=(key)=>{
    console.log(charts);
    return charts.find(x => x.key == key).chart;
}

const getData=async()=>{
    const response = await fetch("http://172.20.10.6:5001/weatherdata"); //API einfügen
    const data= await response.json();
    console.log(data);
 return data;
}

// Labels einfügen, Daten einfügen

const setDataToChart=(data)=>{
    let chartTemp=getChart("temperatureChart");
    let chartPress=getChart("pressureChart");
    console.log(chartTemp,chartPress)
    for (const weatherdata of data) {
        chartTemp.data.labels.push(weatherdata.datetime);
        chartTemp.data.datasets[0].data.push(weatherdata.temperature);
        chartTemp.update();
        
        chartPress.data.labels.push(weatherdata.datetime);
        chartPress.data.datasets[0].data.push(weatherdata.pressure);
        chartPress.update();
}
/*
[{
    temperature: number
    pressure: number
    altitude: number
    datetime: date
}]
*/}