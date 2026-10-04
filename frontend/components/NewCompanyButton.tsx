"use client";

import { useState } from "react";

import NewCompanyForm from "./NewCompanyForm";

export default function NewCompanyButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="rounded-xl bg-slate-950 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-800"
      >
        + New Company
      </button>

      {open && <NewCompanyForm onClose={() => setOpen(false)} />}
    </>
  );
}