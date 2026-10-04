"use client";

import { useState } from "react";

type EditCompanyButtonProps = {
  companyId: number;
  currentName: string;
  currentWebsite: string | null;
  currentIndustry: string | null;
  currentLocation: string | null;
  currentNotes: string | null;
};

export default function EditCompanyButton({
  companyId,
  currentName,
  currentWebsite,
  currentIndustry,
  currentLocation,
  currentNotes,
}: EditCompanyButtonProps) {
  const [open, setOpen] = useState(false);
  const [name, setName] = useState(currentName);
  const [website, setWebsite] = useState(currentWebsite ?? "");
  const [industry, setIndustry] = useState(currentIndustry ?? "");
  const [location, setLocation] = useState(currentLocation ?? "");
  const [notes, setNotes] = useState(currentNotes ?? "");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  async function handleSave() {
    setSaving(true);
    setError("");

    try {
      const response = await fetch(`/api/companies/${companyId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name,
          website: website || null,
          industry: industry || null,
          location: location || null,
          notes: notes || null,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);

        throw new Error(
          data?.detail ?? `Failed to update company: ${response.status}`,
        );
      }

      window.location.reload();
    } catch (error) {
      setError(
        error instanceof Error
          ? error.message
          : "Failed to update company.",
      );
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
              Edit Company
            </h2>

            <div className="mt-5 space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Name
                </label>

                <input
                  value={name}
                  onChange={(event) => setName(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Industry
                </label>

                <input
                  value={industry}
                  onChange={(event) => setIndustry(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Location
                </label>

                <input
                  value={location}
                  onChange={(event) => setLocation(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Website
                </label>

                <input
                  value={website}
                  onChange={(event) => setWebsite(event.target.value)}
                  className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700">
                  Notes
                </label>

                <textarea
                  value={notes}
                  onChange={(event) => setNotes(event.target.value)}
                  rows={3}
                  className="mt-2 w-full rounded-lg border border-slate-300 px-3 py-2"
                />
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