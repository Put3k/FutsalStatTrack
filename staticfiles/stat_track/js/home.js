// // Create <script> element and set its attributes
// var script = document.createElement('script');
// script.src = "https://code.jquery.com/jquery-3.6.0.min.js";

function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("playersList");
  switching = true;
  dir = "asc";

  while (switching) {
    switching = false;
    rows = table.rows;

    for (i = 1; i < (rows.length - 1); i++) {
      shouldSwitch = false;
      x = rows[i].getElementsByTagName("TD")[n].innerText;
      y = rows[i + 1].getElementsByTagName("TD")[n].innerText;

      // Check data type
      if (!isNaN(parseFloat(x)) && !isNaN(parseFloat(y))) {
        // If both are numbers compare as float
        if (dir === "asc") {
          if (parseFloat(x) > parseFloat(y)) {
            shouldSwitch = true;
            break;
          }
        } else if (dir === "desc") {
          if (parseFloat(x) < parseFloat(y)) {
            shouldSwitch = true;
            break;
          }
        }
      } else if (!isNaN(parseInt(x)) && !isNaN(parseInt(y))) {
        // If both are integer compare as int
        if (dir === "asc") {
          if (parseInt(x) > parseInt(y)) {
            shouldSwitch = true;
            break;
          }
        } else if (dir === "desc") {
          if (parseInt(x) < parseInt(y)) {
            shouldSwitch = true;
            break;
          }
        }
      } else {
        // Else compare as text
        if (dir === "asc") {
          if (x.toLowerCase() > y.toLowerCase()) {
            shouldSwitch = true;
            break;
          }
        } else if (dir === "desc") {
          if (x.toLowerCase() < y.toLowerCase()) {
            shouldSwitch = true;
            break;
          }
        }
      }
    }

    if (shouldSwitch) {
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      switchcount++;
    } else {
      if (switchcount === 0 && dir === "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }

  // Update row numbers
  updateRowNumbers(table);
}

// Function to update row numbers
function updateRowNumbers() {
  var table = document.getElementById("playersList");
  var rows = table.rows;
  for (var i = 1; i < rows.length; i++) {
    var rowNumberCell = rows[i].getElementsByTagName("th")[0] || rows[i].getElementsByTagName("td")[0];
    rowNumberCell.innerText = i;
  }
}