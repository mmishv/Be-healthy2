function tableSearch() {
    var str = $('input#search').val().toLowerCase();
    if (str.length <= 0) {
        $('table#table-search tbody tr').show();
    } else {
        $('table#table-search tbody tr').each(function () {
            var found = false;
            $(this).find('td.searchable').each(function () {
                if ($(this).text().toLowerCase().indexOf(str) >= 0) {
                    found = true;
                }
            });
            if (found === false) {
                $(this).hide();
            } else {
                $(this).show();
            }
        });
    }
}