import * as d3 from "d3";
import { useEffect } from "react";

const initChart = async (data: any[]) => {
  console.log("draw");
  // set the dimensions and margins of the graph
  const margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = window.innerWidth - 400 - margin.left - margin.right,
    height = window.innerHeight - 250 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  const svg = d3
    .select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  //Read the data
  /* const data = await d3.csv(
    "https://raw.githubusercontent.com/holtzy/data_to_viz/master/Example_dataset/2_TwoNum.csv"
  );*/
  // Add X axis
  let x = d3.scaleLinear().domain([0, 30]).range([0, width]);

  const xAxis = svg.append("g");
  xAxis.attr("transform", "translate(0," + height + ")").call(d3.axisBottom(x));

  // Add Y axis
  let y = d3.scaleLinear().domain([0, 10]).range([height, 0]);

  const yAxis = svg.append("g");
  yAxis.call(d3.axisLeft(y));

  // Add grid
  xAxis.attr("transform", "translate(0," + height + ")").call(d3.axisBottom(x));
  x.ticks().forEach(
    (tick) =>
      svg
        .append("line")
        .attr("class", "gridline")
        .attr("x1", x(tick))
        .attr("y1", 0)
        .attr("x2", x(tick))
        .attr("y2", height)
        .attr("stroke", "rgba(0, 0, 0, 0.25)") // line color
        .attr("stroke-dasharray", "4") // make it dashed;)
  );

  // Add dots
  const dots = svg
    .append("g")
    .selectAll("dot")
    .data(data)
    .enter()
    .append("circle");

  dots
    .attr("cx", function (d: any) {
      return x(d.age_in_days);
    })
    .attr("cy", function (d: any) {
      return y(d.strength);
    })
    .attr("r", () => 5 /*3 + Math.random() * 10*/)
    .style("fill", "rgba(98, 0, 255, 0.5)")
    .style("stroke", "rgba(98, 0, 255, 0.5)")
    .style("fill", "black")
    .style("stroke", "black");

  console.log("dots", dots);

  const redraw = () => {
    console.log("redraw");
    const margin = { top: 10, right: 30, bottom: 30, left: 60 },
      width = window.innerWidth - margin.left - margin.right,
      height = window.innerHeight - margin.top - margin.bottom;

    svg
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

    x = d3.scaleLinear().domain([0, 30]).range([0, width]);
    xAxis
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x));

    y = d3.scaleLinear().domain([0, 10]).range([height, 0]);
    yAxis.call(d3.axisLeft(y));

    dots
      .attr("cx", function (d: any) {
        return x(d.GrLivArea);
      })
      .attr("cy", function (d: any) {
        return y(d.SalePrice);
      })
      .attr("r", 3)
      .style("fill", "#69b3a2");
  };

  return redraw;
};

const Chart = (props: { data: any }) => {
  useEffect(() => {
    initChart(props.data).then((redraw) =>
      window.addEventListener("resize", redraw)
    );
  }, [props.data]);

  return <div id="my_dataviz" style={{ position: "relative" }}></div>;
};

export default Chart;
