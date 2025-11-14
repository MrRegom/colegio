/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Dashboard crypto init js
*/

// get colors array from the string
function getChartColorsArray(chartId) {
    const chartElement = document.getElementById(chartId);
    if (chartElement) {
        const colors = chartElement.dataset.colors;
        if (colors) {
            const parsedColors = JSON.parse(colors);
            const mappedColors = parsedColors.map((value) => {
                const newValue = value.replace(/\s/g, "");
                if (!newValue.includes(",")) {
                    const color = getComputedStyle(document.documentElement).getPropertyValue(newValue);
                    return color || newValue;
                } else {
                    const val = value.split(",");
                    if (val.length === 2) {
                        const rgbaColor = `rgba(${getComputedStyle(document.documentElement).getPropertyValue(val[0])}, ${val[1]})`;
                        return rgbaColor;
                    } else {
                        return newValue;
                    }
                }
            });
            return mappedColors;
        } else {
            console.warn(`data-colors attribute not found on: ${chartId}`);
        }
    }
}

var ethereumOverviewChart = "";
var stockMarketActiveChart = "";
var stockMarketGainersChart = "";
var marketCapitalizationChart = "";
var allocationOverviewChart = "";

function loadCharts() {

    //  ethereum_overview Charts
    var ethereumOverviewColors = "";
    ethereumOverviewColors = getChartColorsArray("ethereum_overview");
    if (ethereumOverviewColors) {
        var options = {
            series: [{
                data: [{
                    x: new Date(1538778600000),
                    y: [6629.81, 6650.5, 6623.04, 6633.33]
                },
                {
                    x: new Date(1538780400000),
                    y: [6632.01, 6643.59, 6620, 6630.11]
                },
                {
                    x: new Date(1538782200000),
                    y: [6630.71, 6648.95, 6623.34, 6635.65]
                },
                {
                    x: new Date(1538784000000),
                    y: [6635.65, 6651, 6629.67, 6638.24]
                },
                {
                    x: new Date(1538785800000),
                    y: [6638.24, 6640, 6620, 6624.47]
                },
                {
                    x: new Date(1538787600000),
                    y: [6624.53, 6636.03, 6621.68, 6624.31]
                },
                {
                    x: new Date(1538789400000),
                    y: [6624.61, 6632.2, 6617, 6626.02]
                },
                {
                    x: new Date(1538791200000),
                    y: [6627, 6627.62, 6584.22, 6603.02]
                },
                {
                    x: new Date(1538793000000),
                    y: [6605, 6608.03, 6598.95, 6604.01]
                },
                {
                    x: new Date(1538794800000),
                    y: [6604.5, 6614.4, 6602.26, 6608.02]
                },
                {
                    x: new Date(1538796600000),
                    y: [6608.02, 6610.68, 6601.99, 6608.91]
                },
                {
                    x: new Date(1538798400000),
                    y: [6608.91, 6618.99, 6608.01, 6612]
                },
                {
                    x: new Date(1538800200000),
                    y: [6612, 6615.13, 6605.09, 6612]
                },
                {
                    x: new Date(1538802000000),
                    y: [6612, 6624.12, 6608.43, 6622.95]
                },
                {
                    x: new Date(1538803800000),
                    y: [6623.91, 6623.91, 6615, 6615.67]
                },
                {
                    x: new Date(1538805600000),
                    y: [6618.69, 6618.74, 6610, 6610.4]
                },
                {
                    x: new Date(1538807400000),
                    y: [6611, 6622.78, 6610.4, 6614.9]
                },
                {
                    x: new Date(1538809200000),
                    y: [6614.9, 6626.2, 6613.33, 6623.45]
                },
                {
                    x: new Date(1538811000000),
                    y: [6623.48, 6627, 6618.38, 6620.35]
                },
                {
                    x: new Date(1538812800000),
                    y: [6619.43, 6620.35, 6610.05, 6615.53]
                },
                {
                    x: new Date(1538814600000),
                    y: [6615.53, 6617.93, 6610, 6615.19]
                },
                {
                    x: new Date(1538816400000),
                    y: [6615.19, 6621.6, 6608.2, 6620]
                },
                {
                    x: new Date(1538818200000),
                    y: [6619.54, 6625.17, 6614.15, 6620]
                },
                {
                    x: new Date(1538820000000),
                    y: [6620.33, 6634.15, 6617.24, 6624.61]
                },
                {
                    x: new Date(1538821800000),
                    y: [6625.95, 6626, 6611.66, 6617.58]
                },
                {
                    x: new Date(1538823600000),
                    y: [6619, 6625.97, 6595.27, 6598.86]
                },
                {
                    x: new Date(1538825400000),
                    y: [6598.86, 6598.88, 6570, 6587.16]
                },
                {
                    x: new Date(1538827200000),
                    y: [6588.86, 6600, 6580, 6593.4]
                },
                {
                    x: new Date(1538829000000),
                    y: [6593.99, 6598.89, 6585, 6587.81]
                },
                {
                    x: new Date(1538830800000),
                    y: [6587.81, 6592.73, 6567.14, 6578]
                },
                {
                    x: new Date(1538832600000),
                    y: [6578.35, 6581.72, 6567.39, 6579]
                },
                {
                    x: new Date(1538834400000),
                    y: [6579.38, 6580.92, 6566.77, 6575.96]
                },
                {
                    x: new Date(1538836200000),
                    y: [6575.96, 6589, 6571.77, 6588.92]
                },
                {
                    x: new Date(1538838000000),
                    y: [6588.92, 6594, 6577.55, 6589.22]
                },
                {
                    x: new Date(1538839800000),
                    y: [6589.3, 6598.89, 6589.1, 6596.08]
                },
                {
                    x: new Date(1538841600000),
                    y: [6597.5, 6600, 6588.39, 6596.25]
                },
                {
                    x: new Date(1538843400000),
                    y: [6598.03, 6600, 6588.73, 6595.97]
                },
                {
                    x: new Date(1538845200000),
                    y: [6595.97, 6602.01, 6588.17, 6602]
                },
                {
                    x: new Date(1538847000000),
                    y: [6602, 6607, 6596.51, 6599.95]
                },
                {
                    x: new Date(1538848800000),
                    y: [6600.63, 6601.21, 6590.39, 6591.02]
                },
                {
                    x: new Date(1538850600000),
                    y: [6591.02, 6603.08, 6591, 6591]
                },
                {
                    x: new Date(1538852400000),
                    y: [6591, 6601.32, 6585, 6592]
                },
                {
                    x: new Date(1538854200000),
                    y: [6593.13, 6596.01, 6590, 6593.34]
                },
                {
                    x: new Date(1538856000000),
                    y: [6593.34, 6604.76, 6582.63, 6593.86]
                },
                {
                    x: new Date(1538857800000),
                    y: [6593.86, 6604.28, 6586.57, 6600.01]
                },
                {
                    x: new Date(1538859600000),
                    y: [6601.81, 6603.21, 6592.78, 6596.25]
                },
                {
                    x: new Date(1538861400000),
                    y: [6596.25, 6604.2, 6590, 6602.99]
                },
                {
                    x: new Date(1538863200000),
                    y: [6602.99, 6606, 6584.99, 6587.81]
                },
                {
                    x: new Date(1538865000000),
                    y: [6587.81, 6595, 6583.27, 6591.96]
                },
                {
                    x: new Date(1538866800000),
                    y: [6591.97, 6596.07, 6585, 6588.39]
                },
                {
                    x: new Date(1538868600000),
                    y: [6587.6, 6598.21, 6587.6, 6594.27]
                },
                {
                    x: new Date(1538870400000),
                    y: [6596.44, 6601, 6590, 6596.55]
                },
                {
                    x: new Date(1538872200000),
                    y: [6598.91, 6605, 6596.61, 6600.02]
                },
                {
                    x: new Date(1538874000000),
                    y: [6600.55, 6605, 6589.14, 6593.01]
                },
                {
                    x: new Date(1538875800000),
                    y: [6593.15, 6605, 6592, 6603.06]
                },
                {
                    x: new Date(1538877600000),
                    y: [6603.07, 6604.5, 6599.09, 6603.89]
                },
                {
                    x: new Date(1538879400000),
                    y: [6604.44, 6604.44, 6600, 6603.5]
                },
                {
                    x: new Date(1538881200000),
                    y: [6603.5, 6603.99, 6597.5, 6603.86]
                },
                {
                    x: new Date(1538883000000),
                    y: [6603.85, 6605, 6600, 6604.07]
                },
                {
                    x: new Date(1538884800000),
                    y: [6604.98, 6606, 6604.07, 6606]
                },
                ]
            }],
            chart: {
                type: 'candlestick',
                height: 367,
                toolbar: {
                    show: false,
                }
            },
            grid: {
                padding: {
                    bottom: 0,
                    right: 0
                }
            },
            plotOptions: {
                candlestick: {
                    colors: {
                        upward: ethereumOverviewColors[0],
                        downward: ethereumOverviewColors[1],
                    }
                }
            },
            xaxis: {
                type: 'datetime'
            },
            yaxis: {
                tooltip: {
                    enabled: true
                }
            },
        };

        if (ethereumOverviewChart != "")
            ethereumOverviewChart.destroy();
        ethereumOverviewChart = new ApexCharts(document.querySelector("#ethereum_overview"), options);
        ethereumOverviewChart.render();
    }
    
    // stock_market_active
    var stockMarketActiveColors = "";
    stockMarketActiveColors = getChartColorsArray("stock_market_active");
    if (stockMarketActiveColors) {
        var options = {
            series: [{
                name: 'Ethereum Classic (ETC)',
                data: [{
                    x: new Date('2018-01-26').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-01-27').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-01-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-01-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-01-30').getTime(),
                    y: 158
                }, {
                    x: new Date('2018-02-01').getTime(),
                    y: 153
                }, {
                    x: new Date('2018-02-02').getTime(),
                    y: 149
                }, {
                    x: new Date('2018-02-03').getTime(),
                    y: 144
                }, {
                    x: new Date('2018-02-05').getTime(),
                    y: 150
                }, {
                    x: new Date('2018-02-06').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-02-07').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-02-08').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-02-09').getTime(),
                    y: 156
                }, {
                    x: new Date('2018-02-11').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-02-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-02-13').getTime(),
                    y: 161
                }, {
                    x: new Date('2018-02-14').getTime(),
                    y: 150
                }, {
                    x: new Date('2018-02-15').getTime(),
                    y: 154
                }, {
                    x: new Date('2018-02-16').getTime(),
                    y: 160
                }, {
                    x: new Date('2018-02-17').getTime(),
                    y: 165
                }, {
                    x: new Date('2018-02-18').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-02-20').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-02-21').getTime(),
                    y: 164
                }, {
                    x: new Date('2018-02-22').getTime(),
                    y: 160
                }, {
                    x: new Date('2018-02-23').getTime(),
                    y: 165
                }, {
                    x: new Date('2018-02-24').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-02-25').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-02-26').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-02-27').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-02-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-02-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-02-30').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-03-01').getTime(),
                    y: 158
                }, {
                    x: new Date('2018-03-02').getTime(),
                    y: 152
                }, {
                    x: new Date('2018-03-03').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-03-05').getTime(),
                    y: 142
                }, {
                    x: new Date('2018-03-06').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-03-07').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-03-08').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-03-09').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-03-11').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-03-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-03-13').getTime(),
                    y: 161
                }, {
                    x: new Date('2018-03-14').getTime(),
                    y: 166
                }, {
                    x: new Date('2018-03-15').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-03-16').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-03-17').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-03-18').getTime(),
                    y: 181
                }, {
                    x: new Date('2018-03-20').getTime(),
                    y: 178
                }, {
                    x: new Date('2018-03-21').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-03-22').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-03-23').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-03-24').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-03-25').getTime(),
                    y: 164
                }, {
                    x: new Date('2018-03-26').getTime(),
                    y: 168
                }, {
                    x: new Date('2018-03-27').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-03-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-03-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-03-30').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-04-01').getTime(),
                    y: 158
                }, {
                    x: new Date('2018-04-02').getTime(),
                    y: 152
                }, {
                    x: new Date('2018-04-03').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-04-05').getTime(),
                    y: 142
                }, {
                    x: new Date('2018-04-06').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-04-07').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-04-08').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-04-09').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-04-11').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-04-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-04-13').getTime(),
                    y: 161
                }, {
                    x: new Date('2018-04-14').getTime(),
                    y: 166
                }, {
                    x: new Date('2018-04-15').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-04-16').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-04-17').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-04-18').getTime(),
                    y: 181
                }, {
                    x: new Date('2018-04-20').getTime(),
                    y: 178
                }, {
                    x: new Date('2018-04-21').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-04-22').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-04-23').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-04-24').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-04-25').getTime(),
                    y: 164
                }, {
                    x: new Date('2018-04-26').getTime(),
                    y: 168
                }, {
                    x: new Date('2018-04-27').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-04-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-04-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-04-30').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-05-01').getTime(),
                    y: 158
                }, {
                    x: new Date('2018-05-02').getTime(),
                    y: 152
                }, {
                    x: new Date('2018-05-03').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-05-04').getTime(),
                    y: 142
                }, {
                    x: new Date('2018-05-05').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-05-07').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-05-08').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-05-09').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-05-11').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-05-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-05-13').getTime(),
                    y: 161
                }]
            }],
            chart: {
                type: 'area',
                stacked: false,
                height: 150,
                sparkline: {
                    enabled: true
                },
                zoom: {
                    type: 'x',
                    enabled: true,
                    autoScaleYaxis: true
                },
                toolbar: {
                    show: false,
                }
            },
            colors: stockMarketActiveColors,
            dataLabels: {
                enabled: false
            },
            markers: {
                size: 0,
            },
            grid: {
                padding: {
                    top: -15,
                }
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    inverseColors: false,
                    opacityFrom: 0.5,
                    opacityTo: 0,
                    stops: [0, 90, 100]
                },
            },
            yaxis: {
                showAlways: true,
                labels: {
                    show: false,
                    formatter: function (val) {
                        return (val / 1000000).toFixed(0);
                    },
                },
            },
            stroke: {
                width: 2,
                curve: 'smooth'
            },
            xaxis: {
                labels: {
                    show: false,
                },
                type: 'datetime',
            },
            tooltip: {
                shared: false,
                y: {
                    formatter: function (val) {
                        return (val / 1000000).toFixed(0)
                    }
                }
            }
        };

        if (stockMarketActiveChart != "")
            stockMarketActiveChart.destroy();
        stockMarketActiveChart = new ApexCharts(document.querySelector("#stock_market_active"), options);
        stockMarketActiveChart.render();
    }

    // stock_market_gainers
    var stockMarketGainersColors = "";
    stockMarketGainersColors = getChartColorsArray("stock_market_gainers");
    if (stockMarketGainersColors) {
        var options = {
            series: [{
                name: 'Monero (XMR) ',
                data: [{
                    x: new Date('2018-02-05').getTime(),
                    y: 150
                }, {
                    x: new Date('2018-02-06').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-02-07').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-02-08').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-02-09').getTime(),
                    y: 156
                }, {
                    x: new Date('2018-02-11').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-02-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-02-13').getTime(),
                    y: 161
                }, {
                    x: new Date('2018-02-14').getTime(),
                    y: 150
                }, {
                    x: new Date('2018-02-15').getTime(),
                    y: 154
                }, {
                    x: new Date('2018-02-16').getTime(),
                    y: 160
                }, {
                    x: new Date('2018-02-17').getTime(),
                    y: 165
                }, {
                    x: new Date('2018-02-18').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-02-20').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-02-21').getTime(),
                    y: 164
                }, {
                    x: new Date('2018-02-22').getTime(),
                    y: 160
                }, {
                    x: new Date('2018-02-23').getTime(),
                    y: 165
                }, {
                    x: new Date('2018-02-24').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-02-25').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-02-26').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-02-27').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-02-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-02-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-02-30').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-03-01').getTime(),
                    y: 158
                }, {
                    x: new Date('2018-03-02').getTime(),
                    y: 152
                }, {
                    x: new Date('2018-03-03').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-03-05').getTime(),
                    y: 142
                }, {
                    x: new Date('2018-03-06').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-03-07').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-03-08').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-03-09').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-03-11').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-03-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-03-13').getTime(),
                    y: 161
                }, {
                    x: new Date('2018-03-14').getTime(),
                    y: 166
                }, {
                    x: new Date('2018-03-15').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-03-16').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-03-17').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-03-18').getTime(),
                    y: 181
                }, {
                    x: new Date('2018-03-20').getTime(),
                    y: 178
                }, {
                    x: new Date('2018-03-21').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-03-22').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-03-23').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-03-24').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-03-25').getTime(),
                    y: 164
                }, {
                    x: new Date('2018-03-26').getTime(),
                    y: 168
                }, {
                    x: new Date('2018-03-27').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-03-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-03-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-03-30').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-04-01').getTime(),
                    y: 158
                }, {
                    x: new Date('2018-04-02').getTime(),
                    y: 152
                }, {
                    x: new Date('2018-04-03').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-04-05').getTime(),
                    y: 142
                }, {
                    x: new Date('2018-04-06').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-04-07').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-04-08').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-04-09').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-04-11').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-04-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-04-13').getTime(),
                    y: 161
                }, {
                    x: new Date('2018-04-14').getTime(),
                    y: 166
                }, {
                    x: new Date('2018-04-15').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-04-16').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-04-17').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-04-18').getTime(),
                    y: 181
                }, {
                    x: new Date('2018-04-20').getTime(),
                    y: 178
                }, {
                    x: new Date('2018-04-21').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-04-22').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-04-23').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-04-24').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-04-25').getTime(),
                    y: 164
                }, {
                    x: new Date('2018-04-26').getTime(),
                    y: 168
                }, {
                    x: new Date('2018-04-27').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-04-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-04-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-04-30').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-05-01').getTime(),
                    y: 158
                }, {
                    x: new Date('2018-05-02').getTime(),
                    y: 152
                }, {
                    x: new Date('2018-05-03').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-05-04').getTime(),
                    y: 142
                }, {
                    x: new Date('2018-05-05').getTime(),
                    y: 147
                }, {
                    x: new Date('2018-05-07').getTime(),
                    y: 151
                }, {
                    x: new Date('2018-05-08').getTime(),
                    y: 155
                }, {
                    x: new Date('2018-05-09').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-05-11').getTime(),
                    y: 162
                }, {
                    x: new Date('2018-05-12').getTime(),
                    y: 157
                }, {
                    x: new Date('2018-05-13').getTime(),
                    y: 161
                }, {
                    x: new Date('2018-05-14').getTime(),
                    y: 166
                }, {
                    x: new Date('2018-05-15').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-05-16').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-05-17').getTime(),
                    y: 177
                }, {
                    x: new Date('2018-05-18').getTime(),
                    y: 181
                }, {
                    x: new Date('2018-05-20').getTime(),
                    y: 178
                }, {
                    x: new Date('2018-05-21').getTime(),
                    y: 173
                }, {
                    x: new Date('2018-05-22').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-05-23').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-05-24').getTime(),
                    y: 159
                }, {
                    x: new Date('2018-05-25').getTime(),
                    y: 164
                }, {
                    x: new Date('2018-05-26').getTime(),
                    y: 168
                }, {
                    x: new Date('2018-05-27').getTime(),
                    y: 172
                }, {
                    x: new Date('2018-05-28').getTime(),
                    y: 169
                }, {
                    x: new Date('2018-05-29').getTime(),
                    y: 163
                }, {
                    x: new Date('2018-05-30').getTime(),
                    y: 162
                },]
            }],
            chart: {
                type: 'area',
                stacked: false,
                height: 150,
                sparkline: {
                    enabled: true
                },
                zoom: {
                    type: 'x',
                    enabled: true,
                    autoScaleYaxis: true
                },
                toolbar: {
                    show: false,
                }
            },
            colors: stockMarketGainersColors,
            dataLabels: {
                enabled: false
            },
            markers: {
                size: 0,
            },
            grid: {
                padding: {
                    top: -15,
                }
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    inverseColors: false,
                    opacityFrom: 0.5,
                    opacityTo: 0,
                    stops: [0, 90, 100]
                },
            },
            yaxis: {
                showAlways: true,
                labels: {
                    show: false,
                    formatter: function (val) {
                        return (val / 1000000).toFixed(0);
                    },
                },
            },
            stroke: {
                width: 2,
                curve: 'smooth'
            },
            xaxis: {
                labels: {
                    show: false,
                },
                type: 'datetime',
            },
            tooltip: {
                shared: false,
                y: {
                    formatter: function (val) {
                        return (val / 1000000).toFixed(0)
                    }
                }
            }
        };

        if (stockMarketGainersChart != "")
            stockMarketGainersChart.destroy();
        stockMarketGainersChart = new ApexCharts(document.querySelector("#stock_market_gainers"), options);
        stockMarketGainersChart.render();
    }

    // market_capitalization Chart
    var marketCapitalizationColors = "";
    marketCapitalizationColors = getChartColorsArray("market_capitalization");
    if (marketCapitalizationColors) {
        var options = {
            series: [44, 55, 41, 17, 33],
            labels: ['Giant', 'Large', 'Mid', 'Small', 'Micro'],
            chart: {
                height: 227,
                type: 'donut',
            },
            plotOptions: {
                pie: {
                    startAngle: -90,
                    endAngle: 270
                }
            },
            dataLabels: {
                enabled: false
            },
            fill: {
                type: 'gradient',
            },
            legend: {
                formatter: function (val, opts) {
                    return val + " - " + opts.w.globals.series[opts.seriesIndex]
                }
            },
            legend: {
                show: false,
                position: 'bottom'
            },
            colors: marketCapitalizationColors
        };

        if (marketCapitalizationChart != "")
            marketCapitalizationChart.destroy();
        marketCapitalizationChart = new ApexCharts(document.querySelector("#market_capitalization"), options);
        marketCapitalizationChart.render();
    }

    // allocation_overview Chart
    var allocationOverviewColors = "";
    allocationOverviewColors = getChartColorsArray("allocation_overview");
    if (allocationOverviewColors) {
        var options = {
            series: [150, 123, 145, 162, 133],
            chart: {
                height: 227,
                type: 'donut',
            },
            labels: ['Cash', 'Fixed Income', 'Equities', 'FX', 'Alternative'],
            plotOptions: {
                pie: {
                    startAngle: -90,
                    endAngle: 270
                }
            },
            dataLabels: {
                enabled: false
            },
            fill: {
                type: 'gradient',
            },
            legend: {
                formatter: function (val, opts) {
                    return val + " - " + opts.w.globals.series[opts.seriesIndex]
                }
            },
            legend: {
                show: false,
                position: 'bottom'
            },
            colors: allocationOverviewColors
        };

        if (allocationOverviewChart != "")
            allocationOverviewChart.destroy();
        allocationOverviewChart = new ApexCharts(document.querySelector("#allocation_overview"), options);
        allocationOverviewChart.render();
    }
}

window.addEventListener("resize", function () {
    setTimeout(() => {
        loadCharts();
    }, 250);
});
loadCharts();


//leadsList Table
var options = new List('leadsList', {
    valueNames: [
        "coin_name",
        "price",
        "24h_change",
        "total_coin"
    ],
    page: 5,
    pagination: true,
    pagination: {
        item: '<li><a class="page" href="#!"></a></li>'
    }
});