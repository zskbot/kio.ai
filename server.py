import os
import aiohttp
from aiohttp import ClientSession
import json
import time
import asyncio
from pathlib import Path
from aiohttp import web
from agent_router import route as kio_route

ROOT = Path.cwd()


def load_local_env():

    env_file = ROOT / ".env"

    if not env_file.exists():
        return

    try:

        for raw in env_file.read_text().splitlines():

            line = raw.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)

            key = key.strip()
            value = value.strip()

            if (
                len(value) >= 2
                and value[0] == value[-1]
                and value[0] in ("'", '"')
            ):
                value = value[1:-1]

            if key:
                os.environ.setdefault(
                    key,
                    value
                )

    except Exception:
        pass

load_local_env()

CLIENTS = set()
EVENTS = []

IGNORE = {
    ".git",
    "node_modules",
    ".next",
    "dist",
    "build",
    "__pycache__",
    ".cache",
}

def read_json(path, fallback):
    try:
        return json.loads(path.read_text())
    except:
        return fallback

def project_files():
    result = []

    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue

        if any(part in IGNORE for part in p.parts):
            continue

        try:
            result.append({
                "path": str(p.relative_to(ROOT)),
                "size": p.stat().st_size
            })
        except:
            pass

    return sorted(result, key=lambda x: x["path"])

def get_skills():
    return read_json(
        ROOT / "skills" / "index.json",
        []
    )

def get_plugins():
    return read_json(
        ROOT / "plugins" / "index.json",
        []
    )

def get_tools():
    return read_json(
        ROOT / "tools.json",
        []
    )

def tool_for_task(task):
    text = task.lower()

    rules = {
        "terminal": [
            "terminal",
            "command",
            "npm",
            "pnpm",
            "python",
            "shell"
        ],
        "file-manager": [
            "file",
            "folder",
            "workspace",
            "project"
        ],
        "code-search": [
            "search",
            "find",
            "locate",
            "code"
        ],
        "build": [
            "build",
            "compile",
            "create",
            "develop"
        ],
        "test": [
            "test",
            "testing",
            "cypress",
            "playwright",
            "jest"
        ],
        "git": [
            "git",
            "branch",
            "commit",
            "merge"
        ],
        "github": [
            "github",
            "pull request",
            "issue",
            "repository",
            "repo"
        ],
        "deploy": [
            "deploy",
            "deployment",
            "production",
            "vercel"
        ],
        "browser": [
            "browser",
            "website",
            "web",
            "page"
        ],
        "http": [
            "api",
            "http",
            "endpoint",
            "request"
        ]
    }

    selected=[]

    for tool in get_tools():
        tid=tool["id"]

        if any(
            word in text
            for word in rules.get(tid, [])
        ):
            selected.append(tid)

    if not selected:
        selected=["file-manager","build"]

    return selected

def detect_skills(task):
    text = task.lower()

    selected = []

    rules = {
        "frontend": [
            "frontend",
            "html",
            "css",
            "javascript",
            "js",
            "react",
            "vue",
            "website",
            "web",
            "ui",
            "interface"
        ],
        "backend": [
            "backend",
            "api",
            "server",
            "express",
            "python",
            "node"
        ],
        "database": [
            "database",
            "db",
            "sql",
            "postgres",
            "supabase",
            "mysql"
        ],
        "debugging": [
            "fix",
            "debug",
            "error",
            "bug",
            "broken",
            "issue"
        ],
        "git": [
            "git",
            "github",
            "branch",
            "commit",
            "pull request",
            "pr"
        ],
        "testing": [
            "test",
            "testing",
            "cypress",
            "playwright",
            "jest"
        ],
        "deploy": [
            "deploy",
            "deployment",
            "vercel",
            "hosting",
            "production"
        ],
        "build": [
            "build",
            "create",
            "make",
            "develop",
            "application",
            "app",
            "project"
        ]
    }

    for skill in get_skills():
        sid = skill["id"]

        if any(word in text for word in rules.get(sid, [])):
            selected.append(sid)

    if not selected:
        selected = ["build"]

    return selected

async def broadcast(event):
    EVENTS.append(event)

    if len(EVENTS) > 1000:
        del EVENTS[:-1000]

    dead = []

    for ws in list(CLIENTS):
        try:
            await ws.send_str(json.dumps(event))
        except:
            dead.append(ws)

    for ws in dead:
        CLIENTS.discard(ws)

