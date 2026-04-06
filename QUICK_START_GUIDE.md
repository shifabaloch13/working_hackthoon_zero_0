# 🚀 AI EMPLOYEE - QUICK START GUIDE

**Gold Tier - Complete Implementation**

---

## ⚡ ONE-COMMAND TEST

Run the complete test suite:

```batch
cd D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\scripts
test_all_gold_tier.bat
```

This tests all 7 Gold Tier features automatically!

---

## 📋 INDIVIDUAL FEATURE TESTS

### Gold Tier Features (7 Features)

#### 1. CEO Briefing Generator
```powershell
python ceo_briefing.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"
```
**Output:** `Briefings/YYYY-MM-DD_Weekly_Briefing.md`

---

#### 2. Subscription Audit
```powershell
python subscription_audit.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"
```
**Output:** `Briefings/Subscription_Audit_YYYY-MM-DD.md`

---

#### 3. Audit Logger
```powershell
# Log an action
python audit_logger.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" --action test_action

# Generate report
python audit_logger.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" --report --start-date 2026-03-01 --end-date 2026-03-05
```
**Output:** `Logs/Audit/YYYY-MM-DD.json`

---

#### 4. Domain Router
```powershell
python domain_router.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"
```
**Output:** Updates `Dashboard.md` with multi-domain stats

---

#### 5. Ralph Wiggum Loop
```powershell
python ralph_wiggum.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" "Process all files" --max-iterations 5
```
**Output:** Monitors file movement until complete

---

#### 6. Twitter/X MCP
```powershell
# Create tweet draft
python twitter_poster.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" --tweet "Your tweet text here"

# Post approved tweets
python twitter_poster.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" --post-approved
```
**Output:** Tweet drafts in `Pending_Approval/`, posted in `Done/`

---

#### 7. Watchdog (Process Monitor)
```powershell
python watchdog.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"
```
**Output:** Monitors processes, auto-restarts on crash

---

### Silver Tier Features (Quick Reference)

#### Gmail Watcher
```powershell
python gmail_watcher.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" "D:\Download\working_hackthoon_zero_0\credeintals.json"
```

#### Orchestrator
```powershell
python orchestrator.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" --once
```

#### Email MCP Server
```powershell
python email_mcp_server.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" "D:\Download\working_hackthoon_zero_0\credeintals.json"
```

---

## 📁 OUTPUT LOCATIONS

After running tests, check these folders:

| Folder | Contains |
|--------|----------|
| `Briefings/` | CEO briefings, subscription audits |
| `Logs/Audit/` | Audit trail JSON files |
| `Domains/` | Personal/Business domain separation |
| `Done/` | Completed actions (tweets, emails, etc.) |
| `Plans/` | Qwen Code reasoning plans |

---

## ✅ VERIFICATION CHECKLIST

After running all tests, verify:

- [ ] `Briefings/` has 2+ files
- [ ] `Logs/Audit/` has JSON files
- [ ] `Domains/` has `personal/` and `business/` folders
- [ ] `Dashboard.md` updated with multi-domain stats
- [ ] `Done/` has completed action files

---

## 🐛 TROUBLESHOOTING

### Error: "Vault path does not exist"
**Solution:** Use full absolute path:
```powershell
python ceo_briefing.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"
```

### Error: "Module not found"
**Solution:** Install dependencies:
```powershell
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client tweepy
```

### Error: "Port already in use" (Watchdog)
**Solution:** Kill existing process:
```powershell
taskkill /F /PID <PID_NUMBER>
```

---

## 🎯 COMPLETE WORKFLOW EXAMPLE

```powershell
# 1. Navigate to scripts
cd D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\scripts

# 2. Run complete test suite
test_all_gold_tier.bat

# 3. Or run individual features
python ceo_briefing.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"
python subscription_audit.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"
python audit_logger.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault" --action workflow_test
python domain_router.py "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault"

# 4. Check outputs
dir "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\Briefings"
dir "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\Logs\Audit"
dir "D:\Download\working_hackthoon_zero_0\AI_Employee_Vault\Domains"
```

---

## 📚 DOCUMENTATION

For complete details, see:
- `HACKATHON_SUBMISSION_PACKAGE.md` - Complete submission package
- `GOLD_TIER_FINAL_STATUS.md` - Final 95% status
- `GOLD_TIER_IMPLEMENTATION.md` - Architecture documentation
- `GOLD_TIER_TEST_RESULTS.md` - Live test results

---

**Ready for hackathon submission!** 🏆🚀
