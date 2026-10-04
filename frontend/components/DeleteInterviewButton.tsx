"use client";

import { useState } from "react";

type DeleteInterviewButtonProps = {
  interviewId: number;
};

export default function DeleteInterviewButton({
  interviewId,
}: DeleteInterviewButtonProps) {
  const [deleting, setDeleting] = useState(false);
  const [error, setError] = useState("");

  async function handleDelete() {
    const confirmed = window.confirm(
      "Are you sure you want to delete this interview?",
    );

    if (!confirmed) {
      return;
    }

    setDeleting(true);
    setError("");

    try {
      const response = await fetch(`/api/interviews/${interviewId}`, {
        method: "DELETE",
      });

      if (!response.ok) {
        throw new Error(`Failed to delete interview: ${response.status}`);
      }

      window.location.reload();
    } catch {
      setError("Failed to delete interview.");
      setDeleting(false);
    }
  }

  return (
    <div>
      <button
        type="button"
        onClick={handleDelete}
        disabled={deleting}
        className="rounded-lg border border-red-200 px-3 py-1.5 text-sm font-medium text-red-600 hover:bg-red-50 disabled:opacity-50"
      >
        {deleting ? "Deleting..." : "Delete"}
      </button>

      {error && (
        <p className="mt-2 text-xs text-red-600">
          {error}
        </p>
      )}
    </div>
  );
}