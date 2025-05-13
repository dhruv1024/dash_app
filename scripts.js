var trace1 = {
    x: [5.1, 4.9, 6.7, 5.6, 5.7],
    y: [3.5, 3.0, 3.1, 2.5, 3.8],
    mode: 'markers',
    type: 'scatter',
    name: 'Iris setosa',
    marker: { size: 12 }
};

var data = [trace1];

var layout = {
    title: 'Iris Sepal Length vs Width',
    xaxis: { title: 'Sepal Length' },
    yaxis: { title: 'Sepal Width' }
};

Plotly.newPlot('myPlot', data, layout);
