"use client";

import { FormEvent, useState } from "react";

type Company = {
  id: number;
  name: string;
};

type NewApplicationFormProps = {
  companies: Company[];
  onClose: () => void;
};

export default function NewApplicationForm({
  companies,
  onClose,
}: NewApplicationFormProps) {
  const [companyId, setCompanyId] = useState(
    companies.length > 0 ? String(companies[0].id) : "",
  );
  const [position, setPosition] = useState("");
  const [applicationType, setApplicationType] = useState("Internship");
  const [dateApplied, setDateApplied] = useState(
    new Date().toISOString().split("T")[0],
  );
  const [status, setStatus] = useState("Applied");
  const [location, setLocation] = useState("");
  const [deadline, setDeadline] = useState("");
  const [jobUrl, setJobUrl] = useState("");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/applications", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          company_id: Number(companyId),
          position,
          application_type: applicationType,
          date_applied: dateApplied,
          status,
          location: location || null,
          deadline: deadline || null,
          job_url: jobUrl || null,
          notes: notes || null,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to create application.");
      }

      window.location.reload();
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Failed to create application.",
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
            <h3 className="text-xl font-bold">New Application</h3>
            <p className="mt-1 text-sm text-slate-500">
              Add a job or internship application to CareerTrack.
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
          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label
                htmlFor="company"
                className="mb-2 block text-sm font-medium"
              >
                Company
              </label>

              {companies.length > 0 ? (
                <select
                  id="company"
                  value={companyId}
                  onChange={(event) => setCompanyId(event.target.value)}
                  required
                  className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
                >
                  {companies.map((company) => (
                    <option key={company.id} value={company.id}>
                      {company.name}
                    </option>
                  ))}
                </select>
              ) : (
                <p className="rounded-xl bg-slate-50 p-3 text-sm text-slate-500">
                  Create a company first before adding an application.
                </p>
              )}
            </div>

            <div>
              <label
                htmlFor="position"
                className="mb-2 block text-sm font-medium"
              >
                Position
              </label>
              <input
                id="position"
                value={position}
                onChange={(event) => setPosition(event.target.value)}
                required
                placeholder="Software Engineering Intern"
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>

            <div>
              <label
                htmlFor="applicationType"
                className="mb-2 block text-sm font-medium"
              >
                Application type
              </label>
              <select
                id="applicationType"
                value={applicationType}
                onChange={(event) => setApplicationType(event.target.value)}
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              >
                <option value="Internship">Internship</option>
                <option value="Full-time">Full-time</option>
                <option value="Part-time">Part-time</option>
                <option value="Contract">Contract</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="dateApplied"
                className="mb-2 block text-sm font-medium"
              >
                Date applied
              </label>
              <input
                id="dateApplied"
                type="date"
                value={dateApplied}
                onChange={(event) => setDateApplied(event.target.value)}
                required
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>

            <div>
              <label
                htmlFor="status"
                className="mb-2 block text-sm font-medium"
              >
                Status
              </label>
              <select
                id="status"
                value={status}
                onChange={(event) => setStatus(event.target.value)}
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              >
                <option value="Applied">Applied</option>
                <option value="Interview">Interview</option>
                <option value="Offer">Offer</option>
                <option value="Rejected">Rejected</option>
                <option value="Withdrawn">Withdrawn</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="location"
                className="mb-2 block text-sm font-medium"
              >
                Location
              </label>
              <input
                id="location"
                value={location}
                onChange={(event) => setLocation(event.target.value)}
                placeholder="Remote"
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>

            <div>
              <label
                htmlFor="deadline"
                className="mb-2 block text-sm font-medium"
              >
                Deadline
              </label>
              <input
                id="deadline"
                type="date"
                value={deadline}
                onChange={(event) => setDeadline(event.target.value)}
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>

            <div>
              <label
                htmlFor="jobUrl"
                className="mb-2 block text-sm font-medium"
              >
                Job URL
              </label>
              <input
                id="jobUrl"
                type="url"
                value={jobUrl}
                onChange={(event) => setJobUrl(event.target.value)}
                placeholder="https://..."
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>
          </div>

          <div>
            <label
              htmlFor="notes"
              className="mb-2 block text-sm font-medium"
            >
              Notes
            </label>
            <textarea
              id="notes"
              value={notes}
              onChange={(event) => setNotes(event.target.value)}
              rows={4}
              placeholder="Optional notes about this application..."
              className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
            />
          </div>

          {error && (
            <div className="rounded-xl bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {companies.length === 0 && (
            <div className="rounded-xl bg-amber-50 p-3 text-sm text-amber-700">
              No companies are available. Please create a company first.
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
              disabled={loading || companies.length === 0}
              className="rounded-xl bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Application"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}