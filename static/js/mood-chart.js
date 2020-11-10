"use strict";

Chart.pluginService.register({
  beforeDraw: function (chart) {
    var width = chart.chart.width,
      height = chart.chart.height,
      ctx = chart.chart.ctx,
      type = chart.config.type;
  },
});

let ctx_dial = $("#myChart").get(0).getContext("2d");

$.get("/mood.json", function (data) {
  let myMoodChart = new Chart(ctx_dial, {
    type: "pie",
    data: data,
    options: {
      legend: {
        display: false,
      },
      responsive: true,
      maintainAspectRatio: false,
    },
  });
});
