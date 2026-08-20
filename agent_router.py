from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent


TOOL_RULES = {
    "build": [
        "build", "create", "make", "develop", "implement",
        "website", "web", "app", "application", "ui", "interface"
    ],
    "file-manager": [
        "file", "files", "folder", "directory",
        "workspace", "project", "structure"
    ],
    "code-search": [
        "search", "find", "locate", "check", "inspect",
        "where", "code"
    ],
    "test": [
        "test", "testing", "verify", "verification",
        "cypress", "playwright", "pytest", "jest"
    ],
    "git": [
        "git", "commit", "branch", "merge",
        "repository", "repo"
    ],
    "github": [
        "github", "pull request", "pull-request",
        "issue", "repository", "repo"
    ],
    "deploy": [
        "deploy", "deployment", "vercel",
        "production", "publish", "release"
    ],
    "browser": [
        "browser", "website", "webpage",
        "page", "frontend"
    ],
    "http": [
        "api", "http", "endpoint", "request",
        "rest", "json"
    ],
    "terminal": [
        "terminal", "command", "shell",
        "npm", "pnpm", "python"
    ],
}


SKILL_RULES = {
    "frontend": [
        "html", "css", "javascript", "frontend",
        "ui", "interface", "design", "page",
        "website", "web"
    ],
    "backend": [
        "backend", "server", "api", "endpoint",
        "python", "node", "express", "aiohttp"
    ],
    "debugging": [
        "fix", "bug", "error", "broken",
        "debug", "issue", "not working", "lỗi"
    ],
    "testing": [
        "test", "testing", "verify",
        "cypress", "playwright", "pytest"
    ],
    "git-workflow": [
        "git", "github", "commit", "branch",
        "push", "pull request", "repo"
    ],
    "deployment": [
        "deploy", "deployment", "vercel",
        "production", "publish"
    ],
    "project-analysis": [
        "analyze", "analysis", "inspect",
        "review", "structure", "project"
    ],
}


def normalize(text):
    return re.sub(
        r"\s+",
        " ",
        str(text or "").lower()
    ).strip()


def score_rules(text, rules):
    text = normalize(text)
    scores = {}

    for item, keywords in rules.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        if score:
            scores[item] = score

    return sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )


def select_skills(task):
    ranked = score_rules(
        task,
        SKILL_RULES
    )

    selected = [
        name
        for name, score in ranked[:4]
    ]

    if not selected:
        selected = [
            "project-analysis"
        ]

    return selected


def select_tools(task):
    ranked = score_rules(
        task,
        TOOL_RULES
    )

    selected = [
        name
        for name, score in ranked[:5]
    ]

    if not selected:
        selected = [
            "file-manager",
            "code-search",
            "build"
        ]

    return selected


def inspect_workspace():
    files = []

    ignored = {
        ".git",
        "__pycache__",
        "node_modules",
        ".venv",
        "venv"
    }

    for path in ROOT.rglob("*"):

        if not path.is_file():
            continue

        relative = path.relative_to(ROOT)

        if any(
            part in ignored
            for part in relative.parts
        ):
            continue

        if relative.name == ".env":
            continue

        files.append(
            str(relative)
        )

    return sorted(files)[:200]


def choose_files(task, workspace):
    text = normalize(task)

    extensions = []

    if any(
        x in text
        for x in [
            "html", "web", "website",
            "frontend", "ui", "page"
        ]
    ):
        extensions += [
            ".html", ".css", ".js", ".svg"
        ]

    if any(
        x in text
        for x in [
            "python", "backend",
            "server", "api"
        ]
    ):
        extensions += [
            ".py"
        ]

    matches = []

    for filename in workspace:

        if filename.endswith(tuple(extensions)):
            matches.append(filename)

    priority = [
        "index.html",
        "style.css",
        "app.js",
        "server.py"
    ]

    ordered = []

    for filename in priority:
        if filename in matches:
            ordered.append(filename)

    for filename in matches:
        if filename not in ordered:
            ordered.append(filename)

    return ordered[:30]


def make_plan(task, skills, tools, files):
    plan = [
        "Analyze task requirements",
        "Select relevant skills",
        "Select required tools",
        "Inspect workspace"
    ]

    if files:
        plan.append(
            "Prepare affected project files"
        )

    plan += [
        "Run validation",
        "Report Agent result"
    ]

    return plan


def route(task):
    workspace = inspect_workspace()
    skills = select_skills(task)
    tools = select_tools(task)
    files = choose_files(
        task,
        workspace
    )

    plan = make_plan(
        task,
        skills,
        tools,
        files
    )

    return {
        "task": task,
        "skills": skills,
        "tools": tools,
        "workspace": workspace,
        "files": files,
        "plan": plan
    }
