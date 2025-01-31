import React, { useEffect, useRef } from "react";
import Plotly, { Layout } from "plotly.js-dist";
import { LoadingOverlay } from "@mantine/core";

interface GraphProps {
  loading: boolean;
  data: Plotly.Data[] | null;
  layout: Partial<Layout> | null;
  message: string;
}

const GraphComponent: React.FC<GraphProps> = ({ loading, data, layout }) => {
  const plotRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (plotRef.current) {
      if (data !== null && layout !== null) {
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

        Plotly.react(plotRef.current, data, layout, config);
      }
    }
  }, [data, layout]);

  return (
    <div className="flex flex-col p-8 w-auto md:w-full max-w-3xl h-full max-h-[36rem] bg-[#fefefe] rounded-xl shadow-lg">
      <div className="text-xl font-bold">ADJACENT TRANSPOSITION GRAPH</div>
      <div className="w-full min-h-80 h-full sm:h-96 grow relative">
        <div>
          <LoadingOverlay visible={loading} zIndex={1000} />
          <div className="" ref={plotRef} />
        </div>
      </div>
    </div>
  );
};

export default GraphComponent;
