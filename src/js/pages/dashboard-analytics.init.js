/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Dashboard Analytics init js
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

var pageViewsOverviewChart = "";
var salesReportChart = "";
var weeklyVisitorsChart = "";
var sessionCountryChart = "";
var salesFunnelChart = "";
var teamPerformanceChart = ""; 
var chartBubbleSimpleChart = "";

function loadCharts() {

    //pageviews_overview chart
    var pageViewsOverviewColors = '';
    pageViewsOverviewColors = getChartColorsArray("pageviews_overview");
    if (pageViewsOverviewColors) {
        var options = {
            series: [{
                name: 'Website',
                data: [12, 14, 28, 25, 19, 23, 21, 23, 20, 18, 12, 28, 28, 25, 19, 23, 18, 29, 23, 27, 18, 29, 23, 25, 20, 30, 23, 29, 22, 27, 33]
            },
            {
                name: 'Social Media',
                data: [26, 24, 18, 29, 23, 27, 24, 27, 22, 25, 24, 29, 18, 29, 23, 27, 18, 29, 23, 29, 14, 14, 18, 29, 18, 29, 21, 27, 29, 23, 24]
            }
            ],
            chart: {
                type: 'bar',
                height: 250,
                stacked: true,
                toolbar: {
                    show: false
                }
            },
            plotOptions: {
                bar: {
                    columnWidth: '60%',
                    borderRadius: 5,
                    lineCap: 'round',
                    borderRadiusOnAllStackedSeries: true

                },
            },
            colors: pageViewsOverviewColors,
            fill: {
                opacity: 1
            },
            dataLabels: {
                enabled: false,
                textAnchor: 'top',
            },
            grid: {
                padding: {
                    top: -20,
                    right: 0,
                }
            },
            legend: {
                show: false,
                position: 'top',
                horizontalAlign: 'right',
            },
            xaxis: {
                type: 'datetime',
                categories: ['06/01/2023 GMT', '06/02/2023 GMT', '06/03/2023 GMT', '06/04/2023 GMT',
                    '06/05/2023 GMT', '06/06/2023 GMT', '06/07/2023 GMT', '06/08/2023 GMT', '06/09/2023 GMT',
                    '06/10/2023 GMT', '06/11/2023 GMT', '06/12/2023 GMT', '06/13/2023 GMT', '06/14/2023 GMT', '06/15/2023 GMT', '06/16/2023 GMT', '06/17/2023 GMT',
                    '06/18/2023 GMT', '06/19/2023 GMT', '06/20/2023 GMT', '06/21/2023 GMT', '06/22/2023', '06/23/2023', '06/24/2023', '06/25/2023', '06/26/2023', '06/27/2023', '06/28/2023', '06/29/2023', '06/30/2023', '06/31/2023'
                ],
                labels: {
                    rotate: -90
                },
                axisTicks: {
                    show: true,
                },
                axisBorder: {
                    show: true,
                    stroke: {
                        width: 1
                    },
                },
            },
        };

        if (pageViewsOverviewChart != "")
            pageViewsOverviewChart.destroy();
        pageViewsOverviewChart = new ApexCharts(document.querySelector("#pageviews_overview"), options);
        pageViewsOverviewChart.render();
    }

    //  sales_Report Charts
    var salesReportColors = '';
    salesReportColors = getChartColorsArray("sales_Report");
    if (salesReportColors) {
        var options = {
            series: [{
                name: 'Order',
                data: [45, 74, 36, 69, 84, 97, 92]
            }, {
                name: 'Return',
                data: [11, 18, 24, 32, 46, 65, 73]
            }],
            chart: {
                height: 225,
                type: 'area',
                toolbar: {
                    show: false
                }
            },
            grid: {
                padding: {
                    top: -20,
                    bottom: 0,
                },
            },
            legend: {
                show: false,
                position: 'top',
                horizontalAlign: 'right',
                offsetY: "-50px",
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shadeIntensity: 1,
                    inverseColors: false,
                    opacityFrom: 0.4,
                    opacityTo: 0,
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'stepline',
            },
            colors: salesReportColors,
            xaxis: {
                type: 'datetime',
                categories: ["02/01/2023 GMT", "02/02/2023 GMT", "02/03/2023 GMT", "02/04/2023 GMT", "02/05/2023 GMT", "02/06/2023 GMT", "02/07/2023 GMT"]
            },
        };

        if (salesReportChart != "")
            salesReportChart.destroy();
        salesReportChart = new ApexCharts(document.querySelector("#sales_Report"), options);
        salesReportChart.render();
    }

    // Radar Chart - Multi series
    var weeklyVisitorsColors = "";
    weeklyVisitorsColors = getChartColorsArray("weekly_visitors");
    if (weeklyVisitorsColors) {
        var options = {
            series: [{
                name: 'Visitors',
                data: [80, 87, 67, 110, 40, 87],
            },
            {
                name: 'Returning Visitors',
                data: [20, 30, 40, 80, 20, 80],
            }
            ],
            chart: {
                height: 335,
                type: 'radar',
                dropShadow: {
                    enabled: true,
                    blur: 1,
                    left: 1,
                    top: 1
                },
                toolbar: {
                    show: false
                },
            },
            stroke: {
                width: 2
            },
            fill: {
                opacity: 0.2
            },
            markers: {
                size: 0
            },
            colors: weeklyVisitorsColors,
            xaxis: {
                categories: ['2017', '2018', '2019', '2020', '2022', '2023']
            }
        };

        if (weeklyVisitorsChart != "")
            weeklyVisitorsChart.destroy();
        weeklyVisitorsChart = new ApexCharts(document.querySelector("#weekly_visitors"), options);
        weeklyVisitorsChart.render();
    }

    // session_country Charts
    var sessionCountryColors = "";
    sessionCountryColors = getChartColorsArray("session_country");
    if (sessionCountryColors) {
        var options = {
            series: [{
                name: 'Jan',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Feb',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Mar',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Apr',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'May',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Jun',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Jul',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Aug',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            },
            {
                name: 'Nov',
                data: generateData(12, {
                    min: 0,
                    max: 90
                })
            }
            ],
            chart: {
                height: 300,
                type: 'heatmap',
                toolbar: {
                    show: false
                }
            },
            dataLabels: {
                enabled: false
            },
            colors: [sessionCountryColors[0]],
            grid: {
                padding: {
                    top: -22,
                    right: 0,
                    bottom: 0,
                },
            },
            stroke: {
                colors: [sessionCountryColors[1]]
            }
        };
        if (sessionCountryChart != "")
            sessionCountryChart.destroy();
        sessionCountryChart = new ApexCharts(document.querySelector("#session_country"), options);
        sessionCountryChart.render();
    }

    // Generate Data Script

    function generateData(count, yrange) {
        var i = 0;
        var series = [];
        while (i < count) {
            var x = (i + 1).toString();
            var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;

            series.push({
                x: x,
                y: y
            });
            i++;
        }
        return series;
    }

    var data = [{
        name: 'W1',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W2',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W3',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W4',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W5',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W6',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W7',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W8',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W9',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W10',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W11',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W12',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W13',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W14',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'W15',
        data: generateData(8, {
            min: 0,
            max: 90
        })
    }
    ]

    data.reverse()

    // sales_funnel Charts
    var salesFunnelColors = "";
    salesFunnelColors = getChartColorsArray("sales_funnel");
    if (salesFunnelColors) {
        var options = {
            series: [44, 55, 41, 17],
            chart: {
                height: 325,
                type: 'donut',
            },
            labels: ["Prospects", "Leads", "Sales", "Deals"],
            legend: {
                position: 'bottom'
            },
            dataLabels: {
                dropShadow: {
                    enabled: false,
                }
            },
            colors: salesFunnelColors
        };

        if (salesFunnelChart != "")
            salesFunnelChart.destroy();
        salesFunnelChart = new ApexCharts(document.querySelector("#sales_funnel"), options);
        salesFunnelChart.render();
    }

    // team_performance chart
    var teamPerformanceColors = "";
    teamPerformanceColors = getChartColorsArray("team_performance");
    if (teamPerformanceColors) {
        var options = {
            series: [83],
            chart: {
                type: 'radialBar',
                height: 315,
                sparkline: {
                    enabled: true
                },
            },
            plotOptions: {
                radialBar: {
                    startAngle: -90,
                    endAngle: 90,
                    track: {
                        background: "#e7e7e7",
                        strokeWidth: '80%',
                    },
                    dataLabels: {
                        name: {
                            show: false
                        },
                        value: {
                            // show: false,
                            offsetY: -15,
                            fontWeight: 'bold',
                            fontSize: '18px',
                        }
                    }
                }
            },
            grid: {
                padding: {
                    top: -20
                }
            },
            fill: {
                type: 'gradient',
                gradient: {
                    shade: 'light',
                    shadeIntensity: 0.4,
                    inverseColors: false,
                    opacityFrom: 1,
                    opacityTo: 1,
                    stops: [0, 50, 53, 91]
                },
            },
            labels: ['Average Results'],
            colors: teamPerformanceColors
        };

        if (teamPerformanceChart != "")
            teamPerformanceChart.destroy();
        teamPerformanceChart = new ApexCharts(document.querySelector("#team_performance"), options);
        teamPerformanceChart.render();
    }

    // Bubble Charts Generate Data
    function generateBubbleChartData(baseval, count, yrange) {
        var i = 0;
        var series = [];
        while (i < count) {
            var x = Math.floor(Math.random() * (750 - 1 + 1)) + 1;;
            var y = Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min;
            var z = Math.floor(Math.random() * (75 - 15 + 1)) + 15;

            series.push([x, y, z]);
            baseval += 86400000;
            i++;
        }
        return series;
    }

    // Simple Bubble
    var chartBubbleSimpleColors = "";
    chartBubbleSimpleColors = getChartColorsArray("simple_bubble");
    if (chartBubbleSimpleColors) {
        var options = {
            series: [{
                name: 'Users',
                data: generateBubbleChartData(new Date('11 Feb 2017 GMT').getTime(), 20, {
                    min: 10,
                    max: 60
                })
            },
            {
                name: 'Conversation',
                data: generateBubbleChartData(new Date('12 Feb 2017 GMT').getTime(), 20, {
                    min: 10,
                    max: 60
                })
            }
            ],
            chart: {
                height: 300,
                type: 'bubble',
                toolbar: {
                    show: false,
                }
            },
            dataLabels: {
                enabled: false
            },
            fill: {
                opacity: 0.8
            },
            grid: {
                padding: {
                    top: -18
                }
            },
            xaxis: {
                tickAmount: 12,
                type: 'category',
            },
            yaxis: {
                max: 70
            },
            colors: chartBubbleSimpleColors
        };

        if (chartBubbleSimpleChart != "")
            chartBubbleSimpleChart.destroy();
        chartBubbleSimpleChart = new ApexCharts(document.querySelector("#simple_bubble"), options);
        chartBubbleSimpleChart.render();
    }
}

window.addEventListener("resize", function () {
    setTimeout(() => {
        loadCharts();
    }, 250);
});

loadCharts();