import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api'

export default function JobDetailPage({ user }) {
  const { id } = useParams()
  const [job, setJob] = useState(null)
  const [gap, setGap] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.getJob(id).then(j => {
      setJob(j)
      setLoading(false)
      if (user) {
        api.getSkillGap(id).then(setGap).catch(() => {})
      }
    })
  }, [id, user])

  if (loading) return (
    <div className="flex justify-center py-16">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-gray-400 text-sm">Loading job details...</p>
      </div>
    </div>
  )
  if (!job) return <div className="text-center py-16 text-gray-400">Job not found.</div>

  const roleLabel = {
    SWE: 'Software Engineering', DS: 'Data Science', PM: 'Product Management',
    UIUX: 'UI/UX Design', DE: 'Data Engineering', ML: 'Machine Learning',
    FS: 'Full Stack', IT: 'Information Technology', BA: 'Business Analysis', OT: 'Other'
  }[job.role_type] || job.role_type

  return (
    <div className="max-w-3xl mx-auto">
      <Link to="/" className="inline-flex items-center gap-1 text-sm text-gray-400 hover:text-blue-600 mb-6 transition-colors">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to listings
      </Link>

      <div className="card p-8">
        <div className="flex items-start justify-between mb-6">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold text-xl shrink-0">
              {job.company[0]}
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{job.role}</h1>
              <p className="text-gray-500 text-lg">{job.company}</p>
            </div>
          </div>
          <span className="badge bg-blue-50 text-blue-700">{roleLabel}</span>
        </div>

        <p className="text-gray-600 leading-relaxed mb-6">{job.description}</p>

        <div className="flex items-center gap-4 mb-6">
          {job.deadline && (
            <span className="flex items-center gap-1.5 text-sm text-gray-500">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
              Deadline: <strong>{job.deadline}</strong>
            </span>
          )}
        </div>

        <a href={job.application_link} target="_blank" rel="noopener noreferrer"
          className="btn-primary inline-flex items-center gap-2 mb-8">
          Apply Externally
          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
        </a>

        {job.required_skills?.length > 0 && (
          <div className="mb-8">
            <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Required Skills</h3>
            <div className="flex flex-wrap gap-2">
              {job.required_skills.map(s => (
                <span key={s.id} className="badge bg-gray-100 text-gray-700">{s.name}</span>
              ))}
            </div>
          </div>
        )}

        <div className="border-t border-gray-100 pt-6">
          <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-4">NUS Applicant Statistics</h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-4 text-center">
              <div className="text-2xl font-bold text-blue-600">{job.total_applications || 0}</div>
              <div className="text-xs text-blue-600/70 mt-1">Total Apps</div>
            </div>
            <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl p-4 text-center">
              <div className="text-2xl font-bold text-green-600">{job.offer_rate || 0}%</div>
              <div className="text-xs text-green-600/70 mt-1">Offer Rate</div>
            </div>
            <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-4 text-center">
              <div className="text-2xl font-bold text-purple-600">{job.avg_year_of_study ? `Yr ${job.avg_year_of_study}` : 'N/A'}</div>
              <div className="text-xs text-purple-600/70 mt-1">Avg Year</div>
            </div>
          </div>
          {job.gpa_distribution && Object.keys(job.gpa_distribution).length > 0 && (
            <div className="mt-4">
              <p className="text-xs text-gray-500 mb-2">GPA Distribution (Successful Applicants):</p>
              <div className="flex flex-wrap gap-2">
                {Object.entries(job.gpa_distribution).map(([range, count]) => (
                  <span key={range} className="badge bg-green-50 text-green-700">{range}: {count}</span>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {gap && (
        <div className="card p-8 mt-6">
          <h2 className="text-xl font-bold mb-6">Skill Gap Analysis</h2>

          <div className="mb-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Match Score</span>
              <span className="text-sm font-bold text-blue-600">{gap.match_score}%</span>
            </div>
            <div className="w-full h-3 bg-gray-100 rounded-full overflow-hidden">
              <div className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full transition-all duration-700"
                   style={{width: `${gap.match_score}%`}} />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-6">
            {gap.strengths?.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-green-700 uppercase tracking-wide mb-3">Your Strengths</h3>
                <div className="flex flex-wrap gap-2">
                  {gap.strengths.map(s => (
                    <span key={s.id} className="badge bg-green-100 text-green-700">{s.name}</span>
                  ))}
                </div>
              </div>
            )}

            {gap.high_priority_gaps?.length > 0 && (
              <div>
                <h3 className="text-sm font-semibold text-red-700 uppercase tracking-wide mb-3">Gaps to Address</h3>
                <div className="flex flex-wrap gap-2">
                  {gap.high_priority_gaps.map(s => (
                    <span key={s.id} className="badge bg-red-100 text-red-700">{s.name}</span>
                  ))}
                </div>
              </div>
            )}
          </div>

          {gap.suggestions?.length > 0 && (
            <div className="mt-6 pt-6 border-t border-gray-100">
              <h3 className="text-sm font-semibold text-gray-700 uppercase tracking-wide mb-3">Suggestions</h3>
              <div className="space-y-2">
                {gap.suggestions.map((s, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 bg-blue-50 rounded-xl">
                    <span className="text-blue-600 text-lg leading-none mt-0.5">💡</span>
                    <p className="text-sm text-gray-700">{s}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {user ? (
        <div className="mt-6 text-center">
          <Link to={`/jobs/${id}/outcome`}
            className="btn-secondary inline-flex items-center gap-2">
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg>
            Log Your Application Outcome
          </Link>
        </div>
      ) : (
        <div className="mt-6 text-center">
          <Link to="/login" className="btn-secondary inline-flex items-center gap-2">
            Sign in to analyse your skill gap
          </Link>
        </div>
      )}
    </div>
  )
}
