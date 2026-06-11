# Secrets and Model Configuration

Do not commit real API keys, bot tokens, webhook secrets, or private endpoints.

## Local development

1. Copy the template example file:

   ```powershell
   Copy-Item templates/telegram-agent/.env.example templates/telegram-agent/.env
   ```

2. Fill in real values in `.env`.
3. Keep `.env` local. It is ignored by Git.

## Team sharing

Use a team secret manager for real values, then each developer syncs them into their local `.env` file or shell environment.

Recommended options:

- 1Password shared vaults
- Bitwarden organizations
- Doppler
- Infisical
- Cloud secret stores such as Azure Key Vault, AWS Secrets Manager, or Google Secret Manager
- GitHub Actions secrets for CI/CD

The repository should only store `.env.example` files with safe placeholder values.

## Runtime rule

Application code should read secrets through `packages.shared.config.load_settings()` instead of directly calling `os.getenv()` in every file.

## AI provider variables

For Gemini, set:

- `MODEL_PROVIDER=gemini`
- `MODEL_NAME`
- `GEMINI_API_KEY`

For Azure OpenAI, set:

- `MODEL_PROVIDER=azure`
- `MODEL_NAME`
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_API_VERSION`
- `AZURE_OPENAI_DEPLOYMENT`
