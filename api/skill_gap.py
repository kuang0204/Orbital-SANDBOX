"""Skill-gap engine.

Pure functions, no DB writes. Input: a user ``Profile`` and a ``JobListing``.
Output: a plain dict consumed directly by ``JobDetailPage.jsx``:

    {
        "match_score": int,                       # 0-100
        "strengths": [{"id", "name"}, ...],       # user skills in the target set
        "high_priority_gaps": [{"id", "name"}],   # required / common-among-successful gaps
        "medium_priority_gaps": [{"id", "name"}], # remaining target gaps
        "suggestions": [str, ...],                # human-readable, actionable
    }

The function signature is intentionally stable so M3 can swap in weighted
scoring without touching the views or serializers.
"""

# Fraction of successful applicants holding a skill above which a *missing*
# skill is treated as high priority even if it is not formally "required".
HIGH_PRIORITY_THRESHOLD = 0.5


def _tag(skill):
    return {'id': skill.id, 'name': skill.name}


def _by_name(skills):
    return sorted(skills, key=lambda s: s.name.lower())


def analyze_skill_gap(profile, job):
    user_skills = set(profile.skills.all())
    required = set(job.required_skills.all())

    # Composite profile: how often each skill appears among successful applicants.
    success_counts = {}
    successful_applicants = 0
    offer_outcomes = job.outcomes.filter(status='offer').select_related('user__profile')
    for outcome in offer_outcomes:
        applicant_profile = getattr(outcome.user, 'profile', None)
        if applicant_profile is None:
            continue
        successful_applicants += 1
        for skill in applicant_profile.skills.all():
            success_counts[skill] = success_counts.get(skill, 0) + 1

    target = required | set(success_counts.keys())

    if not target:
        return {
            'match_score': 0,
            'strengths': [],
            'high_priority_gaps': [],
            'medium_priority_gaps': [],
            'suggestions': ['No required skills are listed for this role yet.'],
        }

    strengths = user_skills & target
    missing = target - user_skills
    match_score = round(len(strengths) / len(target) * 100)

    def is_high_priority(skill):
        if skill in required:
            return True
        if successful_applicants:
            return success_counts.get(skill, 0) / successful_applicants >= HIGH_PRIORITY_THRESHOLD
        return False

    high_priority = [s for s in missing if is_high_priority(s)]
    medium_priority = [s for s in missing if s not in high_priority]

    suggestions = _build_suggestions(
        high_priority, medium_priority, success_counts, successful_applicants, required
    )

    return {
        'match_score': match_score,
        'strengths': [_tag(s) for s in _by_name(strengths)],
        'high_priority_gaps': [_tag(s) for s in _by_name(high_priority)],
        'medium_priority_gaps': [_tag(s) for s in _by_name(medium_priority)],
        'suggestions': suggestions,
    }


def _build_suggestions(high_priority, medium_priority, success_counts,
                       successful_applicants, required):
    suggestions = []

    # Lead with the highest-impact gaps, ranked by prevalence among successes.
    for skill in sorted(
        high_priority,
        key=lambda s: (-success_counts.get(s, 0), s.name.lower()),
    )[:3]:
        held = success_counts.get(skill, 0)
        if successful_applicants and held:
            pct = round(held / successful_applicants * 100)
            suggestions.append(
                f"Add {skill.name} — {pct}% of successful NUS applicants for this role had it."
            )
        elif skill in required:
            suggestions.append(
                f"{skill.name} is a required skill for this role — prioritise learning it."
            )

    for skill in _by_name(medium_priority)[:2]:
        suggestions.append(
            f"Consider a project using {skill.name} to strengthen your fit."
        )

    if not suggestions:
        suggestions.append(
            "Your profile already covers the key skills for this role — polish your projects and apply."
        )
    return suggestions
