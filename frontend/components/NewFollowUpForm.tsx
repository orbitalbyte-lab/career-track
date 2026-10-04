"use client";

import { FormEvent, useState } from "react";

type Application = {
  id: number;
  position: string;
  company_name: string;
};

type NewFollowUpFormProps = {
  applications: Application[];
  onClose: () => void;
};

export default function NewFollowUpForm({
  applications,
  onClose,
}: NewFollowUpFormProps) {
  const [applicationId, setApplicationId] = useState(
    applications.length > 0 ? String(applications[0].id) : "",
  );
  const [followUpAt, setFollowUpAt] = useState("");
  const [note, setNote] = useState("");
  const [completed, setCompleted] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/follow-ups", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          application_id: Number(applicationId),
          follow_up_at: new Date(followUpAt).toISOString(),
          note,
          completed,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to create follow-up.");
      }

      window.location.reload();
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Failed to create follow-up.",
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
            <h3 className="text-xl font-bold">New Follow-up</h3>
            <p className="mt-1 text-sm text-slate-500">
              Add a reminder to follow up on an application.
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
              htmlFor="followUpApplication"
              className="mb-2 block text-sm font-medium"
            >
              Application
            </label>

            {applications.length > 0 ? (
              <select
                id="followUpApplication"
                value={applicationId}
                onChange={(event) => setApplicationId(event.target.value)}
                required
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              >
                {applications.map((application) => (
                  <option key={application.id} value={application.id}>
                    {application.position} — {application.company_name}
                  </option>
                ))}
              </select>
            ) : (
              <p className="rounded-xl bg-slate-50 p-3 text-sm text-slate-500">
                Create an application first before adding a follow-up.
              </p>
            )}
          </div>

          <div>
            <label
              htmlFor="followUpAt"
              className="mb-2 block text-sm font-medium"
            >
              Follow-up date and time
            </label>

            <input
              id="followUpAt"
              type="datetime-local"
              value={followUpAt}
              onChange={(event) => setFollowUpAt(event.target.value)}
              required
              className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
            />
          </div>

          <div>
            <label
              htmlFor="followUpNote"
              className="mb-2 block text-sm font-medium"
            >
              Note
            </label>

            <textarea
              id="followUpNote"
              value={note}
              onChange={(event) => setNote(event.target.value)}
              required
              rows={4}
              placeholder="Follow up with the recruiter about application status..."
              className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
            />
          </div>

          <label className="flex items-center gap-3 rounded-xl border border-slate-200 p-4">
            <input
              type="checkbox"
              checked={completed}
              onChange={(event) => setCompleted(event.target.checked)}
              className="h-4 w-4"
            />

            <span className="text-sm font-medium">
              Mark this follow-up as completed
            </span>
          </label>

          {error && (
            <div className="rounded-xl bg-red-50 p-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {applications.length === 0 && (
            <div className="rounded-xl bg-amber-50 p-3 text-sm text-amber-700">
              No applications are available. Please create an application
              first.
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
              disabled={loading || applications.length === 0}
              className="rounded-xl bg-slate-950 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Follow-up"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}