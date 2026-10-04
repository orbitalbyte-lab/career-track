"use client";

import { FormEvent, useState } from "react";

type Application = {
  id: number;
  position: string;
  company_name: string;
};

type NewInterviewFormProps = {
  applications: Application[];
  onClose: () => void;
};

export default function NewInterviewForm({
  applications,
  onClose,
}: NewInterviewFormProps) {
  const [applicationId, setApplicationId] = useState(
    applications.length > 0 ? String(applications[0].id) : "",
  );
  const [scheduledAt, setScheduledAt] = useState("");
  const [interviewType, setInterviewType] = useState("Online");
  const [status, setStatus] = useState("Scheduled");
  const [outcome, setOutcome] = useState("Pending");
  const [notes, setNotes] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("/api/interviews", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          application_id: Number(applicationId),
          scheduled_at: new Date(scheduledAt).toISOString(),
          interview_type: interviewType,
          status,
          outcome: outcome || null,
          notes: notes || null,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to create interview.");
      }

      window.location.reload();
    } catch (submitError) {
      setError(
        submitError instanceof Error
          ? submitError.message
          : "Failed to create interview.",
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
            <h3 className="text-xl font-bold">New Interview</h3>
            <p className="mt-1 text-sm text-slate-500">
              Add an interview to an existing application.
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
              htmlFor="interviewApplication"
              className="mb-2 block text-sm font-medium"
            >
              Application
            </label>

            {applications.length > 0 ? (
              <select
                id="interviewApplication"
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
                Create an application first before adding an interview.
              </p>
            )}
          </div>

          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label
                htmlFor="scheduledAt"
                className="mb-2 block text-sm font-medium"
              >
                Scheduled date and time
              </label>

              <input
                id="scheduledAt"
                type="datetime-local"
                value={scheduledAt}
                onChange={(event) => setScheduledAt(event.target.value)}
                required
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              />
            </div>

            <div>
              <label
                htmlFor="interviewType"
                className="mb-2 block text-sm font-medium"
              >
                Interview type
              </label>

              <select
               id="interviewType"
               value={interviewType}
               onChange={(event) => setInterviewType(event.target.value)}
               className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
             >
               <option value="Online">Online</option>
               <option value="Phone">Phone</option>
               <option value="On-site">On-site</option>
             </select>
            </div>

            <div>
              <label
                htmlFor="interviewStatus"
                className="mb-2 block text-sm font-medium"
              >
                Status
              </label>

              <select
                id="interviewStatus"
                value={status}
                onChange={(event) => setStatus(event.target.value)}
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              >
                <option value="Scheduled">Scheduled</option>
                <option value="Completed">Completed</option>
                <option value="Cancelled">Cancelled</option>
                <option value="Rescheduled">Rescheduled</option>
              </select>
            </div>

            <div>
              <label
                htmlFor="interviewOutcome"
                className="mb-2 block text-sm font-medium"
              >
                Outcome
              </label>

              <select
                id="interviewOutcome"
                value={outcome}
                onChange={(event) => setOutcome(event.target.value)}
                className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
              >
                <option value="Pending">Pending</option>
                <option value="Passed">Passed</option>
                <option value="Failed">Failed</option>
              </select>
            </div>
          </div>

          <div>
            <label
              htmlFor="interviewNotes"
              className="mb-2 block text-sm font-medium"
            >
              Notes
            </label>

            <textarea
              id="interviewNotes"
              value={notes}
              onChange={(event) => setNotes(event.target.value)}
              rows={4}
              placeholder="Optional notes about the interview..."
              className="w-full rounded-xl border border-slate-300 px-3 py-2.5 text-sm outline-none focus:border-slate-500"
            />
          </div>

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
              {loading ? "Creating..." : "Create Interview"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}