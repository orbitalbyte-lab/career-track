import Link from "next/link";

import { serverApiFetch } from "../../lib/server-api";
import ApplicationStatusChart from "../../components/ApplicationStatusChart";
import ApplicationTrendChart from "../../components/ApplicationTrendChart";
import ApplicationCompanyChart from "../../components/ApplicationCompanyChart";
import ApplicationTypeChart from "../../components/ApplicationTypeChart";
import ApplicationLocationChart from "../../components/ApplicationLocationChart";
import InterviewOutcomeChart from "../../components/InterviewOutcomeChart";
export const dynamic = "force-dynamic";

type Application = {
  id: number;
  status: string;
  date_applied: string;
  company_id: number;
  application_type: string;
  location: string | null;
  deadline: string | null;
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
  outcome: string;
  notes: string | null;
};

export default async function AnalyticsPage() {
  let applications: Application[] = [];
  let companies: Company[] = [];
  let followUps: { id: number; completed: boolean }[] = [];
  let interviews: Interview[] = [];

  try {
    applications =
      await serverApiFetch<Application[]>("/api/applications");

    companies =
      await serverApiFetch<Company[]>("/api/companies");

    followUps =
      await serverApiFetch<{ id: number; completed: boolean }[]>(
        "/api/follow-ups",
      );
    interviews =
      await serverApiFetch<Interview[]>("/api/interviews");

  } catch {
    applications = [];
    followUps = [];
    companies = [];
  }

  const totalApplications = applications.length;

  const appliedCount = applications.filter(
    (application) => application.status.toLowerCase() === "applied",
  ).length;

  const interviewCount = applications.filter(
    (application) => application.status.toLowerCase() === "interview",
  ).length;

  const offerCount = applications.filter(
    (application) => application.status.toLowerCase() === "offer",
  ).length;

  const rejectedCount = applications.filter(
    (application) => application.status.toLowerCase() === "rejected",
  ).length;

  const statusData = [
    { status: "Applied", count: appliedCount },
    { status: "Interview", count: interviewCount },
    { status: "Offer", count: offerCount },
    { status: "Rejected", count: rejectedCount },
  ];

  const monthlyApplications = applications.reduce(
    (months, application) => {
      const month = application.date_applied.slice(0, 7);

      months[month] = (months[month] ?? 0) + 1;

      return months;
    },
    {} as Record<string, number>,
  );

  const applicationTrendData = Object.entries(monthlyApplications)
    .sort(([monthA], [monthB]) => monthA.localeCompare(monthB))
    .map(([month, count]) => ({
      month,
      count,
    }));

  const applicationsByCompany = applications.reduce(
    (companyCounts, application) => {
      const company = companies.find(
        (item) => item.id === application.company_id,
      );

      const companyName = company?.name ?? "Unknown company";

      companyCounts[companyName] =
        (companyCounts[companyName] ?? 0) + 1;

      return companyCounts;
    },
    {} as Record<string, number>,
  );

  const companyData = Object.entries(applicationsByCompany)
    .sort(([, countA], [, countB]) => countB - countA)
    .map(([company, count]) => ({
      company,
      count,
    }));

  const applicationsByType = applications.reduce(
    (types, application) => {
      const applicationType = application.application_type || "Other";

      types[applicationType] = (types[applicationType] ?? 0) + 1;

      return types;
    },
    {} as Record<string, number>,
  );

  const typeData = Object.entries(applicationsByType)
    .sort(([, countA], [, countB]) => countB - countA)
    .map(([type, count]) => ({
      type,
      count,
    }));

  const applicationsByLocation = applications.reduce(
    (locations, application) => {
      const location = application.location || "Not specified";

      locations[location] = (locations[location] ?? 0) + 1;

      return locations;
    },
    {} as Record<string, number>,
  );

  const locationData = Object.entries(applicationsByLocation)
    .sort(([, countA], [, countB]) => countB - countA)
    .map(([location, count]) => ({
      location,
      count,
    }));

  const upcomingDeadlines = applications
    .filter((application) => application.deadline)
    .map((application) => ({
      ...application,
      deadline: application.deadline as string,
    }))
    .filter(
      (application) =>
        new Date(application.deadline) >= new Date(),
    )
    .sort(
      (applicationA, applicationB) =>
        new Date(applicationA.deadline).getTime() -
        new Date(applicationB.deadline).getTime(),
    );

  const interviewRate =
    totalApplications > 0
      ? Math.round((interviewCount / totalApplications) * 100)
      : 0;

  const offerRate =
    totalApplications > 0
      ? Math.round((offerCount / totalApplications) * 100)
      : 0;

  const interviewToOfferRate =
    interviewCount > 0
      ? Math.round((offerCount / interviewCount) * 100)
      : 0;
  const totalInterviews = interviews.length;

  const pendingInterviews = interviews.filter(
    (interview) => interview.outcome.toLowerCase() === "pending",
  ).length;

  const passedInterviews = interviews.filter(
    (interview) => interview.outcome.toLowerCase() === "passed",
  ).length;

  const failedInterviews = interviews.filter(
    (interview) => interview.outcome.toLowerCase() === "failed",
  ).length;
  const totalFollowUps = followUps.length;

  const interviewOutcomeData = [
    { outcome: "Pending", count: pendingInterviews },
    { outcome: "Passed", count: passedInterviews },
    { outcome: "Failed", count: failedInterviews },
  ];

  const completedFollowUps = followUps.filter(
    (followUp) => followUp.completed,
  ).length;

  const pendingFollowUps = followUps.filter(
    (followUp) => !followUp.completed,
  ).length;

  return (
    <main className="min-h-screen bg-slate-50 px-6 py-8 text-slate-950 lg:px-10">
      <div className="mx-auto max-w-6xl">
        <Link
          href="/"
          className="text-sm font-medium text-slate-500 hover:text-slate-950"
        >
          ← Dashboard
        </Link>

        <h1 className="mt-3 text-3xl font-bold tracking-tight">
          Analytics
        </h1>

        <p className="mt-2 text-slate-500">
          View insights and statistics about your applications.
        </p>

        <section className="mt-8">
          <h2 className="text-lg font-semibold">
            Application Statistics
          </h2>

          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Total</p>
              <p className="mt-2 text-3xl font-bold">
                {totalApplications}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Applied</p>
              <p className="mt-2 text-3xl font-bold">
                {appliedCount}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Interviews</p>
              <p className="mt-2 text-3xl font-bold">
                {interviewCount}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Offers</p>
              <p className="mt-2 text-3xl font-bold">
                {offerCount}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Rejected</p>
              <p className="mt-2 text-3xl font-bold">
                {rejectedCount}
              </p>
            </div>
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">
            Applications by Status
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Breakdown of your applications by their current status.
          </p>

          <div className="mt-6">
            <ApplicationStatusChart data={statusData} />
          </div>
        </section>

        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">
            Applications Over Time
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Number of applications submitted each month.
          </p>

          <div className="mt-6">
            {applicationTrendData.length > 0 ? (
              <ApplicationTrendChart data={applicationTrendData} />
            ) : (
              <p className="py-12 text-center text-sm text-slate-500">
                Add applications to see your application trend.
              </p>
            )}
          </div>
        </section>

        <section className="mt-8">
          <h2 className="text-lg font-semibold">
            Conversion Rates
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            How your applications are progressing through the hiring process.
          </p>

          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Application → Interview
              </p>
              <p className="mt-2 text-3xl font-bold">
                {interviewRate}%
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Application → Offer
              </p>
              <p className="mt-2 text-3xl font-bold">
                {offerRate}%
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Interview → Offer
              </p>
              <p className="mt-2 text-3xl font-bold">
                {interviewToOfferRate}%
              </p>
            </div>
          </div>
        </section>

        {/* Application Success Rate */}
        <section className="mt-8">
          <h2 className="text-lg font-semibold">
            Application Success Rate
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Percentage of applications that resulted in an offer.
          </p>

          <div className="mt-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <p className="text-3xl font-bold">
              {offerRate}%
            </p>
          </div>
        </section>

        {/* Interview Statistics */}
        <section className="mt-8">
          <h2 className="text-lg font-semibold">
            Interview Statistics
          </h2>


          <p className="mt-1 text-sm text-slate-500">
            Overview of your interview outcomes.
          </p>

          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Total</p>
              <p className="mt-2 text-3xl font-bold">
                {totalInterviews}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Pending</p>
              <p className="mt-2 text-3xl font-bold">
                {pendingInterviews}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Passed</p>
              <p className="mt-2 text-3xl font-bold">
                {passedInterviews}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">Failed</p>
              <p className="mt-2 text-3xl font-bold">
                {failedInterviews}
              </p>
            </div>
          </div>

          <div className="mt-6">
            <InterviewOutcomeChart data={interviewOutcomeData} />
          </div>
        </section>

        {/* Upcoming Deadlines */}
        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">
            Upcoming Deadlines
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Applications with upcoming deadlines.
          </p>

          <div className="mt-6">
            {upcomingDeadlines.length > 0 ? (
              <div className="space-y-3">
                {upcomingDeadlines.map((application) => (
                  <div
                    key={application.id}
                    className="rounded-xl border border-slate-200 p-4"
                  >
                    <p className="font-medium">
                      {application.position}
                    </p>

                    <p className="mt-1 text-sm text-slate-500">
                      Deadline: {application.deadline}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="py-8 text-center text-sm text-slate-500">
                No upcoming deadlines.
              </p>
            )}
          </div>
        </section>

        <section className="mt-8">
          <h2 className="text-lg font-semibold">
            Follow-up Statistics
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Overview of your application follow-ups.
          </p>

          <div className="mt-4 grid gap-4 md:grid-cols-3">
            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Total Follow-ups
              </p>
              <p className="mt-2 text-3xl font-bold">
                {totalFollowUps}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Completed
              </p>
              <p className="mt-2 text-3xl font-bold">
                {completedFollowUps}
              </p>
            </div>

            <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
              <p className="text-sm text-slate-500">
                Pending
              </p>
              <p className="mt-2 text-3xl font-bold">
                {pendingFollowUps}
              </p>
            </div>
           </div>
          </section>
          <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold">
              Applications by Company
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Number of applications submitted to each company.
            </p>

            <div className="mt-6">
              {companyData.length > 0 ? (
                <ApplicationCompanyChart data={companyData} />
              ) : (
                <p className="py-12 text-center text-sm text-slate-500">
                  Add applications to see your applications by company.
                </p>
              )}
            </div>
          </section>
          <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold">
              Applications by Type
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Number of applications by opportunity type.
            </p>

            <div className="mt-6">
              {typeData.length > 0 ? (
                <ApplicationTypeChart data={typeData} />
              ) : (
                <p className="py-12 text-center text-sm text-slate-500">
                  Add applications to see your applications by type.
                </p>
              )}
            </div>
          </section>
                  {/* Applications by Location */}
        <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold">
            Applications by Location
          </h2>

          <p className="mt-1 text-sm text-slate-500">
            Number of applications by location.
          </p>

          <div className="mt-6">
            {locationData.length > 0 ? (
              <ApplicationLocationChart data={locationData} />
            ) : (
              <p className="py-12 text-center text-sm text-slate-500">
                Add applications to see your applications by location.
              </p>
            )}
          </div>
        </section>
     </div>
    </main>
    );
}
