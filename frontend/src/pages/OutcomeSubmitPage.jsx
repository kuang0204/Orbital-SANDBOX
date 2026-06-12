import { useState } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { api } from '../api'

const STATUSES = [
  { value: 'offer', label: 'Offer', color: 'bg-green-100 text-green-700' },
  { value: 'rejection', label: 'Rejection', color: 'bg-red-100 text-red-700' },
  { value: 'pending', label: 'Pending', color: 'bg-yellow-100 text-yellow-700' },
]
const CHANNELS = [
  { value: 'portal', label: 'Company Portal' },
  { value: 'linkedin', label: 'LinkedIn' },
  { value: 'careerfair', label: 'Career Fair' },
  { value: 'referral', label: 'Referral' },
  { value: 'email', label: 'Direct Email' },
  { value: 'other', label: 'Other' },
]
const FORMATS = [
  { value: 'online', label: 'Online' },
  { value: 'inperson', label: 'In-Person' },
  { value: 'both', label: 'Both' },
  { value: 'none', label: 'No Interview' },
]

export default function OutcomeSubmitPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    status: '', channel: '', interview_format: '', timeline: '', notes: '',
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      await api.submitOutcome({ ...form, job: parseInt(id) })
      navigate(`/jobs/${id}`)
    } catch (err) {
      setError(err.message)
    }
    setSubmitting(false)
  }

  function update(field, value) {
    setForm(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="max-w-lg mx-auto">
      <Link to={`/jobs/${id}`} className="inline-flex items-center gap-1 text-sm text-gray-400 hover:text-blue-600 mb-6 transition-colors">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" /></svg>
        Back to job
      </Link>

      <div className="text-center mb-8">
        <span className="text-4xl">📝</span>
        <h1 className="text-2xl font-bold gradient-text mt-3">Log Your Outcome</h1>
        <p className="text-gray-500 text-sm mt-1">Share your application experience with the NUS community</p>
      </div>

      <form onSubmit={handleSubmit} className="card p-8 space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Outcome *</label>
          <div className="grid grid-cols-3 gap-2">
            {STATUSES.map(s => (
              <button key={s.value} type="button" onClick={() => update('status', s.value)}
                className={`py-3 rounded-xl text-sm font-medium border-2 transition-all duration-200 ${
                  form.status === s.value
                    ? `${s.color} border-current`
                    : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'
                }`}>
                {s.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Application Channel</label>
          <select value={form.channel} onChange={e => update('channel', e.target.value)}
            className="input-field">
            <option value="">Select channel</option>
            {CHANNELS.map(c => <option key={c.value} value={c.value}>{c.label}</option>)}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Interview Format</label>
          <div className="grid grid-cols-2 gap-2">
            {FORMATS.map(f => (
              <button key={f.value} type="button" onClick={() => update('interview_format', f.value)}
                className={`py-2.5 rounded-xl text-sm font-medium border-2 transition-all duration-200 ${
                  form.interview_format === f.value
                    ? 'bg-blue-50 text-blue-700 border-blue-500'
                    : 'bg-white text-gray-600 border-gray-200 hover:border-gray-300'
                }`}>
                {f.label}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Timeline</label>
          <input type="text" value={form.timeline} onChange={e => update('timeline', e.target.value)}
            placeholder="e.g. Applied Feb, Interview Mar, Offer Apr"
            className="input-field" />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">What I wish I had prepared</label>
          <textarea value={form.notes} onChange={e => update('notes', e.target.value)}
            rows={3} placeholder="Share tips for future applicants..."
            className="input-field" />
        </div>

        {error && (
          <div className="text-sm text-red-600 bg-red-50 rounded-xl p-3">{error}</div>
        )}

        <button type="submit" disabled={submitting} className="btn-primary w-full">
          {submitting ? (
            <span className="flex items-center justify-center gap-2">
              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
              Submitting...
            </span>
          ) : 'Submit Outcome'}
        </button>
      </form>
    </div>
  )
}
