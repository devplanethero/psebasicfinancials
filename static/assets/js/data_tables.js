// $(document).ready(function () {
//     $('#company-list').DataTable();
// });


$(document).ready(function () {
    $('#company-list').DataTable({
        initComplete: function () {
            this.api()
                .columns([2])
                .every(function () {
                    var column = this;
                    var select = $('<select><option value=""></option></select>')
                        .appendTo($(column.header()))
                        .on('change', function () {
                            var val = $.fn.dataTable.util.escapeRegex($(this).val());
 
                            column.search(val ? '^' + val + '$' : '', true, false).draw();
                        })
                        .click( function(e) {
                            e.stopPropagation();
                      });
 
                    column
                        .data()
                        .unique()
                        .sort()
                        .each(function (d, j) {
                            select.append('<option value="' + d + '">' + d + '</option>');
                        });
                });
        },
        "oSearch": {"sSearch": searched },
        "iDisplayLength": 25,
    });
});