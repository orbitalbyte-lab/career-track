export const dynamic = "force-dynamic";

import Link from "next/link";

import { serverApiFetch } from "../../lib/server-api";
import NewFollowUpButton from "../../components/NewFollowUpButton";
import CompleteFollowUpButton from "../../components/CompleteFollowUpButton";
import DeleteFollowUpButton from "../../components/DeleteFollowUpButton";
type FollowUp = {
  id: number;
  application_id: number;
  follow_up_at: string;
  note: string;
  completed: boolean;
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

export default async function FollowUpsPage() {
  let followUps: FollowUp[] = [];
  let applications: Application[] = [];
  let companies: Company[] = [];

  try {
    followUps = await serverApiFetch<FollowUp[]>("/api/follow-ups");
  } catch {
    followUps = [];
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
              Follow-ups
            </h1>

            <p className="mt-2 text-slate-500">
              Keep track of follow-up reminders for your applications.
            </p>
          </div>

          <NewFollowUpButton
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
            <h2 className="text-lg font-semibold">Your Follow-ups</h2>

            <p className="mt-1 text-sm text-slate-500">
              {followUps.length}{" "}
              {followUps.length === 1 ? "follow-up" : "follow-ups"}
            </p>
          </div>

          <div className="mt-6 space-y-3">
            {followUps.length === 0 ? (
              <div className="rounded-xl border border-dashed border-slate-300 p-10 text-center">
                <h3 className="font-semibold">No follow-ups yet</h3>

                <p className="mt-2 text-sm text-slate-500">
                  Add a follow-up when you need to remember to contact a
                  company.
                </p>
              </div>
            ) : (
              followUps.map((followUp) => {
                const application = applications.find(
                  (item) => item.id === followUp.application_id,
                );

                const company = companies.find(
                  (item) => item.id === application?.company_id,
                );

                return (
                  <div
                    key={followUp.id}
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
                              Follow up:
                            </span>{" "}
                            {new Date(
                              followUp.follow_up_at,
                            ).toLocaleString()}
                          </p>

                          <p>
                            <span className="font-medium text-slate-700">
                              Note:
                            </span>{" "}
                            {followUp.note}
                          </p>
                        </div>
                      </div>

                      <div className="flex flex-col items-end gap-2">
                        <span
                          className={`w-fit shrink-0 rounded-full px-3 py-1.5 text-xs font-semibold ${
                            followUp.completed
                              ? "bg-green-100 text-green-700"
                              : "bg-amber-100 text-amber-700"
                          }`}
                        >
                          {followUp.completed ? "Completed" : "Pending"}
                        </span>

                        <div className="flex gap-2">
                          <CompleteFollowUpButton
                            followUpId={followUp.id}
                            completed={followUp.completed}
                          />

                           <DeleteFollowUpButton followUpId={followUp.id} />
                        </div>
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