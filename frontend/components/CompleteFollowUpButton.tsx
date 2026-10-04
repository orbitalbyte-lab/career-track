"use client";

import { useState } from "react";

type CompleteFollowUpButtonProps = {
  followUpId: number;
  completed: boolean;
};

export default function CompleteFollowUpButton({
  followUpId,
  completed,
}: CompleteFollowUpButtonProps) {
  const [loading, setLoading] = useState(false);

  async function handleToggle() {
    setLoading(true);

    try {
      const response = await fetch(`/api/follow-ups/${followUpId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          completed: !completed,
        }),
      });

      if (!response.ok) {
        const data = await response.json().catch(() => null);
        throw new Error(data?.detail ?? "Failed to update follow-up.");
      }

      window.location.reload();
    } catch (error) {
      alert(
        error instanceof Error
          ? error.message
          : "Failed to update follow-up.",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <button
      type="button"
      onClick={handleToggle}
      disabled={loading}
      className="w-fit rounded-xl border border-slate-300 px-3 py-2 text-xs font-semibold text-slate-700 transition hover:bg-slate-50 disabled:cursor-not-allowed disabled:opacity-50"
    >
      {loading
        ? completed
          ? "Reopening..."
          : "Completing..."
        : completed
          ? "Reopen"
          : "Mark Complete"}
    </button>
  );
}