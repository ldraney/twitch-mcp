# Issue: Retest all tools after SDK fixes and token update

**Repository:** twitch-mcp
**Priority:** Medium
**Labels:** qa, testing
**Depends on:** #001, #002, #003

## Summary
After fixing SDK bugs and updating the OAuth token, run a complete retest of all 110 tools.

## Prerequisites
- [ ] Issue #001 (SDK bugs) resolved
- [ ] Issue #002 (OAuth scopes) resolved
- [ ] Issue #003 (App token support) resolved

## Test Plan
1. Ensure MCP server connects to Claude Code session
2. Run through all phases from QA_TEST_MATRIX.md
3. Update matrix with new results
4. Verify live stream operations work (while streaming)

## Current Status (from 2026-01-21 test)
| Status | Count |
|--------|-------|
| Passed | 14 |
| Failed (SDK bugs) | 11 |
| Skipped (scope/requirements) | 38 |
| Not tested | 50 |

## Target Status
| Status | Target |
|--------|--------|
| Passed | 80+ |
| Failed | 0 |
| Skipped (special requirements) | ~20 |
| Not tested | 0 |

## Acceptance Criteria
- [ ] All SDK bugs resolved (11 tools move from Failed to Passed)
- [ ] All scope issues resolved (38 tools move from Skipped to Passed/Tested)
- [ ] All 50 untested tools tested
- [ ] Conduit endpoints work with app token
- [ ] QA_TEST_MATRIX.md updated with final results
- [ ] No critical bugs remaining
