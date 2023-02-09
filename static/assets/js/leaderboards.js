function leaderboardsChartGenerate() {
    var active_year = document.querySelector('#year__selection').value;
    var active_quarter = document.querySelector('.quarter__selection .selected__unit').value;
    var industry_type = encodeURIComponent(document.querySelector('#industry__selection').value);

    // show spinners
    document.querySelectorAll('.spinner__chartloader').forEach(spinner => {
        spinner.classList.remove('not-visible')
    })

    var fetch_url = `${base_url}/api/get-financials/?reporting_period__lt=&reporting_period__gt=&ticker__ticker__iexact=&ticker__type__type__iexact=${industry_type}&quarter__iexact=${active_quarter}&year=${active_year}`;
    fetch(fetch_url)
        .then(res=> {
            return res.json();
        })
        .then(data => {
            //sort based on net income
            data.sort((a,b) => parseFloat(b.Total_Net_Income) - parseFloat(a.Total_Net_Income))
            topTenTotalNetIncome = data.slice(0,10)
            //sort based on net income
            data.sort((a,b) => parseFloat(b.Total_Assets) - parseFloat(a.Total_Assets))
            topTenTotalAssets = data.slice(0,10)
            
            //delete previous chart generated
            document.querySelectorAll("canvas").forEach(canvas => {
                let canvas_id = canvas.getAttribute("id")

                chartStatus = Chart.getChart(canvas_id)
                if (chartStatus != undefined) { // delete previous chart
                    chartStatus.destroy()
                }
            })
            
            // hide spinners
            document.querySelectorAll('.spinner__chartloader').forEach(spinner => {
            spinner.classList.add('not-visible')
            })

            // chart creation
            new Chart(document.querySelector('#barChart_totalAssets'), {
            type: 'bar',
            data: {
                labels: topTenTotalAssets.map(item => item.ticker),
                datasets: [{
                label: 'Total Assets',
                data: topTenTotalAssets.map(item => (Math.round(item.Total_Assets/1000000))),
                backgroundColor: [
                    'rgba(65, 83, 241, 0.6)',
                ],
                borderColor: [
                    'rgba(65, 83, 241, 0.6)',
                ],
                borderWidth: 1
                }]
            },
            options: {
                scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'in M'
                    },
                },
                x: {
                    grid: {
                        display: false
                    }
                },
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            afterTitle: (toolTipAfterTitle) => {
                                let index = toolTipAfterTitle[0].dataIndex
                                return topTenTotalAssets[index].ticker_name
                            }
                        }
                    }
                }
            }
            });
            // end of chart


            // chart creation
            new Chart(document.querySelector('#barChart_netIncome'), {
            type: 'bar',
            data: {
                labels: topTenTotalNetIncome.map(item => item.ticker),
                datasets: [{
                label: 'Total Net Income',
                data: topTenTotalNetIncome.map(item => (Math.round(item.Total_Net_Income/1000000))),
                backgroundColor: [
                    'rgba(65, 83, 241, 0.6)',
                ],
                borderColor: [
                    'rgba(65, 83, 241, 0.6)',
                ],
                borderWidth: 1
                }]
            },
            options: {
                scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'in M'
                    },
                },
                x: {
                    grid: {
                        display: false
                    },
                }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            afterTitle: (toolTipAfterTitle) => {
                                let index = toolTipAfterTitle[0].dataIndex
                                return topTenTotalNetIncome[index].ticker_name
                            }
                        }
                    }
                }
            }
            });
            // end of chart

        })
    }

// industry selection
fetch(`${base_url}/api/get-industries/`)
    .then(res => {
        return res.json()
    })
    .then(data => {
        let industrySelectionContainer = document.querySelector('#industry__selection')
        industrySelectionContainer.innerHTML = ''

        data.forEach(industry => {
            industrySelectionContainer.innerHTML += `<option value="${industry.type}">${industry.type}</option>`
        })
    })

leaderboardsChartGenerate()

/* ------------------------------------------------
# EVENT LISTENERS
-------------------------------------------------*/
// Quarter
document.querySelectorAll('.quarter__selection button').forEach(button => {
    button.addEventListener('click', (e) => {
        document.querySelector('.quarter__selection .selected__unit').classList.remove('selected__unit')
        button.classList.add('selected__unit')
        leaderboardsChartGenerate()
    })
})

// Year
document.querySelector('#year__selection').addEventListener('change', (e) => {
    if (e.target.value !== '2022') {
        document.querySelector('.quarter__selection .disabled').classList.remove('disabled')
    } else {
        document.querySelector('.quarter__selection #period_q4').classList.add('disabled')
    }
    leaderboardsChartGenerate()
})

document.querySelector('#industry__selection').addEventListener('change', (e) => {
    document.querySelector('.industry__title').textContent = document.querySelector('#industry__selection').value
    leaderboardsChartGenerate()
})