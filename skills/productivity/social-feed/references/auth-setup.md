# Auth Setup

Use these flows when the saved local state file is missing or expired.

Do not ask the user to paste account passwords into chat. Open a headed browser window, let the user log in there, save state to a local file, then verify it in a fresh session.

## X

Default state file:

- `<workspace>/.playwright-cli/brief/x.auth-state.json`

Login and save:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"

"$PWCLI" -s=x-auth open https://x.com/home --browser chrome --headed
# User logs in manually in the opened browser window
"$PWCLI" -s=x-auth state-save "<workspace>/.playwright-cli/brief/x.auth-state.json"
```

Verify in a fresh session:

```bash
"$PWCLI" -s=x-check open about:blank --browser chrome --headed
"$PWCLI" -s=x-check state-load "<workspace>/.playwright-cli/brief/x.auth-state.json"
"$PWCLI" -s=x-check goto https://x.com/home
"$PWCLI" --raw -s=x-check eval 'location.href'
"$PWCLI" --raw -s=x-check eval 'document.querySelectorAll(\"article\").length'
```

The state is usable only if the URL is `https://x.com/home` and visible `article` elements exist.

## Weibo Home Timeline

Default state file:

- `<workspace>/.playwright-cli/brief/weibo.auth-state.json`

Open the real sign-in page:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PWCLI="$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh"

"$PWCLI" -s=weibo-auth open 'https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F' --browser chrome --headed
# User logs in manually in the opened browser window
"$PWCLI" -s=weibo-auth state-save "<workspace>/.playwright-cli/brief/weibo.auth-state.json"
```

Verify in a fresh session:

```bash
"$PWCLI" -s=weibo-check open about:blank --browser chrome --headed
"$PWCLI" -s=weibo-check state-load "<workspace>/.playwright-cli/brief/weibo.auth-state.json"
"$PWCLI" -s=weibo-check goto https://m.weibo.cn/
"$PWCLI" --raw -s=weibo-check eval 'fetch(\"https://m.weibo.cn/api/config\").then(r=>r.json()).then(x=>JSON.stringify(x))'
```

The state is usable only if:

- `api/config` reports `login: true`
- the returned uid matches the intended account when one is known
- the visible page shows the `关注` tab

