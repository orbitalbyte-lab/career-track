export const dynamic = "force-dynamic";

import {
  Activity,
  BarChart3,
  Bell,
  BriefcaseBusiness,
  Building2,
  CalendarDays,
  LayoutDashboard,
} from "lucide-react";
import { apiFetch } from "../lib/api";

import { serverApiFetch } from "../lib/server-api";
import NewApplicationButton from "../components/NewApplicationButton";
import LogoutButton from "../components/LogoutButton";

const navigation = [
  { label: "Dashboard", icon: LayoutDashboard, active: true, href: "/" },
  { label: "Applications", icon: BriefcaseBusiness, href: "/applications" },
  { label: "Companies", icon: Building2, href: "/companies" },
  { label: "Interviews", icon: CalendarDays, href: "/interviews" },
  { label: "Follow-ups", icon: Activity, href: "/follow-ups" },
  { label: "Analytics", icon: BarChart3, href: "/analytics" },
];
type Application = {
  id: number;
  company_id: number;
  position: string;
  application_type: string;
  date_applied: string;
  status: string;
  location: string | null;
  deadline: string | null;
  job_url: string | null;
  notes: string | null;
};
type Company = {
  id: number;
  name: string;
};
type Interview = {
  id: number;
  application_id: number;
  scheduled_at: string;
  interview_type: string;
  status: string;
  outcome: string | null;
  notes: string | null;
};
type FollowUp = {
  id: number;
  application_id: number;
  follow_up_at: string;
  note: string;
  completed: boolean;
};
export default async function Home() {
  let backendConnected = false;
  let userEmail = "";
  let applications: Application[] = [];
  let companies: Company[] = [];
  let interviews: Interview[] = [];
  let followUps: FollowUp[] = [];
  try {
    const user = await serverApiFetch<{ email: string }>("/api/auth/me");
    userEmail = user.email;
  } catch (error) {
    console.error("Failed to load current user:", error);
    userEmail = "";
  }

  try {
    applications = await serverApiFetch<Application[]>("/api/applications");
  } catch {
    applications = [];
  }

  try {
    companies = await serverApiFetch<Company[]>("/api/companies");
  } catch {
    companies = [];
  }

  try {
    followUps = await serverApiFetch<FollowUp[]>("/api/follow-ups");
  } catch {
    followUps = [];
  }

  try {
    interviews = await serverApiFetch<Interview[]>("/api/interviews");
  } catch {
    interviews = [];
  }

  try {
    const health = await apiFetch<{ status: string }>("/health");
    backendConnected = health.status === "ok";
  } catch {
    backendConnected = false;
  }
    const offerCount = applications.filter(
      (application) => application.status.toLowerCase() === "offer",
    ).length;

    const stats = [
      {
        label: "Applications",
        value: String(applications.length),
        detail: "Total applications",
      },
      {
        label: "Interviews",
        value: String(interviews.length),
        detail: "Total interviews",
      },
      {
        label: "Offers",
        value: String(offerCount),
        detail: "Applications with offers",
      },
      {
        label: "Follow-ups",
        value: String(followUps.filter((followUp) => !followUp.completed).length),
        detail: "Pending follow-ups",
      },
    ];
  return (
    <div className="min-h-screen bg-slate-50 text-slate-950">
      <div className="flex min-h-screen">
        {/* Sidebar */}
        <aside className="flex w-64 shrink-0 flex-col border-r border-slate-200 bg-white">

          <div className="flex h-20 items-center border-b border-slate-200 px-6">
            <div>
              <h1 className="text-xl font-bold tracking-tight">CareerTrack</h1>
              <p className="text-xs text-slate-500">Application Manager</p>
            </div>
          </div>

          <nav className="flex-1 space-y-1 p-4">
            {navigation.map((item) => (
              <a
               key={item.label}
               href={item.href}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm font-medium transition ${
                  item.active
                    ? "bg-slate-950 text-white"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-950"
                }`}
              >
                <span className="flex h-5 w-5 items-center justify-center text-base">
                  <item.icon className="h-5 w-5" />
                </span>
                {item.label}
              </a>
            ))}
          </nav>

          <div className="border-t border-slate-200 p-4">
            <LogoutButton />
          </div>
        </aside>

        {/* Main content */}
        <main className="min-w-0 flex-1">
          {/* Top bar */}
          <header className="flex h-20 items-center justify-between border-b border-slate-200 bg-white px-6 lg:px-10">
            <div>
              <p className="text-sm text-slate-500">CareerTrack</p>
              <h2 className="font-semibold">Dashboard</h2>
            </div>

            <div className="flex items-center gap-3">
              <button
                aria-label="Notifications"
                className="flex h-10 w-10 items-center justify-center rounded-full border border-slate-200 text-slate-600 transition hover:bg-slate-50"
              >
                <Bell className="h-5 w-5" />
              </button>

              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-slate-950 text-sm font-semibold text-white">
                T
              </div>
            </div>
          </header>

          <div className="mx-auto max-w-7xl p-6 lg:p-10">
            {/* Welcome */}
            <section className="mb-8">
              <p className="mb-2 text-sm font-medium text-slate-500">
                Overview
              </p>

              <div className="flex flex-col justify-between gap-4 md:flex-row md:items-end">
                <div>
                  <h3 className="text-3xl font-bold tracking-tight">
                    Welcome to CareerTrack
                  </h3>

                  {userEmail && (
                    <p className="mt-2 text-sm text-slate-500">
                      Signed in as {userEmail}
                    </p>
                  )}
                  <p className="mt-2 max-w-2xl text-slate-500">
                    Manage your applications, companies, interviews, and
                    follow-ups in one place.
                  </p>
                  </div>
                    <NewApplicationButton companies={companies} />
                  </div>
            </section>

            {/* Stats */}
            <section className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
              {stats.map((stat) => (
                <div
                  key={stat.label}
                  className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"
                >
                  <p className="text-sm font-medium text-slate-500">
                    {stat.label}
                  </p>

                  <div className="mt-4 flex items-end justify-between">
                    <p className="text-3xl font-bold tracking-tight">
                      {stat.value}
                    </p>

                    <span className="text-xs text-slate-400">
                      {stat.detail}
                    </span>
                  </div>
                </div>
              ))}
            </section>

            {/* Main dashboard grid */}
            <section className="mt-6 grid gap-6 xl:grid-cols-3">
              {/* Applications */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm xl:col-span-2">
                <div className="flex items-center justify-between">
                  <div>
                    <h4 className="font-semibold">Recent Applications</h4>
                    <p className="mt-1 text-sm text-slate-500">
                      Your latest job applications will appear here.
                    </p>
                  </div>

                  <button className="text-sm font-medium text-slate-600 hover:text-slate-950">
                    View all →
                  </button>
                </div>

                <div className="mt-8 space-y-3">
                  {applications.length === 0 ? (
                    <div className="rounded-xl border border-dashed border-slate-300 p-10 text-center">
                      <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-slate-100 text-xl">
                        +
                      </div>

                      <h5 className="mt-4 font-semibold">
                        No applications yet
                      </h5>

                      <p className="mx-auto mt-2 max-w-md text-sm text-slate-500">
                        Create your first application to start tracking your job search.
                      </p>
                    </div>
                  ) : (
                    applications.map((application) => (
                      <div
                        key={application.id}
                        className="rounded-xl border border-slate-200 p-5 transition hover:bg-slate-50"
                      >
                        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                          <div>
                            <h5 className="font-semibold">{application.position}</h5>

                            <p className="mt-1 text-sm text-slate-500">
                              {companies.find((company) => company.id === application.company_id)?.name ??
                                "Company not found"}
                            </p>

                            <p className="mt-2 text-xs text-slate-400">
                              {application.application_type} ·{" "}
                              {application.location ?? "Location not specified"} ·{" "}
                              {application.date_applied}
                            </p>
                          </div>

                          <span className="w-fit rounded-full bg-slate-100 px-3 py-1.5 text-xs font-semibold text-slate-700">
                            {application.status}
                          </span>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* Upcoming */}
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <div>
                  <h4 className="font-semibold">Upcoming</h4>
                  <p className="mt-1 text-sm text-slate-500">
                    Interviews and follow-ups
                  </p>
                </div>

                <div className="mt-8 space-y-3">
                  <div className="rounded-xl bg-slate-50 p-4">
                    <p className="text-sm font-medium">Interviews</p>
                    {interviews.length === 0 ? (
                      <p className="mt-1 text-xs text-slate-500">
                        No upcoming interviews
                      </p>
                    ) : (
                      <div className="mt-2 space-y-2">
                        {interviews.map((interview) => (
                          <div key={interview.id}>
                            <p className="text-xs font-medium text-slate-700">
                              {interview.interview_type}
                            </p>
                            <p className="mt-1 text-xs text-slate-500">
                              {new Date(interview.scheduled_at).toLocaleString()}
                            </p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>

                  <div className="rounded-xl bg-slate-50 p-4">
                    <p className="text-sm font-medium">Follow-ups</p>

                    {followUps.filter((followUp) => !followUp.completed).length === 0 ? (
                      <p className="mt-1 text-xs text-slate-500">
                        No pending follow-ups
                      </p>
                    ) : (
                      <div className="mt-2 space-y-2">
                        {followUps
                          .filter((followUp) => !followUp.completed)
                          .map((followUp) => (
                            <div key={followUp.id}>
                              <p className="text-xs font-medium text-slate-700">
                                {followUp.note}
                              </p>
                              <p className="mt-1 text-xs text-slate-500">
                                {new Date(followUp.follow_up_at).toLocaleString()}
                              </p>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                </div>
              </div>
            </section>

            {/* API status */}
            <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h4 className="font-semibold">Backend connection</h4>
                  <p className="mt-1 text-sm text-slate-500">
                    Your CareerTrack dashboard is connected to the FastAPI backend.
                  </p>
                </div>

                <span
                  className={`inline-flex w-fit items-center gap-2 rounded-full px-3 py-1.5 text-xs font-semibold ${
                    backendConnected
                      ? "bg-emerald-50 text-emerald-700"
                      : "bg-amber-50 text-amber-700"
                  }`}
                >
                  <span
                    className={`h-2 w-2 rounded-full ${
                      backendConnected ? "bg-emerald-500" : "bg-amber-500"
                    }`}
                  />
                  {backendConnected ? "Connected" : "Not connected"}
                </span>
              </div>
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}