async def log(message, level="info"):
    await broadcast({
        "type":"log",
        "time":time.strftime("%H:%M:%S"),
        "level":level,
        "message":message
    })

async def activity(message, status="working"):
    await broadcast({
        "type":"activity",
        "message":message,
        "status":status
    })

async def tool_call(tool_id, status="CALLED"):
    await broadcast({
        "type":"tool",
        "tool":tool_id,
        "status":status
    })


async def run_task(task):

    task = str(task or "").strip()

    if not task:
        return

    try:

        await broadcast({
            "type": "activity",
            "status": "working"
        })

        await log(
            "KIO Agent Router: analyzing task"
        )

        result = kio_route(task)

        skills = result.get(
            "skills",
            []
        )

        tools = result.get(
            "tools",
            []
        )

        files = result.get(
            "files",
            []
        )

        plan = result.get(
            "plan",
            []
        )

        await broadcast({
            "type": "plan",
            "items": plan
        })

        await broadcast({
            "type": "skills",
            "skills": skills
        })

        await log(
            "✓ Skills selected: "
            + ", ".join(skills)
        )

        await log(
            "✓ Tools selected: "
            + ", ".join(tools)
        )

        prepared_files = []

        for filename in files:

            prepared_files.append({
                "path": filename,
                "status": "READY"
            })

        await broadcast({
            "type": "files",
            "files": prepared_files
        })

        await log(
            "Workspace inspected: "
            f"{len(result.get('workspace', []))} files"
        )

        for tool in tools:

            await broadcast({
                "type": "plugin",
                "plugin": tool,
                "action": "route",
                "status": "CALLING"
            })

            await log(
                f"→ tool:{tool}"
            )

        if prepared_files:

            working_files = []

            for item in prepared_files:

                working_files.append({
                    "path": item["path"],
                    "status": "WORKING"
                })

            await broadcast({
                "type": "files",
                "files": working_files
            })

            await log(
                "Agent prepared affected files"
            )

            staged_files = []

            for item in prepared_files:

                staged_files.append({
                    "path": item["path"],
                    "status": "STAGED"
                })

            await broadcast({
                "type": "files",
                "files": staged_files
            })

        await log(
            "✓ Agent Router validation complete"
        )

        summary = (
            "KIO đã phân tích task và tạo execution plan.\n\n"
            "Skills: "
            + ", ".join(skills)
            + "\n"
            "Tools: "
            + ", ".join(tools)
            + "\n"
            "Files: "
            + (
                ", ".join(files)
                if files
                else "workspace scan only"
            )
        )

        await broadcast({
            "type": "agent",
            "message": summary
        })

        await broadcast({
            "type": "activity",
            "status": "done"
        })

        await broadcast({
            "type": "complete"
        })

    except Exception as error:

        await log(
            "✗ Agent Router error: "
            + str(error)
        )

        await broadcast({
            "type": "agent",
            "message":
                "KIO Agent Router gặp lỗi: "
                + str(error)
        })

        await broadcast({
            "type": "activity",
            "status": "error"
        })

        await broadcast({
            "type": "complete"
        })

async def index(request):
    return web.FileResponse(
        ROOT / "index.html"
    )


async def task_api(request):

    data = await request.json()

    task = str(
        data.get("task","")
    ).strip()

    if not task:
        return web.json_response(
            {"error":"Task is empty"},
            status=400
        )

    asyncio.create_task(
        run_task(task)
    )

    return web.json_response({
        "ok":True,
        "task":task
    })


async def files_api(request):

    return web.json_response({
        "root":str(ROOT),
        "files":project_files()
    })


async def skills_api(request):

    return web.json_response(
        get_skills()
    )



async def tools_api(request):

    return web.json_response(
        get_tools()
    )


async def events_api(request):

    return web.json_response(
        EVENTS[-200:]
    )


async def websocket(request):

    ws = web.WebSocketResponse()

    await ws.prepare(request)

    CLIENTS.add(ws)

    for event in EVENTS[-100:]:
        await ws.send_str(
            json.dumps(event)
        )

    try:

        async for _ in ws:
            pass

    finally:

        CLIENTS.discard(ws)

    return ws


async def static_file(request):

    filename = request.match_info["filename"]

    safe = (
        ROOT / filename
    ).resolve()

    try:
        safe.relative_to(
            ROOT.resolve()
        )
    except:
        raise web.HTTPForbidden()

    if not safe.exists():
        raise web.HTTPNotFound()

    if not safe.is_file():
        raise web.HTTPNotFound()

    return web.FileResponse(safe)




