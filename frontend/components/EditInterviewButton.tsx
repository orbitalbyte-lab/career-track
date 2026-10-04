"use client";

import { useState } from "react";

type EditInterviewButtonProps = {
  interviewId: number;
  currentStatus: string;
  currentOutcome: string | null;
};

export default function EditInterviewButton({
  interviewId,
  currentStatus,
  currentOutcome,
}: EditInterviewButtonProps) {
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState(currentStatus);
  const [outcome, setOutcome] = useState(currentOutcome ?? "Pending");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function handleSave() {
    setSaving(true);
    setError("");

    try {
      const response = await fetch(`/api/interviews/${interviewId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          status,
          outcome,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to update interview: ${response.status}`);
      }

      window.location.reload();
    } catch {
      setError("Failed to update interview.");
      setSaving(false);
    }
  }

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="rounded-lg border border-slate-300 px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-100"
      >
        Edit
      </button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
          <div className="w-full max-w-md rounded-2xl bg-white p-6 shadow-xl">
            <h2 className="text-xl font-semibold">
              Edit Interview
            </h2>

            <div className="mt-5 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Status
                </label>

                <select
                  value={status}
                  onChange={(event) => setStatus(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
                >
                  <option value="Scheduled">Scheduled</option>
                  <option value="Completed">Completed</option>
                  <option value="Canceled">Canceled</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Outcome
                </label>

                <select
                  value={outcome}
                  onChange={(event) => setOutcome(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
                >
                  <option value="Pending">Pending</option>
                  <option value="Passed">Passed</option>
                  <option value="Failed">Failed</option>
                </select>
              </div>

              {error && (
                <p className="text-sm text-red-600">
                  {error}
                </p>
              )}

              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={() => setOpen(false)}
                  className="rounded-lg border border-slate-300 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100"
                >
                  Cancel
                </button>

                <button
                  type="button"
                  onClick={handleSave}
                  disabled={saving}
                  className="rounded-lg bg-slate-950 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:opacity-50"
                >
                  {saving ? "Saving..." : "Save"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </>
  );
}