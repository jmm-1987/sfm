// filtros_repartos.js

// Filtrar la tabla
function filterTable() {
    const filterEstado = document.getElementById('filterEstado').value.toLowerCase();
    const filterFecha = document.getElementById('filterFecha').value.toLowerCase();
    const filterFechaAsignacion = document.getElementById('filterFechaAsignado').value.toLowerCase();
    const filterAsignado = document.getElementById('filterAsignado').value.toLowerCase();
    const filterFechaEntrega = document.getElementById('filterFechaReparto').value.toLowerCase();

    const rows = document.querySelectorAll('#expedicionTable tbody tr');

    rows.forEach(row => {
        const estado = row.cells[7].textContent.toLowerCase(); // Columna 7: Estado
        const fecha = row.cells[1].textContent.toLowerCase(); // Columna 1: Fecha
        const fechaAsignacion = row.cells[8].textContent.toLowerCase(); // Columna 8: Fecha Asignado
        const asignado = row.cells[9].textContent.toLowerCase(); // Columna 9: Asignado
        const fechaEntrega = row.cells[10].textContent.toLowerCase(); // Columna 10: Fecha Entrega

        if (estado.includes(filterEstado) &&
            fecha.includes(filterFecha) &&
            fechaAsignacion.includes(filterFechaAsignacion) &&
            asignado.includes(filterAsignado) &&
            fechaEntrega.includes(filterFechaEntrega)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

document.querySelectorAll('.p-2.border').forEach(input => {
    input.addEventListener('input', filterTable);
});

// Limpiar los filtros
function clearFilters() {
    document.getElementById('filterEstado').value = "";
    document.getElementById('filterFecha').value = "";
    document.getElementById('filterFechaAsignado').value = "";
    document.getElementById('filterAsignado').value = "";
    document.getElementById('filterFechaReparto').value = "";
    filterTable();
}

// Evento de entrada en los filtros
function setupFilters() {
    document.querySelectorAll('.p-2.border').forEach(input => {
        input.addEventListener('input', filterTable);
    });
}

// Formatear fechas al cargar
function formatDatesOnLoad() {
    const dateCells = document.querySelectorAll("#expedicionTable tbody tr td:nth-child(2), #expedicionTable tbody tr td:nth-child(4), #expedicionTable tbody tr td:nth-child(5)");
    dateCells.forEach(cell => {
        const dateParts = cell.textContent.split("-");
        if (dateParts.length === 3) {
            const formattedDate = `${dateParts[2]}/${dateParts[1]}/${dateParts[0]}`;
            cell.textContent = formattedDate;
        }
    });
}

export { filterTable, clearFilters, setupFilters, formatDatesOnLoad };
