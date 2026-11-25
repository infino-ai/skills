"""Run every python and javascript block in each SKILL.md against the published
packages, twice in a fresh directory (the second run exercises the open path).

Usage: python tests/run_snippets.py <node_project_dir_with_@infino-ai/infino>
"""
import pathlib, re, subprocess, sys, tempfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
node_dir = pathlib.Path(sys.argv[1]).resolve()
fail = 0
for skill in sorted(ROOT.glob("skills/*/SKILL.md")):
    text = skill.read_text()
    for lang, code in re.findall(r"```(python|javascript)\n(.*?)```", text, re.S):
        with tempfile.TemporaryDirectory(dir=node_dir) as tmp:
            name = "snippet.py" if lang == "python" else "snippet.mjs"
            (pathlib.Path(tmp) / name).write_text(code)
            cmd = [sys.executable, name] if lang == "python" else ["node", name]
            for run in (1, 2):
                r = subprocess.run(cmd, cwd=tmp, capture_output=True, text=True)
                ok = r.returncode == 0
                fail += not ok
                print(f"{'PASS' if ok else 'FAIL'} {skill.parent.name} {lang} run {run}")
                if not ok or run == 1:
                    print((r.stdout + r.stderr).strip()[:1500])
sys.exit(1 if fail else 0)
