var indicator = document.querySelector('#economy-nav a.active').dataset.value
var thead = document.querySelector('thead tr')
var tbody = document.querySelector('tbody')
var countrySelection = document.querySelector('.country_selection')
var removed_datasets = []
var lineChartColors = [
    '#00bfa0',
    '#003f5c',
    '#2f4b7c',
    '#665191',
    '#a05195',
    '#d45087',
    '#f95d6a',
    '#f95d6a',
    '#ff7c43',
    '#ffa600'
]

// chart config
var lineChart = new Chart(document.querySelector('#lineChart'), {
    type: 'line',
    data: {
        labels: [],
        datasets:[]
        },
    options: {
        maintainAspectRatio: false,
        scales: {
        y: {
            beginAtZero: true,
            grid: {
                display: true
            },
            title: {
                display: true,
                text: 'Rate'
            },
        },
        x: {
            grid: {
                display: false
            }
        },
        },
    }
    });
    // end of chart

const economics_data = async(indicator) => {

    //get countries
    let countryRes = await fetch(`${base_url}/api/countries-list/`)
    let countriesArray = await countryRes.json() 

    let i = 0
    for (const countryDetails of countriesArray) {
        econ_indicator = indicator
        country = countryDetails.name

        let fetch_url = `${base_url}/api/economy_records/?country__name__iexact=${country}&economic_indicator__title__iexact=${econ_indicator}&quarter__iexact=&year=`

        let response = await fetch(fetch_url)
        let economics_data = await response.json()
        if (i === 0){
            let periods = economics_data.map(item => item.period)
            lineChart.data.labels = periods
            // set table_headers
            periods.forEach(item => {
                thead.innerHTML += `<th scope="col" class="text-center text-nowrap table-header">${item}</th>`
            })
            
        } // set labels
        
        var dataset = {
            label: country,
            data: economics_data.map(item => {
                if (item.value == 0){
                    return "N/A"
                } else {
                    return item.value
                }
            }),
            backgroundColor: lineChartColors[i],
            borderColor: lineChartColors[i],
            borderWidth: 2,
            fill: false
            }
        

        // push datasets to chart
        lineChart.data.datasets.push(dataset)
        lineChart.update()

        // table_values
        tbody.innerHTML += `<tr>
                                <th scope="row" class="text-nowrap ps-2"><span id="table_first_col">${country}</span></th>
                                ${economics_data.map(item => {
                                    return '<td class="col-md-1 text-end px-2 table-values">'+ item.value +'</td>'
                                }).join("")}
                            </tr>`
        // country checkbox
        countrySelection.innerHTML += `<div class="form-check form-check-inline">
                                        <input class="form-check-input" type="checkbox" id="${country}_checkbox" value="${country}" checked onchange="addRemoveData('${country}')">
                                        <label class="form-check-label" for="${country}_checkbox">${country}</label>
                                    </div>
      `
        
        i++
        } // end of countries array loop
    
    // hide spinners
    document.querySelectorAll('.spinner__chartloader').forEach(spinner => {
        spinner.classList.add('not-visible')
        })
    }


function addRemoveData(country) {
    let array = lineChart.data.datasets.map((dataset, index) => {
        return dataset.label
    })
    
    let position = array.indexOf(country)
    if(position > -1) {
        removed_datasets.push(lineChart.data.datasets[position])
        lineChart.data.datasets.splice(position, 1)
        lineChart.update()
    } else {
        position_removed = removed_datasets.map(dataset => dataset.label).indexOf(country)
        lineChart.data.datasets.push(removed_datasets[position_removed]) 
        lineChart.update()
    }

    
}

economics_data(indicator)

