import React from "react";
import Plotly from "plotly.js-dist";
import { LoadingOverlay } from "@mantine/core";
import { GraphData } from "../../types";
import Plot from "react-plotly.js";

interface GraphProps {
  loading: boolean;
  graphData: GraphData | null;
}

const GraphComponent: React.FC<GraphProps> = ({ loading, graphData }) => {
  const config: Partial<Plotly.Config> = {
    displaylogo: false,
    modeBarButtonsToRemove: [
      "zoom3d",
      "pan3d",
      "resetCameraDefault3d",
      "resetCameraLastSave3d",
      "orbitRotation",
      "tableRotation",
      "toImage",
    ],
  };

  const layout: Partial<Plotly.Layout> = {
    uirevision: "constant",
    scene: {
      xaxis: { visible: false },
      yaxis: { visible: false },
      zaxis: { visible: false },
      bgcolor: "rgba(0, 0, 0, 0)",
      dragmode: "orbit",
    },
    margin: { l: 0, r: 0, b: 0, t: 0 },
    legend: {
      xanchor: "right",
      yanchor: "top",
      bgcolor: "rgba(255, 255, 255, 0.3)",
    },
  };

  return (
    <div className="flex flex-col p-8 w-auto md:w-full max-w-3xl h-full max-h-[36rem] bg-[#fefefe] rounded-xl shadow-lg">
      <div className="text-xl font-bold">ADJACENT TRANSPOSITION GRAPH</div>
      <div className="w-full min-h-80 h-full sm:h-96 grow relative">
        <div data-test-id="plot-container">
          <LoadingOverlay
            visible={loading}
            zIndex={1000}
            data-testid="loading-overlay"
          />
          {graphData && graphData.data ? (
            <div data-testid="plot-div">
              <Plot
                data={graphData.data}
                layout={layout}
                config={config}
                style={{ width: "100%", height: "100%" }}
              />
            </div>
          ) : (
            <></>
          )}
        </div>
      </div>
    </div>
  );
};

export default GraphComponent;
