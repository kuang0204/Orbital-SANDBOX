import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

const ROLE_TYPES = [
  { value: '', label: 'All Roles' },
  { value: 'SWE', label: 'Software Engineering' },
  { value: 'DS', label: 'Data Science' },
  { value: 'PM', label: 'Product Management' },
  { value: 'UIUX', label: 'UI/UX Design' },
  { value: 'DE', label: 'Data Engineering' },
  { value: 'ML', label: 'Machine Learning' },
]

export default function JobListPage({ user }) {
  const [jobs, setJobs] = useState([])
  const [roleFilter, setRoleFilter] = useState('')
  const [search, setSearch] = useState('')

  useEffect(() => {
    api.getJobs({ role_type: roleFilter }).then(setJobs)
  }, [roleFilter])

  const filtered = jobs.filter(j =>
    !search || j.company.toLowerCase().includes(search.toLowerCase()) || j.role.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div>
      <div className="text-center mb-10">
        <h1 className="text-3xl font-bold gradient-text">Discover Internships</h1>
        <p className="text-gray-500 mt-2">Browse opportunities tracked by the NUS community</p>
      </div>

      <div className="card p-4 mb-8">
        <div className="flex items-center gap-3">
          <div className="relative flex-1">
            <svg className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
            <input type="text" placeholder="Search by company or role..." value={search}
              onChange={e => setSearch(e.target.value)}
              className="input-field !pl-10" />
          </div>
          <select value={roleFilter} onChange={e => setRoleFilter(e.target.value)}
            className="input-field !w-48">
            {ROLE_TYPES.map(r => <option key={r.value} value={r.value}>{r.label}</option>)}
          </select>
        </div>
      </div>

      <div className="grid gap-4">
        {filtered.map(job => (
          <Link key={job.id} to={`/jobs/${job.id}`} className="card p-6 block">
            <div className="flex items-start justify-between">
              <div className="flex items-start gap-4">
                <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white font-bold text-lg shrink-0">
                  {job.company[0]}
                </div>
                <div>
                  <h2 className="text-lg font-semibold text-gray-900">{job.role}</h2>
                  <p className="text-gray-500">{job.company}</p>
                </div>
              </div>
              <span className="badge bg-blue-50 text-blue-700">
                {ROLE_TYPES.find(r => r.value === job.role_type)?.label || job.role_type}
              </span>
            </div>
            <div className="mt-4 flex items-center gap-4 text-sm">
              {job.total_applications > 0 && (
                <span className="flex items-center gap-1.5 text-gray-500">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
                  {job.total_applications} applicant{job.total_applications !== 1 ? 's' : ''}
                </span>
              )}
              {job.offer_rate > 0 && (
                <span className="flex items-center gap-1.5 text-green-600 font-medium">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                  {job.offer_rate}% offer rate
                </span>
              )}
              {job.deadline && (
                <span className="flex items-center gap-1.5 text-gray-400 ml-auto">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>
                  {job.deadline}
                </span>
              )}
            </div>
          </Link>
        ))}
        {filtered.length === 0 && (
          <div className="text-center py-16">
            <p className="text-4xl mb-3">🔍</p>
            <p className="text-gray-400">No jobs found matching your filters.</p>
          </div>
        )}
      </div>
    </div>
  )
}
