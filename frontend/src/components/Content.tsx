import React, { useState } from "react";
import InputForm from "./InputForm";
import Graph from "./Graph";
import { Layout } from "plotly.js-dist";
import api from "../api";

const Content: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<Plotly.Data[] | null>(null);
  const [layout, setLayout] = useState<Partial<Layout> | null>(null);

  const fetchPlotData = async (size: number, selectedNodes: string[]) => {
    try {
      setData(null);
      setLoading(true);

      const response = await api.get(`/graph`, {
        params: {
          size: size,
          selected_nodes: selectedNodes,
        },
        paramsSerializer: {
          indexes: null,
        },
      });

      const parsedData = JSON.parse(response.data);

      const fetchedData: Plotly.Data[] = parsedData.data || [];

      setData(fetchedData);

      const fetchedLayout: Partial<Layout> = parsedData.layout || {};
      setLayout(fetchedLayout);
    } catch (error) {
      console.error("Error rendering the plot:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full px-4 md:px-8 grow flex flex-col sm:flex-row justify-center gap-12 w-full max-w-6xl mx-auto">
      <InputForm fetchPlotData={fetchPlotData} />
      <Graph loading={loading} data={data} layout={layout} />
    </div>
  );
};

export default Content;
