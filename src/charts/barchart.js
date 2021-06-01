import * as d3 from "d3";
import React, { useRef, useEffect, useState } from "react";
import {
  predThreshold,
  red,
  green,
  msToS,
  edfWindow,
  buttonStyle
} from "../constants/constants";

export default function BarChart({
  width,
  height,
  data,
  binWidth,
  binInterval,
  xStart,
  xEnd
}) {
  const ref = useRef();
  const [window, setWindow] = useState(0);
  // - 50 for y-axis taking up 50 px of width
  // Another -20 for x-axis right padding
  // Another +10: ? Don't know but it just works lol
  const barWidth = ((binWidth / msToS) * (width - 60)) / edfWindow;
  const barInterval = ((binInterval / msToS) * (width - 60)) / edfWindow;

  useEffect(() => {
    const svg = d3
      .select(ref.current)
      .attr("width", width)
      .attr("height", height);
  }, []);

  useEffect(() => {
    draw();
  }, [data]);

  const pickHex = (color1, color2, percent) => {
    // Quash the gradient
    if (percent < predThreshold) {
      percent = percent / 3;
    }
    const w1 = percent / 100;
    const w2 = 1 - w1;
    var rgb = [
      Math.round(color1[0] * w1 + color2[0] * w2),
      Math.round(color1[1] * w1 + color2[1] * w2),
      Math.round(color1[2] * w1 + color2[2] * w2)
    ];
    return rgb;
  };

  // Converts a probability (0 - 1) to a color
  const probToColor = prob => {
    let percent = Math.round((prob * 100) / 4) * 4;
    const mix = pickHex(red, green, percent);
    const barcolor = "rgb(" + mix[0] + "," + mix[1] + "," + mix[2] + ")";
    return barcolor;
  };

  const indexToXCoord = i => i * barInterval;

  const draw = () => {
    const svg = d3.select(ref.current);
    svg.selectAll("*").remove();

    var selection = svg.selectAll("rect").data(data);

    // TODO: Remove this when I have better way to viz summary stats
    d3.selection.prototype.moveToFront = function() {
      return this.each(function() {
        this.parentNode.appendChild(this);
      });
    };

    var yScale = d3
      .scaleLinear()
      .domain([0, 1])
      .range([0, height - 45]);

    // Model Confidence -> Summary Statistics
    const prob = svg
      .append("text")
      .attr("transform", "translate(" + width / 2 + " ," + 40 + ")")
      .style("text-anchor", "middle")
      .style("font", "14px")
      .text("");

    function mouseover(d, i) {
      d3.selectAll("rect").attr("fill-opacity", 0.1);
      d3.select(this).attr("fill-opacity", 1);
      // Weird quirk but i is data value here
      prob.text(`Model Confidence : ${i.toFixed(2)}`).moveToFront();
    }

    function mouseleave(d) {
      svg.selectAll("rect").attr("fill-opacity", 0.7);
      prob.text("");
    }

    // Enter
    selection
      .enter()
      .append("rect")
      .attr("x", (d, i) => indexToXCoord(i))
      .attr("y", d => height)
      .on("mouseover", mouseover)
      .on("mouseleave", mouseleave)
      .attr("pointer-events", "none")
      .attr("width", barWidth)
      .attr("height", 0)
      .attr("fill", d => probToColor(d))
      .attr("fill-opacity", 0.7)
      .transition()
      .duration(300)
      .attr("height", d => yScale(d))
      .attr("y", d => height - yScale(d))
      .attr("transform", "translate(50, -30)")
      .attr("pointer-events", "auto");

    // Update
    selection
      .on("mouseover", mouseover)
      .on("mouseleave", mouseleave)
      .attr("pointer-events", "none")
      .transition()
      .duration(300)
      .attr("height", d => yScale(d))
      .attr("x", (d, i) => indexToXCoord(i))
      .attr("y", d => height - yScale(d))
      .attr("fill", d => probToColor(d))
      .attr("width", barWidth)
      .attr("fill-opacity", 0.7)
      .attr("transform", "translate(50, -30)")
      .attr("pointer-events", "auto");

    // Exit/Clean-up during updates
    selection
      .exit()
      .transition()
      .duration(300)
      .attr("y", d => height)
      .attr("height", 0)
      .attr("pointer-events", "none")
      .remove();

    // Add X axis
    var x = d3
      .scaleLinear()
      .domain([xStart, xEnd])
      .range([40, width - 20]);
    svg
      .append("g")
      .attr("transform", "translate(10," + 210 + ")")
      .call(d3.axisBottom(x));

    // text label for the x axis
    svg
      .append("text")
      .attr("transform", "translate(" + width / 2 + " ," + height + ")")
      .style("text-anchor", "middle")
      .text("Time from start (in sec)");

    // Add Y axis
    var y = d3
      .scaleLinear()
      .domain([0, 1])
      .range([height - 30, 20]);
    svg
      .append("g")
      .call(d3.axisLeft(y))
      .attr("transform", "translate(50," + 0 + ")");

    // text label for the y axis
    svg
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0)
      .attr("x", 0 - height / 2)
      .attr("dy", "1em")
      .style("text-anchor", "middle")
      .text("Probability");
  };

  return (
    <div className="chart">
      <svg ref={ref}></svg>
    </div>
  );
}
