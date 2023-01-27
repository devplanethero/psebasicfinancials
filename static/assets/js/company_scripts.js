    var tbody = document.querySelector('tbody')
    var thead = document.querySelector('thead')
    var table_rows = tbody.querySelectorAll('tr')
    var active_table_values = []
    var active_table_headers = []
    var bar_chart_container = document.querySelector('#bar-chart')

    function create_chart(item){
        let table_headers = thead.querySelectorAll('th')
        var table_row_values = item.querySelectorAll('td')
        var chart_values = Array.from(table_row_values).map(item => parseFloat(item.textContent.replace(/,/g, '')))
        var chart_title = item.querySelector('th').textContent
        var chart_headers = Array.from(table_headers).map(item => item.textContent).filter(item => item != '')

        document.getElementById('chart-title').textContent = chart_title
        active_table_values = chart_values
        active_table_headers = chart_headers
        // new_div = `<div>${chart_values}</div>`
        // var container = document.getElementById('container-top')
        // container.innerHTML += new_div

        chartStatus = Chart.getChart("barChart")
        if (chartStatus != undefined) { // delete previous chart
            chartStatus.destroy()
            document.querySelector("#selector-decorator").remove()
        }

        var financial_chart = new Chart(document.querySelector('#barChart'), {
            type: 'bar',
            data: {
                labels: active_table_headers,
                datasets: [{
                label: chart_title,
                data: active_table_values,
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
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
                }
            }
            });

        item.querySelector('th').innerHTML = `<div class="position-absolute" style="
                                                    top: 0;
                                                    left: 0;
                                                    height: 100%;
                                                    width: 4px;
                                                    background-color: rgb(65, 84, 241);"
                                                id="selector-decorator"></div>` + item.querySelector('th').innerHTML
    }


    // highlight table when clicked
    table_rows.forEach(item => {
        item.addEventListener('click', () => {

            // table_rows.forEach(a=> {
            //     a.classList.remove("table-active")
            // })
            var table_active_status = document.querySelector(".table-active") !== null
            if (table_active_status) {
                document.querySelector(".table-active").classList.remove("table-active")
            }

            item.classList.add("table-active")
            bar_chart_container.classList.remove("collapse")

            create_chart(item)

        })
    })

    function closeChart(){
        bar_chart_container.classList.add("collapse")
    }


    /* --------------------------------------------------
    # STORING VALUES FOR RANGE SLIDERS
    ----------------------------------------------------*/
    var table_headers_El = thead.querySelectorAll('th')
    const table_headers = Array.from(table_headers_El).map(item => item.textContent).filter(item => item != '')
    var table_values = [] //should change if rounded


    var table_contents = tbody.querySelectorAll('tr')
    table_contents.forEach(row => {
        row_contents = row.querySelectorAll('td')
        row_list = Array.from(row_contents).map(cell => cell.textContent)
        table_values.push(row_list)
    })

    /* --------------------------------------------------
    # RANGE SLIDERS
    ----------------------------------------------------*/
    // update the table based on the slider
    function sliceTable(indexFrom, indexTo) {
        indexTo = indexTo // to include last index
        let thead_cells_container = thead.querySelector('tr')
        let denominator = document.querySelector('.selected__unit').value
        //reset table
        thead_cells_container.innerHTML = `<th scope="col" class="text-center text-nowrap table-header"></th>` // first column_header
        tbody.querySelectorAll('tr').forEach(row => {
            row.innerHTML = row.firstElementChild.outerHTML
        })


        table_headers.slice(indexFrom, indexTo).forEach((header, colIndex) => {
            thead_cells_container.innerHTML = thead_cells_container.innerHTML + `<th scope="col" class="text-center text-nowrap table-header">${header}</th>` // column_header

            tbody.querySelectorAll('tr').forEach((row, rowIndex) => {
                let rowVal = table_values[rowIndex].slice(indexFrom, indexTo)[colIndex]
                rowVal = rowVal.replace(/,/g, '')
                if (denominator == '1000000') {
                    rowVal = Math.round(parseFloat(rowVal)/denominator*100)/100 // round based on selected unit
                } else {
                    rowVal = Math.round(parseFloat(rowVal)/denominator) // round based on selected unit
                }
                
                rowVal = rowVal.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',') 
                row.innerHTML = row.innerHTML + `<td class="col-md-1 text-end px-2 table-values">${rowVal}</td>`
            })

        })
    }
    const rangeInput = document.querySelectorAll(".range-input input");
    progress = document.querySelector('.slider .progress');
    sliderTooltip = document.querySelectorAll('.slider__tooltip');
    sliderTooltip[0].querySelector('.label__range').textContent = table_headers[0]
    sliderTooltip[1].querySelector('.label__range').textContent = table_headers[table_headers.length -1]



    rangeInput.forEach(input => {
        input.setAttribute("max", table_headers.length.toString()) //change max value of slider
        if (input.className === 'range-max') {
            input.setAttribute("value", table_headers.length.toString())
        }

        // eventListener for the slider
        input.addEventListener("input", (e)=>{
            var minVal = parseInt(rangeInput[0].value),
            maxVal = parseInt(rangeInput[1].value);

            if (maxVal - minVal < 0){
                if (e.target.className === 'range-min'){
                    rangeInput[0].value = maxVal
                } else {
                    rangeInput[1].value = minVal
                }

            } else {
                progress.style.left = (minVal / rangeInput[0].max) * 100 + "%";
                sliderTooltip[0].style.left = "calc(" + (minVal / rangeInput[0].max) * 100 + "% - 12px)";
                sliderTooltip[0].querySelector('.label__range').textContent = table_headers[minVal]

                progress.style.right = 100 - (maxVal / rangeInput[1].max) * 100 + "%";
                sliderTooltip[1].style.right =  "calc(" + (100 - (maxVal / rangeInput[1].max) * 100 )+ "% - 12px)";
                sliderTooltip[1].querySelector('.label__range').textContent = table_headers[maxVal - 1]

                sliceTable(minVal, maxVal) //update table

                //update chart
                let table_active_status = document.querySelector(".table-active") !== null
                if (table_active_status) {
                    create_chart(document.querySelector(".table-active"))
                }     
            }
        })
        input.addEventListener('mousedown', (e) => {
            sliderTooltip.forEach(tooltip => {
                console.log(tooltip.style.transform)
                tooltip.style.transform = 'scale(1.20)'
            })
        })
        input.addEventListener('mouseup', (e) => {
            sliderTooltip.forEach(tooltip => {
                tooltip.style.transform = 'scale(1)'
            })
        })
    })


    /*-------------------------------------------------
    Table Rounding
    ----------------------------------------------------*/

    const roundingSelection = document.querySelectorAll('.rounding__selection button')

    roundingSelection.forEach(button => {
        button.addEventListener('click', (e) => {
            document.querySelector('.selected__unit').classList.remove('selected__unit')
            button.classList.add('selected__unit')
            let denominator = document.querySelector('.selected__unit').value
            // each row
            tbody.querySelectorAll('tr').forEach((row, rowIndex) => {
                let rowValuesSliced = table_values[rowIndex].slice(parseInt(rangeInput[0].value), parseInt(rangeInput[1].value))

                // each cell in row
                row.querySelectorAll('td').forEach((item, index) => {
                    newItem = rowValuesSliced[index].replace(/,/g, '')
        
                    if (denominator == '1000000') {
                        newItem = Math.round(parseFloat(newItem)/denominator*100)/100 // round based on selected unit
                    } else {
                        newItem = Math.round(parseFloat(newItem)/denominator) // round based on selected unit
                    }
        
                    item.textContent = newItem.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
                })
            })
        
            let table_active_status = document.querySelector(".table-active") !== null
                if (table_active_status) {
                    create_chart(document.querySelector(".table-active"))
                }
        })
    })