def get_plugin_registry():

    return read_json(
        ROOT / "plugins.json",
        []
    )


def get_plugin(plugin_id):

    return next(
        (
            item
            for item in get_plugin_registry()
            if item.get("id") == plugin_id
        ),
        None
    )


def plugin_token(plugin):

    if not plugin:
        return ""

    env_name = plugin.get(
        "env",
        ""
    )

    return os.environ.get(
        env_name,
        ""
    ).strip()


def plugin_status(plugin):

    token = plugin_token(plugin)

    return {
        "id": plugin.get("id"),
        "name": plugin.get("name"),
        "category": plugin.get("category"),
        "description": plugin.get("description"),
        "configured": bool(token),
        "status":
            "CONNECTED"
            if token
            else "NOT_CONFIGURED"
    }


def get_plugins_with_status():

    return [
        plugin_status(plugin)
        for plugin in get_plugin_registry()
    ]


async def http_json(
    method,
    url,
    headers=None,
    params=None,
    json_data=None
):

    timeout = aiohttp.ClientTimeout(
        total=20
    )

    async with ClientSession(
        timeout=timeout
    ) as session:

        async with session.request(
            method,
            url,
            headers=headers or {},
            params=params,
            json=json_data
        ) as response:

            text = await response.text()

            try:
                data = json.loads(text)
            except Exception:
                data = {
                    "raw": text[:4000]
                }

            return (
                response.status,
                data
            )


async def github_adapter(
    action,
    payload=None
):

    token = os.environ.get(
        "GITHUB_TOKEN",
        ""
    ).strip()

    if not token:
        return {
            "ok": False,
            "status": "NOT_CONFIGURED",
            "message":
                "GITHUB_TOKEN is missing."
        }

    headers = {
        "Authorization":
            f"Bearer {token}",
        "Accept":
            "application/vnd.github+json",
        "X-GitHub-Api-Version":
            "2022-11-28"
    }

    payload = payload or {}

    if action == "status":

        code, data = await http_json(
            "GET",
            "https://api.github.com/user",
            headers=headers
        )

        return {
            "ok": code < 300,
            "provider": "github",
            "action": action,
            "status_code": code,
            "user": {
                "login":
                    data.get("login"),
                "name":
                    data.get("name"),
                "public_repos":
                    data.get("public_repos")
            }
        }

    if action == "repos":

        code, data = await http_json(
            "GET",
            "https://api.github.com/user/repos",
            headers=headers,
            params={
                "per_page": 30,
                "sort": "updated"
            }
        )

        repos = []

        if isinstance(data, list):

            for repo in data:

                repos.append({
                    "name":
                        repo.get("name"),
                    "full_name":
                        repo.get("full_name"),
                    "private":
                        repo.get("private"),
                    "default_branch":
                        repo.get(
                            "default_branch"
                        )
                })

        return {
            "ok": code < 300,
            "provider": "github",
            "action": action,
            "status_code": code,
            "repos": repos
        }

    return {
        "ok": False,
        "provider": "github",
        "error":
            f"Unsupported action: {action}"
    }


async def vercel_adapter(
    action,
    payload=None
):

    token = os.environ.get(
        "VERCEL_TOKEN",
        ""
    ).strip()

    if not token:
        return {
            "ok": False,
            "status": "NOT_CONFIGURED",
            "message":
                "VERCEL_TOKEN is missing."
        }

    headers = {
        "Authorization":
            f"Bearer {token}"
    }

    if action == "status":

        code, data = await http_json(
            "GET",
            "https://api.vercel.com/v2/user",
            headers=headers
        )

        user = data.get(
            "user",
            {}
        )

        return {
            "ok": code < 300,
            "provider": "vercel",
            "action": action,
            "status_code": code,
            "user": {
                "username":
                    user.get("username"),
                "email":
                    user.get("email")
            }
        }

    if action == "projects":

        code, data = await http_json(
            "GET",
            "https://api.vercel.com/v9/projects",
            headers=headers,
            params={
                "limit": 30
            }
        )

        projects = []

        for project in data.get(
            "projects",
            []
        ):

            projects.append({
                "id":
                    project.get("id"),
                "name":
                    project.get("name"),
                "framework":
                    project.get("framework")
            })

        return {
            "ok": code < 300,
            "provider": "vercel",
            "action": action,
            "status_code": code,
            "projects": projects
        }

    return {
        "ok": False,
        "provider": "vercel",
        "error":
            f"Unsupported action: {action}"
    }


