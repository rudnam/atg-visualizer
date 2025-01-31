import { Layout } from "plotly.js-dist";

export interface GraphData {
  data: Plotly.Data[];
  layout: Partial<Layout>;
}
