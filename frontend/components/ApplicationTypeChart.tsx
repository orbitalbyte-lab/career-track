"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

type ApplicationTypeChartProps = {
  data: {
    type: string;
    count: number;
  }[];
};

export default function ApplicationTypeChart({
  data,
}: ApplicationTypeChartProps) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="type" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" name="Applications" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}