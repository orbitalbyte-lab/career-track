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

type ApplicationCompanyChartProps = {
  data: {
    company: string;
    count: number;
  }[];
};

export default function ApplicationCompanyChart({
  data,
}: ApplicationCompanyChartProps) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="company" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" name="Applications" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}