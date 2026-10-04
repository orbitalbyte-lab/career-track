"use client";

import { useState } from "react";

import NewFollowUpForm from "./NewFollowUpForm";

type Application = {
  id: number;
  position: string;
  company_name: string;
};

type NewFollowUpButtonProps = {
  applications: Application[];
};

export default function NewFollowUpButton({
  applications,
}: NewFollowUpButtonProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
      >
        + New Follow-up
      </button>

      {open && (
        <NewFollowUpForm
          applications={applications}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  );
}