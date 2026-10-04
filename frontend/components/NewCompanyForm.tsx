"use client";

import { FormEvent, useState } from "react";

type NewCompanyFormProps = {
  onClose: () => void;
};

export default function NewCompanyForm({
  onClose,
}: NewCompanyFormProps) {
  const [name, setName] = useState("");
  const [website, setWebsite] = useState("");
  const [industry, setIndustry] = useState("");
  const [location, setLocation] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/companies", {
        method: "POST",
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
        throw new Error(data?.detail ?? "Failed to create company.");
      }

      window.location.reload();
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Failed to create company.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
      <div className="max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-2xl bg-white p-6 shadow-xl">
        <div className="flex items-start justify-between gap-4">
          <div>
            <h3 className="text-xl font-bold">New Company</h3>
            <p className="mt-1 text-sm text-slate-500">
              Add a company to CareerTrack.
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            className="rounded-lg px-3 py-2 text-sm text-slate-500 transition hover:bg-slate-100 hover:text-slate-700"
          >
            Close
          </button>
        </div>

        <form onSubmit={handleSubmit} className="mt-6 space-y-5">
          <div>
            <label
              htmlFor="companyName"
              className="mb-2 block text-sm font-medium"
            >
              Company name
            </label>
            <input
              id="companyName"
              value={name}
              onChange={(event) => setName(event.target.value)}
              required
              placeholder="Anthropic"
              className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
            />
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label
                htmlFor="companyWebsite"
                className="mb-2 block text-sm font-medium"
              >
                Website
              </label>
              <input
                id="companyWebsite"
                type="url"
                value={website}
                onChange={(event) => setWebsite(event.target.value)}
                placeholder="https://example.com"
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>

            <div>
              <label
                htmlFor="companyIndustry"
                className="mb-2 block text-sm font-medium"
              >
                Industry
              </label>
              <input
                id="companyIndustry"
                value={industry}
                onChange={(event) => setIndustry(event.target.value)}
                placeholder="Technology"
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>

            <div>
              <label
                htmlFor="companyLocation"
                className="mb-2 block text-sm font-medium"
              >
                Location
              </label>
              <input
                id="companyLocation"
                value={location}
                onChange={(event) => setLocation(event.target.value)}
                placeholder="Remote"
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>
          </div>

          <div>
            <label
              htmlFor="companyNotes"
              className="mb-2 block text-sm font-medium"
            >
              Notes
            </label>
            <textarea
              id="companyNotes"
              value={notes}
              onChange={(event) => setNotes(event.target.value)}
              rows={4}
              placeholder="Optional notes about this company..."
              className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
            />
          </div>

          {error && (
            <div className="rounded-xl bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          <div className="flex justify-end gap-3 border-t border-slate-200 pt-5">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl border border-slate-300 px-4 py-2.5 text-sm font-semibold text-slate-700 transition hover:bg-slate-50"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Company"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}