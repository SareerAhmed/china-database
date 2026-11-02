# China CSC Type B research — 2027–2028

Persistent province-wise database for international master's applicants. Research is in progress: ten universities across Anhui and Fujian, including four verified 2027 intake opportunities. Historical participation never confirms the target year. Unknown means evidence is unavailable, not a negative finding.

Read README.md, PROGRESS.md, UNIVERSITIES.md, SOURCES.md and RESEARCH_LOG.md before resuming. Continue the exact next task in PROGRESS.md; compare English names, Chinese names and aliases across Markdown/JSON/CSV before adding records. The existing workspace is the project root.

UNIVERSITIES.md is authoritative. It contains all requested fields plus evidence-year dates, source IDs and counting flags. Each field is a string; URLs can point to an official guide containing a programme list. A CSC portal reference is not a separately inspected catalogue. Date fields without an evidence prefix apply only to 2027 intake. Scholarship amounts and requirements labelled 2026 must be reverified for 2027. University-level counts are not counts of individual degrees.

Statuses: CONFIRMED_2027_2028 requires official target-intake Type B evidence; PREVIOUS_YEAR_EVIDENCE requires official historical B evidence; UNVERIFIED is a candidate needing evidence. Announced-open status reflects published dates, not a tested submission or award guarantee. Conditional IELTS alternatives are separate from unconditional test exemptions. Generic English proficiency wording does not establish university-issued MOI acceptance.

Coverage: 23 provinces, five autonomous regions, four municipalities. Taiwan tracked separately with no presumed mainland CSC eligibility. No region is complete yet. Anhui initial checks are saved as NEEDS_VERIFICATION while geographic discovery proceeds in Fujian. Candidate checks and exclusions must be logged before declaring regional discovery complete; subsequent verification remains necessary.

Run `python3 scripts/sync.py` after Markdown changes (requires openpyxl; in this session use `PYTHONPATH=/tmp/csc-research-deps`). Exports: CSV, JSON and an Excel workbook with Universities, Regions and Sources sheets. Run `python3 scripts/sync.py --check` to validate without rewriting.

Repository: https://github.com/SareerAhmed/china-database (existing origin, main branch). GitHub CLI authentication verified outside sandbox on 2026-11-02; sandbox-only status checks can misleadingly report invalid authentication. Never send tokens in chat. No background process or scheduler is installed: research resumes when this agent is invoked.

Publish every 20 unique new institutions. Before publication regenerate exports, validate duplicates/equality, inspect the staged diff for secrets and personal data, stage only project files, commit meaningfully and push normally. Confirm remote commit with Git before advancing published counters. On success, update the ledger in PROGRESS and log, regenerate the workbook and publish a follow-up ledger commit; on failure retain pending counts and local work. Never force-push. For a session with fewer than 20 pending records preserve progress locally.
