import { useState, useEffect } from 'react'
import { api } from '../api'

const FACULTIES = [
  { value: 'SOC', label: 'School of Computing' },
  { value: 'ENG', label: 'Faculty of Engineering' },
  { value: 'BIZ', label: 'NUS Business School' },
  { value: 'FASS', label: 'Faculty of Arts and Social Sciences' },
  { value: 'SCI', label: 'Faculty of Science' },
  { value: 'MED', label: 'Yong Loo Lin School of Medicine' },
  { value: 'LAW', label: 'Faculty of Law' },
]

const YEARS = ['1', '2', '3', '4', '5', '6']
const GPA_RANGES = ['0.0-2.0', '2.0-3.0', '3.0-3.5', '3.5-4.0', '4.0-5.0']

export default function ProfilePage() {
  const [profile, setProfile] = useState(null)
  const [allSkills, setAllSkills] = useState([])
  const [selectedSkillIds, setSelectedSkillIds] = useState([])
  const [saving, setSaving] = useState(false)
  const [message, setMessage] = useState('')

  useEffect(() => {
    api.getProfile().then(p => {
      setProfile(p)
      setSelectedSkillIds(p.skills.map(s => s.id))
    })
    api.getSkills().then(s => setAllSkills(s))
  }, [])

  async function handleSave(e) {
    e.preventDefault()
    setSaving(true)
    setMessage('')
    try {
      const data = new FormData(e.target)
      const payload = Object.fromEntries(data)
      payload.skill_ids = selectedSkillIds
      await api.updateProfile(payload)
      setMessage('Profile saved!')
    } catch (err) {
      setMessage('Error: ' + err.message)
    }
    setSaving(false)
  }

  function toggleSkill(id) {
    setSelectedSkillIds(prev =>
      prev.includes(id) ? prev.filter(s => s !== id) : [...prev, id]
    )
  }

  if (!profile) return (
    <div className="flex justify-center py-16">
      <div className="flex flex-col items-center gap-3">
        <div className="w-8 h-8 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
        <p className="text-gray-400 text-sm">Loading profile...</p>
      </div>
    </div>
  )

  const filledCount = [
    profile.faculty, profile.major, profile.year_of_study,
    profile.gpa_range, profile.linkedin_url,
    ...(profile.skills || [])
  ].filter(Boolean).length
  const completion = Math.min(Math.round(filledCount / 8 * 100), 100)

  return (
    <div className="max-w-2xl mx-auto">
      <div className="text-center mb-8">
        <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-blue-500 to-indigo-500 flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
          {profile.user?.username?.[0]?.toUpperCase() || '?'}
        </div>
        <h1 className="text-2xl font-bold gradient-text">Your Profile</h1>
        <p className="text-gray-500 text-sm mt-1">Manage your NUS student profile</p>
      </div>

      <div className="card p-5 mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">Profile Completion</span>
          <span className="text-sm font-bold text-blue-600">{completion}%</span>
        </div>
        <div className="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden">
          <div className="h-full bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full transition-all duration-700"
               style={{width: `${completion}%`}} />
        </div>
      </div>

      <form onSubmit={handleSave} className="card p-8 space-y-6">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Faculty</label>
            <select name="faculty" defaultValue={profile.faculty} className="input-field">
              <option value="">Select faculty</option>
              {FACULTIES.map(f => <option key={f.value} value={f.value}>{f.label}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Major</label>
            <input name="major" defaultValue={profile.major} className="input-field" placeholder="e.g. Computer Science" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Year of Study</label>
            <select name="year_of_study" defaultValue={profile.year_of_study} className="input-field">
              <option value="">Select year</option>
              {YEARS.map(y => <option key={y} value={y}>Year {y}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">GPA Range</label>
            <select name="gpa_range" defaultValue={profile.gpa_range} className="input-field">
              <option value="">Select GPA range</option>
              {GPA_RANGES.map(g => <option key={g} value={g}>{g}</option>)}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1.5">Skills <span className="text-gray-400 font-normal">(click to toggle)</span></label>
          <div className="flex flex-wrap gap-2">
            {allSkills.map(skill => (
              <button key={skill.id} type="button" onClick={() => toggleSkill(skill.id)}
                className={`badge transition-all duration-200 cursor-pointer ${
                  selectedSkillIds.includes(skill.id)
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}>
                {selectedSkillIds.includes(skill.id) ? '✓ ' : ''}{skill.name}
              </button>
            ))}
          </div>
        </div>

        <div className="border-t border-gray-100 pt-6 space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Experiences</label>
            <textarea name="experiences" defaultValue={profile.experiences} rows={3}
              className="input-field" placeholder="Describe your work experience..." />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Projects</label>
            <textarea name="projects" defaultValue={profile.projects} rows={3}
              className="input-field" placeholder="Highlight your key projects..." />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">Portfolio Links</label>
            <input name="portfolio_links" defaultValue={profile.portfolio_links}
              className="input-field" placeholder="https://github.com/your-profile" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1.5">LinkedIn URL</label>
            <input name="linkedin_url" defaultValue={profile.linkedin_url}
              className="input-field" placeholder="https://linkedin.com/in/your-profile" />
          </div>
        </div>

        {message && (
          <div className={`text-sm p-3 rounded-xl ${message.startsWith('Error') ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'}`}>
            {message}
          </div>
        )}

        <button type="submit" disabled={saving} className="btn-primary w-full">
          {saving ? 'Saving...' : 'Save Profile'}
        </button>
      </form>
    </div>
  )
}
