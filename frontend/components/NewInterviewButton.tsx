"use client";

import { useState } from "react";

import NewInterviewForm from "./NewInterviewForm";

type Application = {
  id: number;
  position: string;
  company_name: string;
};

type NewInterviewButtonProps = {
  applications: Application[];
};

export default function NewInterviewButton({
  applications,
}: NewInterviewButtonProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
      >
        + New Interview
      </button>

      {open && (
        <NewInterviewForm
          applications={applications}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  );
}