async def openai_adapter(
    action,
    payload=None
):

    token = os.environ.get(
        "OPENAI_API_KEY",
        ""
    ).strip()

    if not token:
        return {
            "ok": False,
            "status": "NOT_CONFIGURED",
            "message":
                "OPENAI_API_KEY is missing."
        }

    headers = {
        "Authorization":
            f"Bearer {token}"
    }

    if action in (
        "status",
        "models"
    ):

        code, data = await http_json(
            "GET",
            "https://api.openai.com/v1/models",
            headers=headers
        )

        models = []

        for model in data.get(
            "data",
            []
        )[:50]:

            models.append(
                model.get("id")
            )

        return {
            "ok": code < 300,
            "provider": "openai",
            "action": "models",
            "status_code": code,
            "models": models
        }

    return {
        "ok": False,
        "provider": "openai",
        "error":
            f"Unsupported action: {action}"
    }


async def anthropic_adapter(
    action,
    payload=None
):

    token = os.environ.get(
        "ANTHROPIC_API_KEY",
        ""
    ).strip()

    if not token:
        return {
            "ok": False,
            "status": "NOT_CONFIGURED",
            "message":
                "ANTHROPIC_API_KEY is missing."
        }

    headers = {
        "x-api-key":
            token,
        "anthropic-version":
            "2023-06-01"
    }

    if action in (
        "status",
        "models"
    ):

        code, data = await http_json(
            "GET",
            "https://api.anthropic.com/v1/models",
            headers=headers
        )

        models = []

        for model in data.get(
            "data",
            []
        )[:50]:

            models.append(
                model.get("id")
            )

        return {
            "ok": code < 300,
            "provider": "anthropic",
            "action": "models",
            "status_code": code,
            "models": models
        }

    return {
        "ok": False,
        "provider": "anthropic",
        "error":
            f"Unsupported action: {action}"
    }


async def google_ai_adapter(
    action,
    payload=None
):

    token = os.environ.get(
        "GOOGLE_AI_API_KEY",
        ""
    ).strip()

    if not token:
        return {
            "ok": False,
            "status": "NOT_CONFIGURED",
            "message":
                "GOOGLE_AI_API_KEY is missing."
        }

    if action in (
        "status",
        "models"
    ):

        code, data = await http_json(
            "GET",
            "https://generativelanguage.googleapis.com/v1beta/models",
            params={
                "key": token
            }
        )

        models = []

        for model in data.get(
            "models",
            []
        )[:50]:

            models.append(
                model.get("name")
            )

        return {
            "ok": code < 300,
            "provider": "google-ai",
            "action": "models",
            "status_code": code,
            "models": models
        }

    return {
        "ok": False,
        "provider": "google-ai",
        "error":
            f"Unsupported action: {action}"
    }



async def ollama_adapter(
    action,
    payload=None
):

    payload = payload or {}

    base_url = os.environ.get(
        "OLLAMA_HOST",
        "http://127.0.0.1:11434"
    ).strip()

    if base_url.endswith("/"):
        base_url = base_url[:-1]

    if action == "status":

        try:
            code, data = await http_json(
                "GET",
                f"{base_url}/api/tags"
            )

            models = []

            for model in data.get(
                "models",
                []
            ):

                models.append({
                    "name":
                        model.get("name"),
                    "size":
                        model.get("size"),
                    "modified_at":
                        model.get(
                            "modified_at"
                        )
                })

            return {
                "ok": code < 300,
                "provider": "ollama",
                "action": "status",
                "status_code": code,
                "models": models
            }

        except Exception as error:

            return {
                "ok": False,
                "provider": "ollama",
                "status": "OFFLINE",
                "error": str(error)
            }

    if action == "models":

        return await ollama_adapter(
            "status",
            payload
        )

    if action == "chat":

        model = str(
            payload.get(
                "model",
                ""
            )
        ).strip()

        message = str(
            payload.get(
                "message",
                ""
            )
        ).strip()

        if not model:
            return {
                "ok": False,
                "provider": "ollama",
                "error":
                    "Missing model"
            }

        if not message:
            return {
                "ok": False,
                "provider": "ollama",
                "error":
                    "Missing message"
            }

        code, data = await http_json(
            "POST",
            f"{base_url}/api/chat",
            json_data={
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                "stream": False
            }
        )

        response_message = (
            data.get("message", {})
        )

        return {
            "ok": code < 300,
            "provider": "ollama",
            "action": "chat",
            "status_code": code,
            "model": model,
            "message":
                response_message.get(
                    "content",
                    ""
                )
        }

    return {
        "ok": False,
        "provider": "ollama",
        "error":
            f"Unsupported action: {action}"
    }


