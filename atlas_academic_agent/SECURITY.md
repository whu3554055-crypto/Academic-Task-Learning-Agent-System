# Security Best Practices for ATLAS Project

## 🔒 Sensitive Information Protection

This document outlines the security measures implemented in this project to protect sensitive information.

### Protected Files

The following files are excluded from version control via `.gitignore`:

- `.env` - Contains API keys and secrets
- `*.env` - All environment variable files (except `.env.example`)
- `venv/` - Virtual environment (may contain cached credentials)
- `__pycache__/` - Python cache files

### Current Security Status

✅ **API Keys**: 
- `.env.example` contains placeholder values only
- Real API keys should be stored in `.env` (gitignored)
- No hardcoded credentials in source code

✅ **Personal Data**:
- Sample data files (`profile.json`, `calendar.json`, `task.json`) contain fictional test data
- No real student information or personal identifiers

✅ **Configuration**:
- Database URLs, endpoints use safe defaults
- No production secrets in code

### How to Add Your API Key Safely

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your actual API key:
   ```
   NEMOTRON_4_340B_INSTRUCT_KEY=your_real_api_key_here
   ```

3. The `.env` file is automatically ignored by Git

### Security Checklist

Before committing code, verify:

- [ ] No `.env` files with real credentials
- [ ] No hardcoded API keys in source code
- [ ] No personal/student data in sample files
- [ ] No passwords or tokens in configuration
- [ ] `.gitignore` is properly configured

### If You Accidentally Commit Secrets

1. **Immediately** rotate/revoke the exposed credential
2. Remove the secret from history:
   ```bash
   git filter-branch --force --index-filter \
     'git rm --cached --ignore-unmatch path/to/file' \
     --prune-empty --tag-name-filter cat -- --all
   ```
3. Force push to remote (if applicable):
   ```bash
   git push origin --force --all
   ```
4. Notify team members to reclone the repository

### Additional Recommendations

- Use environment variables for all secrets
- Never commit `.env` files
- Regularly rotate API keys
- Use separate keys for development and production
- Consider using a secrets manager for production deployments
