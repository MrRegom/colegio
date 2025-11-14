/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Ecommerce Dashboard init js
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

var totalRevenueChart = "";
var totalEarningsChart = "";
var averageDailySalesChart = "";
var totalOrdersChart = "";
var revenueOverviewChart = "";
var realTimeSalesChart = "";
var salesTrafficSourceChart = "";
var onlineStoreChart = "";
var chartBarChart = "";

function loadCharts() {
    
    // Average daily sales chart
    var averageDailySalesColors = "";
    averageDailySalesColors = getChartColorsArray("average_daily_sales");
    if (averageDailySalesColors) {
        var options = {
            series: [76],
            chart: {
                type: 'radialBar',
                height: 220,
                // offsetY: -20,
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
                    top: -35
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
            colors: averageDailySalesColors
        };

        if (averageDailySalesChart != "")
            averageDailySalesChart.destroy();
        averageDailySalesChart = new ApexCharts(document.querySelector("#average_daily_sales"), options);
        averageDailySalesChart.render();
    }

    // Total Revenue chart
    var totalRevenueColors = "";
    totalRevenueColors = getChartColorsArray("total_revenue");
    if (totalRevenueColors) {
        var options1 = {
            series: [{
                data: [24, 43, 51, 66, 49, 33, 48, 66]
            }],
            chart: {
                type: 'line',
                height: 70,
                sparkline: {
                    enabled: true
                }
            },
            colors: totalRevenueColors,
            stroke: {
                curve: 'smooth',
                width: 2,
            },
            tooltip: {
                fixed: {
                    enabled: false
                },
                x: {
                    show: false
                },
                y: {
                    title: {
                        formatter: function (seriesName) {
                            return ''
                        }
                    }
                },
                marker: {
                    show: false
                }
            }
        };

        if (totalRevenueChart != "")
            totalRevenueChart.destroy();
        totalRevenueChart = new ApexCharts(document.querySelector("#total_revenue"), options1);
        totalRevenueChart.render();
    }

    // Total earnings chart
    var totalEarningsColors = "";
    totalEarningsColors = getChartColorsArray("total_earnings");
    if (totalEarningsColors) {
        var options = {
            series: [{
                name: 'Total Earnings',
                data: [0.7, 1.0, 0.8, 1.4, 2.3, 3.2, 3.6, 4.0, 5.1, 4.0, 3.1, 4.3]
            }],
            chart: {
                height: 70,
                type: 'bar',
                toolbar: {
                    show: false,
                },
                sparkline: {
                    enabled: true
                }
            },
            xaxis: {
                categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            },
            colors: totalEarningsColors,
            yaxis: {
                labels: {
                    show: false,
                    formatter: function (val) {
                        return val + "k";
                    }
                }
            },
        };

        if (totalEarningsChart != "")
            totalEarningsChart.destroy();
        totalEarningsChart = new ApexCharts(document.querySelector("#total_earnings"), options);
        totalEarningsChart.render();
    }

    // Total orders chart
    var totalOrdersColors = "";
    totalOrdersColors = getChartColorsArray("total_orders");
    if (totalOrdersColors) {
        var options1 = {
            series: [{
                data: [36, 21, 45, 53, 39, 55, 67, 58]
            }],
            chart: {
                type: 'line',
                height: 70,
                sparkline: {
                    enabled: true
                }

            },
            colors: totalOrdersColors,
            stroke: {
                curve: 'stepline',
                width: 2,
            },
            tooltip: {
                fixed: {
                    enabled: false
                },
                x: {
                    show: false
                },
                y: {
                    title: {
                        formatter: function (seriesName) {
                            return ''
                        }
                    }
                },
                marker: {
                    show: false
                }
            }
        };

        if (totalOrdersChart != "")
            totalOrdersChart.destroy();
        totalOrdersChart = new ApexCharts(document.querySelector("#total_orders"), options1);
        totalOrdersChart.render();
    }

    // Real time sales Chart
    var realTimeSalesColors = "";
    realTimeSalesColors = getChartColorsArray("real_time_sales");
    if (realTimeSalesColors) {
        var options = {
            chart: {
                height: 275,
                type: 'bar',
                stacked: true,
                toolbar: {
                    show: false,
                }
            },
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '45%',
                    endingShape: 'rounded'
                },
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                show: true,
                width: 1,
                colors: ['transparent']
            },
            legend: {
                show: false,
            },
            series: [{
                name: 'Search Engine Traffic',
                data: [74, 83, 89, 97, 97, 97, 74]
            }, {
                name: 'Direct Traffic',
                data: [46, 57, 59, 54, 97, 97, 84]
            }],
            colors: realTimeSalesColors,
            xaxis: {
                categories: ['Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'],
            },
            yaxis: {
                show: true,
            },
            grid: {
                show: true,
                padding: {
                    right: 0,
                },
                borderColor: '#000',
                xaxis: {
                    lines: {
                        show: true
                    }
                },
                yaxis: {
                    lines: {
                        show: false
                    }
                },
            },
        }

        if (realTimeSalesChart != "")
            realTimeSalesChart.destroy();
        realTimeSalesChart = new ApexCharts(document.querySelector("#real_time_sales"), options);
        realTimeSalesChart.render();
    }

    // world map with line & markers
    var vectorMapWorldLineColors = getChartColorsArray("world-map-line-markers");
    if (vectorMapWorldLineColors) {
        document.getElementById("world-map-line-markers").innerHTML = "";
        var worldlinemap = new jsVectorMap({
            map: "world_merc",
            selector: "#world-map-line-markers",
            zoomOnScroll: false,
            zoomButtons: false,
            markers: [{
                name: "Greenland",
                coords: [72, -42]
            },
            {
                name: "Canada",
                coords: [56.1304, -106.3468],
            },
            {
                name: "Brazil",
                coords: [-14.2350, -51.9253]
            },
            {
                name: "Serbia",
                coords: [44.0165, 21.0059]
            },
            {
                name: "Russia",
                coords: [61, 105]
            },
            {
                name: "United States",
                coords: [37.0902, -95.7129]
            },],
            regionStyle: {
                initial: {
                    stroke: "#9599ad",
                    strokeWidth: 0.25,
                    fill: vectorMapWorldLineColors,
                    fillOpacity: 1,
                },
            },
            labels: {
                markers: {
                    render(marker, index) {
                        return marker.name || marker.labelName || 'Not available'
                    }
                }
            },
        });
    }

    //revenue overview
    var revenueOverviewColors = "";
    revenueOverviewColors = getChartColorsArray("revenue_overview");
    if (revenueOverviewColors) {
        var options = {
            series: [{
                name: 'Total Revenue',
                type: 'area',
                data: [
                    [1346277600000, 31.46],
                    [1346364000000, 31.27],
                    [1346709600000, 31.43],
                    [1346796000000, 32.26],
                    [1346882400000, 32.79],
                    [1346968800000, 32.46],
                    [1347228000000, 32.13],
                    [1347314400000, 32.43],
                    [1347400800000, 32.42],
                    [1347487200000, 32.81],
                    [1347573600000, 33.34],
                    [1347832800000, 33.41],
                    [1347919200000, 32.57],
                    [1348005600000, 33.12],
                    [1348092000000, 34.53],
                    [1348178400000, 33.83],
                    [1348437600000, 33.41],
                    [1348524000000, 32.90],
                    [1348610400000, 32.53],
                    [1348696800000, 32.80],
                    [1348783200000, 32.44],
                    [1349042400000, 32.62],
                    [1349128800000, 32.57],
                    [1349215200000, 32.60],
                    [1349301600000, 32.68],
                    [1349388000000, 32.47],
                    [1349647200000, 32.23],
                    [1349733600000, 31.68],
                    [1349820000000, 31.51],
                    [1349906400000, 31.78],
                    [1349992800000, 31.94],
                    [1350252000000, 32.33],
                    [1350338400000, 33.24],
                    [1350424800000, 33.44],
                    [1350511200000, 33.48],
                    [1350597600000, 33.24],
                    [1350856800000, 33.49],
                    [1350943200000, 33.31],
                    [1351029600000, 33.36],
                    [1351116000000, 33.40],
                    [1351202400000, 34.01],
                    [1351638000000, 34.02],
                    [1351724400000, 34.36],
                    [1351810800000, 34.39],
                    [1352070000000, 34.24],
                    [1352156400000, 34.39],
                    [1352242800000, 33.47],
                    [1352329200000, 32.98],
                    [1352415600000, 32.90],
                    [1352674800000, 32.70],
                    [1352761200000, 32.54],
                    [1352847600000, 32.23],
                    [1352934000000, 32.64],
                    [1353020400000, 32.65],
                    [1353279600000, 32.92],
                    [1353366000000, 32.64],
                    [1353452400000, 32.84],
                    [1353625200000, 33.40],
                    [1353884400000, 33.30],
                    [1353970800000, 33.18],
                    [1354057200000, 33.88],
                    [1354143600000, 34.09],
                    [1354230000000, 34.61],
                    [1354489200000, 34.70],
                    [1354575600000, 35.30],
                    [1354662000000, 35.40],
                    [1354748400000, 35.14],
                    [1354834800000, 35.48],
                    [1355094000000, 35.75],
                    [1355180400000, 35.54],
                    [1355266800000, 35.96],
                    [1355353200000, 35.53],
                    [1355439600000, 37.56],
                    [1355698800000, 37.42],
                    [1355785200000, 37.49],
                    [1355871600000, 38.09],
                    [1355958000000, 37.87],
                    [1356044400000, 37.71],
                    [1356303600000, 37.53],
                    [1356476400000, 37.55],
                    [1356562800000, 37.30],
                    [1356649200000, 36.90],
                    [1356908400000, 37.68],
                    [1357081200000, 38.34],
                    [1357167600000, 37.75],
                    [1357254000000, 38.13],
                    [1357513200000, 37.94],
                    [1357599600000, 38.14],
                    [1357686000000, 38.66],
                    [1357772400000, 38.62],
                    [1357858800000, 38.09],
                    [1358118000000, 38.16],
                    [1358204400000, 38.15],
                    [1358290800000, 37.88],
                    [1358377200000, 37.73],
                    [1358463600000, 37.98],
                    [1358809200000, 37.95],
                    [1358895600000, 38.25],
                    [1358982000000, 38.10],
                    [1359068400000, 38.32],
                    [1359327600000, 38.24],
                    [1359414000000, 38.52],
                    [1359500400000, 37.94],
                    [1359586800000, 37.83],
                    [1359673200000, 38.34],
                    [1359932400000, 38.10],
                    [1360018800000, 38.51],
                    [1360105200000, 38.40],
                    [1360191600000, 38.07],
                    [1360278000000, 39.12],
                    [1360537200000, 38.64],
                    [1360623600000, 38.89],
                    [1360710000000, 38.81],
                    [1360796400000, 38.61],
                    [1360882800000, 38.63],
                    [1361228400000, 38.99],
                    [1361314800000, 38.77],
                    [1361401200000, 38.34],
                    [1361487600000, 38.55],
                    [1361746800000, 38.11],
                    [1361833200000, 38.59],
                    [1361919600000, 39.60],
                ]
            }, {
                name: 'Total Earnings',
                type: 'line',
                data: [
                    [1346277600000, 39.60],
                    [1346364000000, 38.59],
                    [1346709600000, 38.11],
                    [1346796000000, 38.55],
                    [1346882400000, 38.34],
                    [1346968800000, 38.77],
                    [1347228000000, 38.99],
                    [1347314400000, 38.63],
                    [1347400800000, 38.61],
                    [1347487200000, 38.81],
                    [1347573600000, 38.89],
                    [1347832800000, 38.64],
                    [1347919200000, 39.12],
                    [1348005600000, 38.07],
                    [1348092000000, 38.40],
                    [1348178400000, 38.51],
                    [1348437600000, 38.10],
                    [1348524000000, 38.34],
                    [1348610400000, 37.83],
                    [1348696800000, 37.94],
                    [1348783200000, 38.52],
                    [1349042400000, 38.24],
                    [1349128800000, 38.32],
                    [1349215200000, 38.10],
                    [1349301600000, 38.25],
                    [1349388000000, 37.95],
                    [1349647200000, 37.98],
                    [1349733600000, 37.73],
                    [1349820000000, 37.88],
                    [1349906400000, 38.15],
                    [1349992800000, 38.16],
                    [1350252000000, 38.09],
                    [1350338400000, 38.62],
                    [1350424800000, 38.66],
                    [1350511200000, 38.14],
                    [1350597600000, 37.94],
                    [1350856800000, 38.13],
                    [1350943200000, 37.75],
                    [1351029600000, 38.34],
                    [1351116000000, 37.68],
                    [1351202400000, 36.90],
                    [1351638000000, 37.30],
                    [1351724400000, 37.55],
                    [1351810800000, 37.53],
                    [1352070000000, 37.71],
                    [1352156400000, 37.87],
                    [1352242800000, 38.09],
                    [1352329200000, 37.49],
                    [1352415600000, 37.42],
                    [1352674800000, 37.56],
                    [1352761200000, 35.53],
                    [1352847600000, 35.96],
                    [1352934000000, 35.54],
                    [1353020400000, 35.75],
                    [1353279600000, 35.48],
                    [1353366000000, 35.14],
                    [1353452400000, 35.40],
                    [1353625200000, 35.30],
                    [1353884400000, 34.70],
                    [1353970800000, 34.61],
                    [1354057200000, 34.09],
                    [1354143600000, 33.88],
                    [1354230000000, 33.18],
                    [1354489200000, 33.30],
                    [1354575600000, 33.40],
                    [1354662000000, 32.84],
                    [1354748400000, 32.64],
                    [1354834800000, 32.92],
                    [1355094000000, 32.65],
                    [1355180400000, 32.64],
                    [1355266800000, 32.23],
                    [1355353200000, 32.54],
                    [1355439600000, 32.70],
                    [1355698800000, 32.90],
                    [1355785200000, 32.98],
                    [1355871600000, 33.47],
                    [1355958000000, 34.39],
                    [1356044400000, 34.24],
                    [1356303600000, 34.39],
                    [1356476400000, 34.36],
                    [1356562800000, 34.02],
                    [1356649200000, 34.01],
                    [1356908400000, 33.40],
                    [1357081200000, 33.36],
                    [1357167600000, 33.31],
                    [1357254000000, 33.49],
                    [1357513200000, 33.24],
                    [1357599600000, 33.48],
                    [1357686000000, 33.44],
                    [1357772400000, 33.24],
                    [1357858800000, 32.33],
                    [1358118000000, 31.94],
                    [1358204400000, 31.78],
                    [1358290800000, 31.51],
                    [1358377200000, 31.68],
                    [1358463600000, 32.23],
                    [1358809200000, 32.47],
                    [1358895600000, 32.68],
                    [1358982000000, 32.60],
                    [1359068400000, 32.57],
                    [1359327600000, 32.62],
                    [1359414000000, 32.44],
                    [1359500400000, 32.80],
                    [1359586800000, 32.53],
                    [1359673200000, 32.90],
                    [1359932400000, 33.41],
                    [1360018800000, 34.53],
                    [1360105200000, 33.12],
                    [1360191600000, 32.57],
                    [1360278000000, 33.41],
                    [1360537200000, 35.34],
                    [1360623600000, 37.89],
                    [1360710000000, 38.81],
                    [1360796400000, 38.61],
                    [1360882800000, 37.63],
                    [1361228400000, 38.99],
                    [1361314800000, 38.77],
                    [1361401200000, 38.34],
                    [1361487600000, 38.55],
                    [1361746800000, 34.43],
                    [1361833200000, 37.27],
                    [1361919600000, 35.46],
                ]
            }],
            chart: {
                id: 'area-datetime',
                type: 'line',
                height: 300,
                toolbar: {
                    show: false
                },
                zoom: {
                    autoScaleYaxis: true
                }
            },

            stroke: {
                width: 2,
            },
            colors: revenueOverviewColors,
            grid: {
                xaxis: {
                    lines: {
                        show: false
                    }
                },
                yaxis: {
                    lines: {
                        show: false
                    }
                },
                padding: {
                    right: 0
                }
            },
            yaxis: {
                tickAmount: 4,
                min: 25,
                max: 45,
                labels: {
                    formatter: function (val) {
                        return val + "k";
                    }
                }
            },
            legend: {
                position: 'top',
                horizontalAlign: 'center',
            },
            dataLabels: {
                enabled: false
            },
            markers: {
                size: 0,
                style: 'hollow',
            },
            xaxis: {
                type: 'datetime',
                min: new Date('01 Sep 2012').getTime(),
                tickAmount: 6,
            },
            tooltip: {
                x: {
                    format: 'dd MMM yyyy'
                }
            },
            fill: {
                type: ['gradient', 'solid'],
                gradient: {
                    type: "vertical",
                    shade: 'light',
                    shadeIntensity: 1,
                    inverseColors: false,
                    opacityFrom: 0.3,
                    opacityTo: 0.1,
                    stops: [0, 100]
                },
            },
        };

        if (revenueOverviewChart != "")
            revenueOverviewChart.destroy();
        revenueOverviewChart = new ApexCharts(document.querySelector("#revenue_overview"), options);
        revenueOverviewChart.render();
    }

    var resetCssClasses = function (activeEl) {
        var els = document.querySelectorAll('button')
        Array.prototype.forEach.call(els, function (el) {
            el.classList.remove('active')
        })

        activeEl.target.classList.add('active')
    }

    document.querySelector('#one_month').addEventListener('click', function (e) {
        resetCssClasses(e)
        revenueOverviewChart.zoomX(
            new Date('28 Jan 2013').getTime(),
            new Date('27 Feb 2013').getTime()
        )
    });

    document.querySelector('#three_months').addEventListener('click', function (e) {
        resetCssClasses(e)
        revenueOverviewChart.zoomX(
            new Date('01 Dec 2012').getTime(),
            new Date('27 Feb 2013').getTime()
        )
    });

    document.querySelector('#six_months').addEventListener('click', function (e) {
        resetCssClasses(e)
        revenueOverviewChart.zoomX(
            new Date('01 Sep 2012').getTime(),
            new Date('27 Feb 2013').getTime()
        )
    });


    document.querySelector('#all').addEventListener('click', function (e) {
        resetCssClasses(e)
        revenueOverviewChart.zoomX(
            new Date('29 Aug 2012').getTime(),
            new Date('27 Feb 2013').getTime()
        )
    })

    // sales_traffic_source
    var salesTrafficSourceColors = "";
    salesTrafficSourceColors = getChartColorsArray("sales_traffic_source");
    if (salesTrafficSourceColors) {
        var options = {
            series: [59, 40, 44, 31],
            labels: ["Facebook", "Instagram", "YouTube", "Google Ads"],
            chart: {
                height: 267,
                type: 'donut',
            },
            legend: {
                show: false
            },
            dataLabels: {
                dropShadow: {
                    enabled: false,
                }
            },
            colors: salesTrafficSourceColors
        };

        if (salesTrafficSourceChart != "")
            salesTrafficSourceChart.destroy();
        salesTrafficSourceChart = new ApexCharts(document.querySelector("#sales_traffic_source"), options);
        salesTrafficSourceChart.render();
    }

    //  online_store Charts
    var onlineStoreColors = "";
    onlineStoreColors = getChartColorsArray("online_store");
    if (onlineStoreColors) {
        var options = {
            series: [{
                name: "Desktops",
                data: [10, 41, 35, 51, 49, 62]
            }],
            chart: {
                height: 290,
                type: 'line',
                zoom: {
                    enabled: false
                },
                toolbar: {
                    show: false
                }
            },
            markers: {
                size: 4,
            },
            dataLabels: {
                enabled: false
            },
            stroke: {
                curve: 'smooth'
            },
            colors: onlineStoreColors,
            xaxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
            }
        };

        if (onlineStoreChart != "")
            onlineStoreChart.destroy();
        onlineStoreChart = new ApexCharts(document.querySelector("#online_store"), options);
        onlineStoreChart.render();
    }

    // Basic Bar chart
    var chartBarColors = "";
    chartBarColors = getChartColorsArray("bar_chart");
    if (chartBarColors) {
        var options = {
            chart: {
                height: 140,
                type: 'bar',
                toolbar: {
                    show: false,
                }
            },
            plotOptions: {
                bar: {
                    horizontal: true,
                }
            },
            dataLabels: {
                enabled: false
            },
            series: [{
                name: 'Income & Expenses',
                data: [599, 510]
            }],
            labels: ['Income', 'Expense'],
            colors: chartBarColors,
            grid: {
                padding: {
                    top: -20,
                    right: 0,
                }
            },
            xaxis: {
                categories: ['Income', 'Expense'],
            }
        }

        if (chartBarChart != "")
            chartBarChart.destroy();
        chartBarChart = new ApexCharts(document.querySelector("#bar_chart"), options);
        chartBarChart.render();
    }
}

