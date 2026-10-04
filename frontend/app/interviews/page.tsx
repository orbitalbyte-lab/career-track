export const dynamic = "force-dynamic";

import Link from "next/link";

import { serverApiFetch } from "../../lib/server-api";
import NewInterviewButton from "../../components/NewInterviewButton";
import EditInterviewButton from "../../components/EditInterviewButton";
import DeleteInterviewButton from "../../components/DeleteInterviewButton";

type Interview = {
  id: number;
  application_id: number;
  scheduled_at: string;
  interview_type: string;
  status: string;
  outcome: string | null;
  notes: string | null;
};

type Application = {
  id: number;
  company_id: number;
  position: string;
};

type Company = {
  id: number;
  name: string;
};

export default async function InterviewsPage() {
  let interviews: Interview[] = [];
  let applications: Application[] = [];
  let companies: Company[] = [];

  try {
    interviews = await serverApiFetch<Interview[]>("/api/interviews");
  } catch {
    interviews = [];
  }

  try {
    applications =
      await serverApiFetch<Application[]>("/api/applications");
  } catch {
    applications = [];
  }

  try {
    companies = await serverApiFetch<Company[]>("/api/companies");
  } catch {
    companies = [];
  }

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-8 text-slate-950 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <Link
              href="/"
              className="text-sm font-medium text-slate-500 hover:text-slate-950"
            >
              ← Dashboard
            </Link>

            <h1 className="mt-3 text-3xl font-bold tracking-tight">
              Interviews
            </h1>

            <p className="mt-2 text-slate-500">
              Track your upcoming and completed interviews.
            </p>
          </div>

          <NewInterviewButton
            applications={applications.map((application) => {
              const company = companies.find(
                (item) => item.id === application.company_id,
              );

              return {
                id: application.id,
                position: application.position,
                company_name: company?.name ?? "Company not found",
              };
            })}
          />
        </div>

        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div>
            <h2 className="text-lg font-semibold">Your Interviews</h2>
            <p className="mt-1 text-sm text-slate-500">
              {interviews.length}{" "}
              {interviews.length === 1 ? "interview" : "interviews"}
            </p>
          </div>

          <div className="mt-6 space-y-3">
            {interviews.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-300 p-10 text-center">
                <h3 className="font-semibold">No interviews yet</h3>

                <p className="mt-2 text-sm text-slate-500">
                  Add an interview when an application moves to the interview
                  stage.
                </p>
              </div>
            ) : (
              interviews.map((interview) => {
                const application = applications.find(
                  (item) => item.id === interview.application_id,
                );

                const company = companies.find(
                  (item) => item.id === application?.company_id,
                );

                return (
                  <div
                    key={interview.id}
                    className="rounded-xl border border-slate-200 p-5 transition hover:bg-slate-50"
                  >
                    <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
                      <div>
                        <h3 className="font-semibold">
                          {application?.position ?? "Application not found"}
                        </h3>

                        <p className="mt-1 text-sm text-slate-500">
                          {company?.name ?? "Company not found"}
                        </p>

                        <div className="mt-3 space-y-2 text-sm text-slate-500">
                          <p>
                            <span className="font-medium text-slate-700">
                              Type:
                            </span>{" "}
                            {interview.interview_type}
                          </p>

                          <p>
                            <span className="font-medium text-slate-700">
                              Scheduled:
                            </span>{" "}
                            {new Date(
                              interview.scheduled_at,
                            ).toLocaleString()}
                          </p>

                          {interview.outcome && (
                            <p>
                              <span className="font-medium text-slate-700">
                                Outcome:
                              </span>{" "}
                              {interview.outcome}
                            </p>
                          )}

                          {interview.notes && (
                            <p>
                              <span className="font-medium text-slate-700">
                                Notes:
                              </span>{" "}
                              {interview.notes}
                            </p>
                          )}
                        </div>
                      </div>

                        <div className="flex shrink-0 items-center gap-2">
                          <EditInterviewButton
                            interviewId={interview.id}
                            currentStatus={interview.status}
                            currentOutcome={interview.outcome}
                          />

                          <DeleteInterviewButton interviewId={interview.id} />

                          <span className="w-fit rounded-full bg-slate-100                  px-3 py-1.5 text-xs font-semibold text-slate-700">
                            {interview.status}
                           </span>
                          </div>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </section>
      </div>
    </main>
  );
}