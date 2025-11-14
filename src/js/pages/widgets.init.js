/*
Template Name: Judia - Admin & Dashboard Template
Author: Themesbrand
Website: https://Themesbrand.com/
Contact: Themesbrand@gmail.com
File: Widgets init js
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
var realTimeSalesChart = "";
var salesReportChart = "";
var syncStatusBreakdownChart = "";
var realizedRateChart = "";
var emailSentChart = "";
function loadCharts() {

    // Average daily sales chart
    var averageDailySalesColors = "";
    averageDailySalesColors = getChartColorsArray("average_daily_sales");
    if (averageDailySalesColors) {
        var options = {
            series: [76],
            chart: {
                type: 'radialBar',
                height: 260,
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
                height: 300,
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

    //  sales_Report Charts
    var salesReportColors = '';
    salesReportColors = getChartColorsArray("sales_Report");
    if (salesReportColors) {
        var options = {
            series: [{
                name: 'This Month',
                data: [45, 74, 36, 69, 84, 110, 92]
            }, {
                name: 'Last Month',
                data: [11, 18, 20, 32, 46, 65, 73]
            }],
            chart: {
                height: 333,
                type: 'area',
                toolbar: {
                    show: false
                }
            },
            grid: {
                padding: {
                    top: 0,
                    right: 2,
                    bottom: 0,
                },
            },
            legend: {
                show: true,
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
            yaxis: {
                labels: {
                    show: true,
                    formatter: function (y) {
                        return y.toFixed(0) + "k";
                    }
                },
            },
        };

        if (salesReportChart != "")
            salesReportChart.destroy();
        salesReportChart = new ApexCharts(document.querySelector("#sales_Report"), options);
        salesReportChart.render();
    }

    // syncStatusBreakdown Charts
    var syncStatusBreakdownColors = "";
    syncStatusBreakdownColors = getChartColorsArray("syncStatusBreakdown");
    if (syncStatusBreakdownColors) {
        var options = {
            series: [{
                name: 'Synced',
                data: [44, 55, 41, 37, 22, 43, 21]
            }, {
                name: 'Sync Needed',
                data: [53, 32, 33, 52, 13, 43, 32]
            }, {
                name: 'Never Synced',
                data: [12, 17, 11, 9, 15, 11, 20]
            }, {
                name: 'Review Needed',
                data: [9, 7, 5, 8, 6, 9, 4]
            }],
            chart: {
                type: 'bar',
                height: 365,
                stacked: true,
                toolbar: {
                    show: false,
                }
            },
            plotOptions: {
                bar: {
                    horizontal: true,
                    columnHight: '40%',
                },
            },
            grid: {
                show: true,
                padding: {
                    top: -20,
                    right: 0,
                    bottom: -10,
                },
            },
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
            },
            yaxis: {
                title: {
                    text: undefined
                },
            },
            fill: {
                opacity: 1
            },
            legend: {
                show: false,
            },
            colors: syncStatusBreakdownColors
        };

        if (syncStatusBreakdownChart != "")
            syncStatusBreakdownChart.destroy();
        syncStatusBreakdownChart = new ApexCharts(document.querySelector("#syncStatusBreakdown"), options);
        syncStatusBreakdownChart.render();
    }

    // realized_rate charts
    var realizedRateColors = "";
    realizedRateColors = getChartColorsArray("realized_rate");
    if (realizedRateColors) {
        var options = {
            series: [{
                name: 'Read',
                data: [80, 50, 30, 40, 100, 20],
            },
            {
                name: 'Delivery',
                data: [20, 30, 40, 80, 20, 80],
            },
            {
                name: 'Failed',
                data: [44, 76, 78, 13, 43, 10],
            }
            ],
            chart: {
                height: 308,
                type: 'radar',
                toolbar: {
                    show: false
                },
            },
            stroke: {
                width: 1
            },
            fill: {
                opacity: 0.2
            },
            markers: {
                size: 3,
                hover: {
                    size: 4,
                }
            },
            tooltip: {
                y: {
                    formatter: function (val) {
                        return val
                    }
                }
            },
            colors: realizedRateColors,
            xaxis: {
                categories: ['2018', '2019', '2020', '2021', '2022', '2023'],
            }
        };

        if (realizedRateChart != "")
            realizedRateChart.destroy();
        realizedRateChart = new ApexCharts(document.querySelector("#realized_rate"), options);
        realizedRateChart.render();
    }

    // emailSent Bar
    var emailSentColors = "";
    emailSentColors = getChartColorsArray("emailSent");
    if (emailSentColors) {
        var options = {
            series: [63, 87, 33],
            chart: {
                height: 400,
                type: 'radialBar',
            },
            plotOptions: {
                radialBar: {
                    track: {
                        background: emailSentColors,
                        opacity: 0.15,
                    },
                    dataLabels: {
                        name: {
                            fontSize: '22px',
                        },
                        value: {
                            fontSize: '16px',
                        },
                        total: {
                            show: true,
                            label: 'Total',
                            formatter: function (w) {
                                return 1793
                            }
                        }
                    },
                }
            },
            legend: {
                show: true,
                position: 'bottom',
            },
            labels: ['Sent', 'Received', 'Failed'],
            colors: emailSentColors
        };

        if (emailSentChart != "")
            emailSentChart.destroy();
        emailSentChart = new ApexCharts(document.querySelector("#emailSent"), options);
        emailSentChart.render();
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
}
// Reload charts on the theme change or resize browser
window.addEventListener("resize", function () {
    setTimeout(() => {
        loadCharts();
    }, 250);
});

loadCharts();

//Browser Usage Table
var options = {
    valueNames: [
        "browsers",
        "click",
        "pageviews"
    ],
};
var contactList = new List("networks", options)

// sortble-dropdown
var sorttableDropdown = document.querySelectorAll('.sortble-dropdown');
if (sorttableDropdown) {
    sorttableDropdown.forEach(function (elem) {
        elem.querySelectorAll('.dropdown-menu .dropdown-item').forEach(function (item) {
            item.addEventListener('click', function () {
                elem.querySelector('.dropdown-title').innerHTML = item.innerHTML;
            });
        });
    });
}