document.addEventListener('DOMContentLoaded', function () {
    new DataTable('#data-table', {
        paging: true,
        searching: true,
        ordering: true,
        info: true,
        pageLength: 10
    });
});