import {
  Button,
  InputLabel,
  InputWrapper,
  Slider,
  Textarea,
} from "@mantine/core";
import { useState } from "react";
import GraphComponent from "./Graph";
import api from "../api";
import { Layout } from "plotly.js-dist";
import ResultsPanel from "./ResultsPanel";

const InputForm: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [size, setSize] = useState<number>(4);
  const [data, setData] = useState<Plotly.Data[] | null>(null);
  const [layout, setLayout] = useState<Partial<Layout> | null>(null);
  const [textareaValue, setTextareaValue] = useState<string>("");

  const fetchPlotData = async () => {
    try {
      setData(null);
      setLoading(true);

      const selectedNodes = textareaValue
        .split("\n")
        .map((line) => line.trim())
        .filter((line) => line !== "");

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
    <>
      <div className="w-72 h-full max-h-[36rem] flex flex-col mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
        <div className="text-xl font-bold">INPUT</div>
        <InputWrapper>
          <InputLabel>Size</InputLabel>
          <Slider
            defaultValue={4}
            min={2}
            max={6}
            onChange={setSize}
            marks={[
              { value: 2, label: 2 },
              { value: 3 },
              { value: 4 },
              { value: 5 },
              { value: 6, label: 6 },
            ]}
          />
        </InputWrapper>

        <Textarea
          className="w-36 mx-auto"
          label="Input Y"
          description="Input permutations"
          placeholder={`1234\n4321\n3214`}
          resize="vertical"
          onChange={(event) => setTextareaValue(event.currentTarget.value)}
          autosize
          minRows={4}
        />
        <Button
          className="mx-auto"
          variant="gradient"
          gradient={{ from: "purple", to: "maroon", deg: 90 }}
          onClick={() => fetchPlotData()}
        >
          Generate
        </Button>
      </div>
      <GraphComponent loading={loading} data={data} layout={layout} />
      <ResultsPanel/>
    </>
  );
};

export default InputForm;
