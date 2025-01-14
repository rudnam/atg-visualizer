import React, { useEffect, useRef } from "react";
import Plotly, { Layout } from "plotly.js-dist";
import api from "../api";

const GraphComponent: React.FC = () => {
  const plotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const fetchAndRenderPlot = async () => {
      try {
        const response = await api.get("/graph?sequence=1234");
        const parsedData = JSON.parse(response.data);

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        const traces = parsedData.data.map((trace: any) => ({
          x: trace.x,
          y: trace.y,
          z: trace.z,
          mode: trace.mode,
          type: trace.type,
          name: trace.name,
          line: trace.line,
        }));

        const layout: Partial<Layout> = {
          margin: { l: 0, r: 0, b: 0, t: 0 },
          scene: { aspectmode: "cube" },
          showlegend: false,
        };

        const config: Partial<Plotly.Config> = {
          displaylogo: false,
          modeBarButtonsToRemove: [
            "zoom2d",
            "pan2d",
            "select2d",
            "lasso2d",
            "zoomIn2d",
            "zoomOut2d",
            "autoScale2d",
            "resetScale2d",
            "hoverClosestCartesian",
            "hoverCompareCartesian",
            "zoom3d",
            "pan3d",
            "resetCameraDefault3d",
            "resetCameraLastSave3d",
            "hoverClosest3d",
            "orbitRotation",
            "tableRotation",
            "zoomInGeo",
            "zoomOutGeo",
            "resetGeo",
            "hoverClosestGeo",
            "toImage",
            "sendDataToCloud",
            "hoverClosestGl2d",
            "hoverClosestPie",
            "toggleHover",
            "resetViews",
            "toggleSpikelines",
            "resetViewMapbox",
          ],
        };

        if (plotRef.current) {
          Plotly.newPlot(plotRef.current, traces, layout, config);
        }
      } catch (error) {
        console.error("Error rendering the plot:", error);
      }
    };

    fetchAndRenderPlot();
  }, []);

  return (
    <div className="flex flex-col shadow-lg p-8 rounded-xl">
      <div className="text-2xl font-bold">ADJACENT TRANSPOSITION GRAPH</div>
      <div className="w-full h-64 sm:h-96" ref={plotRef} />
    </div>
  );
};

export default GraphComponent;