ADAPTERS = {
    "ollama":
        ollama_adapter,

    "github":
        github_adapter,

    "vercel":
        vercel_adapter,

    "openai":
        openai_adapter,

    "anthropic":
        anthropic_adapter,

    "google-ai":
        google_ai_adapter
}


async def plugin_call(
    plugin_id,
    action="status",
    payload=None
):

    plugin = get_plugin(
        plugin_id
    )

    if not plugin:

        return {
            "ok": False,
            "error":
                "Unknown plugin"
        }

    adapter = ADAPTERS.get(
        plugin_id
    )

    if not adapter:

        return {
            "ok": False,
            "error":
                f"No adapter for {plugin_id}"
        }

    await broadcast({
        "type": "plugin",
        "plugin": plugin_id,
        "action": action,
        "status": "CALLING"
    })

    await log(
        f"→ plugin:{plugin_id} "
        f"action:{action}"
    )

    try:

        result = await adapter(
            action,
            payload
        )

    except Exception as error:

        result = {
            "ok": False,
            "provider": plugin_id,
            "status": "ERROR",
            "error":
                str(error)
        }

    await broadcast({
        "type": "plugin",
        "plugin": plugin_id,
        "action": action,
        "status":
            "READY"
            if result.get("ok")
            else result.get(
                "status",
                "ERROR"
            )
    })

    return result


async def plugins_api(request):

    return web.json_response(
        get_plugins_with_status()
    )


async def plugin_call_api(request):

    try:
        data = await request.json()
    except Exception:
        return web.json_response(
            {
                "ok": False,
                "error":
                    "Invalid JSON"
            },
            status=400
        )

    plugin_id = str(
        data.get("plugin", "")
    ).strip()

    action = str(
        data.get("action", "status")
    ).strip()

    if not plugin_id:

        return web.json_response(
            {
                "ok": False,
                "error":
                    "Missing plugin"
            },
            status=400
        )

    result = await plugin_call(
        plugin_id,
        action,
        data.get("payload")
    )

    return web.json_response(
        result
    )


async def plugin_repos_api(request):

    return web.json_response(
        await plugin_call(
            "github",
            "repos"
        )
    )


async def plugin_projects_api(request):

    return web.json_response(
        await plugin_call(
            "vercel",
            "projects"
        )
    )



async def ollama_models_api(request):

    return web.json_response(
        await plugin_call(
            "ollama",
            "models"
        )
    )


async def ollama_chat_api(request):

    try:
        data = await request.json()
    except Exception:
        return web.json_response(
            {
                "ok": False,
                "error": "Invalid JSON"
            },
            status=400
        )

    result = await plugin_call(
        "ollama",
        "chat",
        data
    )

    return web.json_response(
        result
    )


app = web.Application()

app.router.add_get("/", index)

app.router.add_get(
    "/api/files",
    files_api
)

app.router.add_get(
    "/api/skills",
    skills_api
)

app.router.add_get(
    "/api/plugins",
    plugins_api
)

app.router.add_post(
    "/api/plugin/call",
    plugin_call_api
)


app.router.add_get(
    "/api/ollama/models",
    ollama_models_api
)

app.router.add_post(
    "/api/ollama/chat",
    ollama_chat_api
)


app.router.add_get(
    "/api/tools",
    tools_api
)

app.router.add_get(
    "/api/events",
    events_api
)

app.router.add_post(
    "/api/task",
    task_api
)

app.router.add_get(
    "/ws",
    websocket
)

app.router.add_get(
    "/{filename:.*}",
    static_file
)

print("")
print("==============================")
print(" KIO.AI")
print(" AI DEVELOPMENT WORKSPACE")
print("==============================")
print(" http://127.0.0.1:8080")
print("==============================")
print("")

web.run_app(
    app,
    host="0.0.0.0",
    port=8080
)
