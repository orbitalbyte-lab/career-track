"use client";

import { useState } from "react";

import NewApplicationForm from "./NewApplicationForm";

type Company = {
  id: number;
  name: string;
};

type NewApplicationButtonProps = {
  companies: Company[];
};

export default function NewApplicationButton({
  companies,
}: NewApplicationButtonProps) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
      >
        + New Application
      </button>

      {open && (
        <NewApplicationForm
          companies={companies}
          onClose={() => setOpen(false)}
        />
      )}
    </>
  );
}