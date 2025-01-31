import { Layout } from "plotly.js-dist";

export interface GraphData {
  data: Plotly.Data[];
  layout: Partial<Layout>;
}

export interface PosetResult {
  name: string;
  linearExtensions: string[];
}