window.addEventListener("resize", function () {
    setTimeout(() => {
        loadCharts();
    }, 250);
});

loadCharts();

//Product Launch Widgets
document.addEventListener('DOMContentLoaded', function () {
    var mainArray = Array.from(document.querySelectorAll(".launch-widgets"))
    mainArray.forEach(function (item) {
        var countdownVal = new Date().getTime() + 10000; // item.getAttribute("data-countdown") // You may use specific date for long duration of coming soon time.

        // Set the date we're counting down to
        var countDownDate = new Date(countdownVal).getTime();

        // Update the count down every 1 second
        var countDown = setInterval(function () {
            // Get today's date and time
            var currentTime = new Date().getTime();
            // Find the distance between currentTime and the count down date
            var distance = countDownDate - currentTime;

            // Time calculations for days, hours, minutes and seconds
            var days = Math.floor(distance / (1000 * 60 * 60 * 24));
            var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            var seconds = Math.floor((distance % (1000 * 60)) / 1000);

            var countDownBlock = '<div class="countdownlist-item">' +
                '<div class="count-title">Days</div>' + '<div class="count-num">' + days + '</div>' +
                '</div>' +
                '<div class="countdownlist-item">' +
                '<div class="count-title">Hours</div>' + '<div class="count-num">' + hours + '</div>' +
                '</div>' +
                '<div class="countdownlist-item">' +
                '<div class="count-title">Minutes</div>' + '<div class="count-num">' + minutes + '</div>' +
                '</div>' +
                '<div class="countdownlist-item">' +
                '<div class="count-title">Seconds</div>' + '<div class="count-num">' + seconds + '</div>' +
                '</div>';

            // Output the result in an element with id="countDownBlock"
            if (item) {
                item.innerHTML = countDownBlock;
            }
            // If the count down is over, write some text 
            if (distance < 0) {
                clearInterval(countDown);
                document.getElementById("countDownText").innerHTML = `<div class="card-body text-center">
                <div">
                    <div class="my-5 pt-3">
                        <img src="/static/images/comingsoon.png" alt="" style="max-height: 181px;">
                    </div>
                    <h5 class="text-white pt-4 text-xl">We've Launched your Product</h5>
                    <p class="text-white text-opacity-50">Click the below button to view your product.</p>
                    <a href="index.html" class="text-white icon-link icon-link-hover mt-1">View Product <i class="bi bi-arrow-right"></i></a>
                </div>
            </div>`;
            }
        }, 1000);
    })
});

//Orders Table
var options = {
    valueNames: [
        "order_date",
        "order_id",
        "shop",
        "customer",
        "products",
        "amount",
        "status",
        "rating"
    ],
};

// Init list
var contactList = new List("contactList", options).on("updated", function (list) {
    list.matchingItems.length == 0 ?
        (document.getElementsByClassName("noresult")[0].style.display = "block") :
        (document.getElementsByClassName("noresult")[0].style.display = "none");

    if (list.matchingItems.length > 0) {
        document.getElementsByClassName("noresult")[0].style.display = "none";
    } else {
        document.getElementsByClassName("noresult")[0].style.display = "block";
    }
});

// sortble-dropdown
var sorttableDropdown = document.querySelectorAll('.sortble-dropdown');
if (sorttableDropdown) {
    sorttableDropdown.forEach(function (elem) {
        elem.querySelectorAll('.dropdown-menu .dropdown-item').forEach(function (item) {
            item.addEventListener('click', function () {
                var getHtml = item.innerHTML;
                elem.querySelector('.dropdown-title').innerHTML = getHtml;
            });
        });
    });
}