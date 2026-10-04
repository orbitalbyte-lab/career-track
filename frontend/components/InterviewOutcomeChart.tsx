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

type InterviewOutcomeChartProps = {
  data: {
    outcome: string;
    count: number;
  }[];
};

export default function InterviewOutcomeChart({
  data,
}: InterviewOutcomeChartProps) {
  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="outcome" />
          <YAxis allowDecimals={false} />
          <Tooltip />
          <Bar dataKey="count" name="Interviews" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
