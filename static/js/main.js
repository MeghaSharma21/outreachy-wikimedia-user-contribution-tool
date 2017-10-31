$(document).ready(function() {

  google.charts.load("current", {
    packages: ["calendar"]
  });

  var frm = $('#username_form');
  frm.submit(function() {
    $("#message").html(
      "<div class='panel panel-default message'><div class='panel-body'>Creating Graphs...</div></div>"
    );
    $.ajax({
      type: frm.attr('method'),
      data: frm.serialize(),
      success: function(data) {
        google.charts.setOnLoadCallback(drawCharts(data));
      },
      error: function(data) {
        $("#message").html(
          "<div class='panel panel-default message'><div class='panel-body'>Something went wrong!</div></div>"
        );
      }
    });
    return false;
  });
});

/**
 * Function to draw all the charts
 */
function drawCharts(data) {
  //Draw chart for articles created by a user
  if (data.articlesCreated.result == true) {
  drawContributionTimelineChart(data.articlesCreated.dates, 'Articles Created',
    'articles-created');    
  }
  else{
    $("#message").html(
          "<div class='panel panel-default message'><div class='panel-body'>" + data.articlesCreated.message + "</div></div>"
        );
  }


  //Draw chart for articles edited by a user
  if (data.articlesEdited.result == true) {
  drawContributionTimelineChart(data.articlesEdited.dates, 'Articles Edited',
    'articles-edited');   
  }
  else{
    $("#message").html(
          "<div class='panel panel-default message'><div class='panel-body'>" + data.articlesEdited.message + "</div></div>"
        );
  }
}
/**
 * Function to draw charts showing the timeline of contributions of a user
 */
function drawContributionTimelineChart(inputDataArray, typeId, elementId) {
  var dataTable = new google.visualization.DataTable();
  dataTable.addColumn({
    type: 'date',
    id: 'Date'
  });
  dataTable.addColumn({
    type: 'number',
    id: typeId
  });
  var graphData = [];
  for (var date in inputDataArray) {
    var dateArray = date.split('-');
    graphData.push([new Date(dateArray[0], Number(dateArray[1]) - 1, dateArray[
      2]), inputDataArray[date]]);
  }
  dataTable.addRows(graphData);

  var chart = new google.visualization.Calendar(document.getElementById(
    elementId));

  var options = {
    title: typeId,
    width: 1000,
  };
  $("#message").empty();
  chart.draw(dataTable, options);
}