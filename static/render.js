window.onload = function() {
  fetch('static/data.json')
    .then(function(resp){
    //  return resp.text();
      return resp.json();
    })
    .then(function(data){

      RenderSpreadsheet(data)
    });
}


// renders tables
function RenderSpreadsheet(spreadsheet){
  //function GrabByIndex
  function CreateTableNames(){
    var spreadsheet_string = '<tr>';
    for (var col in spreadsheet) {
      var table_name = '<th scope="col">'+ col + '</th>'
      spreadsheet_string += table_name;
    }
    spreadsheet_string += '</tr>'
    return spreadsheet_string
  }
  function GetTableLength(){
    for (var col in spreadsheet) {
      var table_length = Object.keys(spreadsheet[col]).length;
      return table_length
    }
  }
  function CreateTableColumns(){
    var spreadsheet_length = GetTableLength();
    var spreadsheet_string = '';
    for (let i = 0; i < spreadsheet_length; i++){
      spreadsheet_string += '<tr>';
      for (var col in spreadsheet) {
        var spreadsheet_columns = spreadsheet[col];
        var row_data = spreadsheet_columns[i];
        var table_row = '<td>' + row_data + '</td>';
        spreadsheet_string += table_row
      }
      spreadsheet_string += '</tr>';
    }
    return spreadsheet_string
  }
  const spreadsheetnames = document.getElementById('spreadsheetnames')
  //const spreadsheetcolumns = document.getElementById('spreadsheetcolumns')

  //console.log(JSON.stringify(spreadsheet))
  var HTMLSpreadsheetNames = CreateTableNames();
  var HTMLSpreadsheetColumns = CreateTableColumns();
  var HTML_cmd = `
  <table class="table table-dark">
    <tr>
      <thead>`
      + HTMLSpreadsheetNames +
    `</thead>
    </tr>
    <tr>
      <tbody>`
      + HTMLSpreadsheetColumns +
    ` </tbody>
    </tr>
  </table>
  `;
  //console.log(HTML_cmd)
  spreadsheetnames.innerHTML = HTML_cmd
}
