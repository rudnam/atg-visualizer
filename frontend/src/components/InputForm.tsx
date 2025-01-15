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

const InputForm: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [size, setSize] = useState<number>(4);
  const [data, setData] = useState<Plotly.Data[] | null>(null);
  const [layout, setLayout] = useState<Partial<Layout> | null>(null);

  const generateSequence = (size: number): string => {
    return Array.from({ length: size }, (_, i) => i + 1).join("");
  };

  const fetchPlotData = async () => {
    try {
      setData(null);
      setLoading(true);
      const response = await api.get(
        `/graph?sequence=${generateSequence(size)}`
      );

      const parsedData = JSON.parse(response.data);

      const fetchedData: Plotly.Data[] = parsedData.data || [];

      setData(fetchedData);

      const fetchedLayout: Partial<Layout> = parsedData.layout || {};
      setLayout(fetchedLayout);
      console.log(fetchedLayout);
    } catch (error) {
      console.error("Error rendering the plot:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="w-72 h-full max-h-[36rem] flex flex-col mx-auto md:mx-0 gap-4 bg-[#fefefe] p-8 rounded-xl shadow-lg">
        <div className="text-2xl font-bold">INPUT</div>
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
          description="Input the linear orders"
          placeholder={`1234\n4321\n3214`}
          resize="vertical"
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
    </>
  );
};

export default InputForm;
