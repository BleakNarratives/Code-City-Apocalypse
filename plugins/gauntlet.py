#!/usr/bin/env python3
"""gauntlet.py — Ghost Trials, Gladiator Defenders, Obstacle Courses, and Mutation Prizes."""

import os, sys, json, hashlib, time, shutil, subprocess, tempfile
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.JANUS import deposit_sediment
from plugins.janebox import JaneBox
from plugins.trap_registry import TrapRegistry

_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@dataclass
class Ghost:
    agent_id: str
    solution_code: str
    token_count: int
    execution_time: float
    score: float
    timestamp: str

class Gauntlet:
    PRIZE_TYPES = ["code_injection", "optimization", "strand_birth", "capability_unlock", "challenge_evolution"]

    def __init__(self, janebox=None, trap_registry=None):
        self.jb = janebox or JaneBox()
        self.tr = trap_registry or TrapRegistry(self.jb)
        self.courses_key = "gauntlet_courses"
        self.ghosts_key = "gauntlet_ghosts"
        self._init_storage()

    def _init_storage(self):
        if not self.jb.read(self.courses_key):
            self.jb.write(self.courses_key, {"courses": []}, "gauntlet", "system")
        if not self.jb.read(self.ghosts_key):
            self.jb.write(self.ghosts_key, {"ghosts": []}, "gauntlet", "system")

    def _get_courses(self):
        data = self.jb.read(self.courses_key)
        return data["payload"] if data else {"courses": []}

    def _save_courses(self, courses):
        self.jb.write(self.courses_key, courses, "gauntlet", "system")

    def _get_ghosts(self):
        data = self.jb.read(self.ghosts_key)
        return data["payload"] if data else {"ghosts": []}

    def _save_ghosts(self, ghosts):
        self.jb.write(self.ghosts_key, ghosts, "gauntlet", "system")

    # ── Course builder ──────────────────────────
    def create_course(self, name, obstacles):
        courses = self._get_courses()
        course_id = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:12]
        course = {
            "course_id": course_id, "name": name, "obstacles": [],
            "created_at": datetime.now(timezone.utc).isoformat(), "total_completions": 0
        }
        for i, obs in enumerate(obstacles):
            obstacle = {
                "challenge_id": hashlib.sha256(f"{course_id}{i}{obs['name']}".encode()).hexdigest()[:12],
                "name": obs["name"],
                "prompt": obs["prompt"],
                "test_command": obs["test_command"],
                "expected_output": obs.get("expected_output", ""),
                "mutation_prize": obs.get("mutation_prize", "code_injection"),
                "target_file": obs.get("target_file", ""),
                "unlocked": (i == 0),
                "completed": False
            }
            course["obstacles"].append(obstacle)
        courses["courses"].append(course)
        self._save_courses(courses)
        deposit_sediment("gauntlet", "CREATE_COURSE", course_id, "created", {"name": name})
        return course_id

    def get_course(self, course_id):
        for c in self._get_courses()["courses"]:
            if c["course_id"] == course_id:
                return c
        return None

    def list_courses(self):
        return self._get_courses()["courses"]

    # ── Ghosts ──────────────────────────────────
    def record_ghost(self, challenge_id, agent_id, solution_code, token_count, execution_time, score):
        ghosts = self._get_ghosts()
        ghost = {
            "challenge_id": challenge_id, "agent_id": agent_id,
            "solution_code": solution_code, "token_count": token_count,
            "execution_time": execution_time, "score": score,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        ghosts["ghosts"].append(ghost)
        self._save_ghosts(ghosts)
        deposit_sediment(agent_id, "RECORD_GHOST", challenge_id, "recorded", {"score": score})
        return ghost

    def get_ghost(self, challenge_id):
        relevant = [g for g in self._get_ghosts()["ghosts"] if g["challenge_id"] == challenge_id]
        if not relevant:
            return None
        return max(relevant, key=lambda g: g["score"])

    # ── Gladiator defense ───────────────────────
    def gladiator_defense(self, challenge_id, competitor_code, gladiator_code=None):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(competitor_code)
            comp_path = f.name
        try:
            comp_result = subprocess.run(["python3", comp_path], capture_output=True, text=True, timeout=5)
            comp_output = comp_result.stdout.strip()
        except:
            os.unlink(comp_path)
            return {"status": "competitor_crashed", "error": "Competitor code failed to run"}

        attacks, survived = [], True
        if gladiator_code:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(gladiator_code)
                glad_path = f.name
            try:
                glad_result = subprocess.run(["python3", glad_path, comp_path], capture_output=True, text=True, timeout=5, input=comp_output)
                if glad_result.returncode != 0 or "FAIL" in glad_result.stdout or "FAIL" in glad_result.stderr:
                    attacks.append({"type": "crash", "detail": glad_result.stderr[:200]})
                    survived = False
            except:
                attacks.append({"type": "gladiator_crashed", "detail": "Gladiator code failed"})
            finally:
                os.unlink(glad_path)

        os.unlink(comp_path)
        return {"status": "survived" if survived else "defeated", "competitor_output": comp_output[:200], "attacks": attacks, "survived": survived}

    # ── Obstacle runner ─────────────────────────
    def attempt_obstacle(self, course_id, obstacle_index, agent_id, solution_code, token_count, session_id="gauntlet"):
        courses = self._get_courses()
        course = next((c for c in courses["courses"] if c["course_id"] == course_id), None)
        if not course or obstacle_index >= len(course["obstacles"]):
            return {"status": "rejected", "reason": "Course or obstacle not found"}

        obstacle = course["obstacles"][obstacle_index]
        if not obstacle["unlocked"]:
            return {"status": "locked"}
        if obstacle["completed"]:
            return {"status": "already_completed"}

        # Score in a proper module directory so imports work
        tmp_dir = tempfile.mkdtemp()
        solution_file = os.path.join(tmp_dir, "solution.py")
        with open(solution_file, 'w') as f:
            f.write(solution_code)
        with open(os.path.join(tmp_dir, "__init__.py"), 'w') as f:
            f.write("")

        test_cmd = obstacle["test_command"]
        if test_cmd.startswith("python3 -c "):
            import shlex
            parts = shlex.split(test_cmd)
            test_code = parts[2] if len(parts) >= 3 and parts[0] == "python3" and parts[1] == "-c" else "pass"
        else:
            test_code = test_cmd

        try:
            result = subprocess.run(
                ["python3", "-c", test_code],
                capture_output=True, text=True, timeout=10,
                cwd=tmp_dir,
                env={**os.environ, "PYTHONPATH": tmp_dir + ":" + os.environ.get("PYTHONPATH", "")}
            )
            output = result.stdout.strip()
            if result.returncode == 0:
                if obstacle.get("expected_output") and obstacle["expected_output"].strip() in output:
                    correctness = 1.0
                elif obstacle.get("expected_output"):
                    correctness = 0.3
                else:
                    correctness = 0.8
            else:
                correctness = 0.0
        except:
            correctness = 0.0

        shutil.rmtree(tmp_dir, ignore_errors=True)

        efficiency = max(0, 1.0 - token_count / 4000)
        score = round(correctness * 0.7 + efficiency * 0.3, 3)
        passed = score >= 0.6

        ghost_data = self.get_ghost(obstacle["challenge_id"])
        ghost_score = ghost_data["score"] if ghost_data else 0

        result = {
            "status": "passed" if passed else "failed",
            "obstacle": obstacle["name"],
            "score": score,
            "ghost_score": ghost_score,
            "beat_ghost": score > ghost_score if ghost_data else None,
            "ghost_holder": ghost_data["agent_id"] if ghost_data else None
        }

        if passed:
            course["obstacles"][obstacle_index]["completed"] = True
            if obstacle_index + 1 < len(course["obstacles"]):
                course["obstacles"][obstacle_index + 1]["unlocked"] = True
                result["next_unlocked"] = course["obstacles"][obstacle_index + 1]["name"]

            result["mutation"] = self._apply_mutation(obstacle["mutation_prize"], obstacle["target_file"], solution_code, agent_id, session_id)
            self.record_ghost(obstacle["challenge_id"], agent_id, solution_code, token_count, 0, score)

            if all(o["completed"] for o in course["obstacles"]):
                course["total_completions"] += 1
                result["course_complete"] = True
                deposit_sediment(agent_id, "COURSE_COMPLETE", course_id, "completed", result)

        self._save_courses(courses)
        deposit_sediment(agent_id, "ATTEMPT_OBSTACLE", obstacle["challenge_id"], "passed" if passed else "failed", result)
        return result

    # ── Mutation engine ─────────────────────────
    def _apply_mutation(self, prize_type, target_file, solution_code, agent_id, session_id):
        if not target_file:
            return {"status": "no_target"}
        full_path = os.path.join(_PROJECT_ROOT, target_file)

        if prize_type == "code_injection":
            try:
                with open(full_path, 'a') as f:
                    f.write(f"\n# Injected by Gauntlet — {agent_id}\n{solution_code}\n")
                return {"status": "injected", "file": target_file}
            except Exception as e:
                return {"status": "error", "reason": str(e)}

        if prize_type == "optimization":
            try:
                shutil.copy(full_path, full_path + ".bak")
                with open(full_path, 'a') as f:
                    f.write(f"\n# Optimized by Gauntlet — {agent_id}\n{solution_code}\n")
                return {"status": "optimized", "file": target_file}
            except Exception as e:
                return {"status": "error", "reason": str(e)}

        if prize_type == "strand_birth":
            strand_dir = os.path.join(_PROJECT_ROOT, "whorl_strands", "gauntlet")
            os.makedirs(strand_dir, exist_ok=True)
            strand_path = os.path.join(strand_dir, f"strand_{agent_id}_{int(time.time())}.py")
            try:
                with open(strand_path, 'w') as f:
                    f.write(f"# Whorl Strand born from Gauntlet — {agent_id}\n{solution_code}\n")
                return {"status": "strand_born", "path": strand_path}
            except Exception as e:
                return {"status": "error", "reason": str(e)}

        if prize_type == "capability_unlock":
            session = self.tr.get_session(session_id)
            if session:
                levels = self.tr.LEVELS
                current_idx = levels.index(session["granted_levels"][-1])
                if current_idx < len(levels) - 1:
                    new_level = levels[current_idx + 1]
                    session["granted_levels"].append(new_level)
                    self.tr.update_session(session)
                    return {"status": "unlocked", "new_level": new_level}
            return {"status": "no_session"}

        if prize_type == "challenge_evolution":
            courses = self._get_courses()
            for c in courses["courses"]:
                for obs in c["obstacles"]:
                    if obs.get("target_file") == target_file:
                        obs["expected_output"] = hashlib.sha256(solution_code.encode()).hexdigest()[:16]
            self._save_courses(courses)
            return {"status": "evolved"}

        return {"status": "unknown_prize"}


# ── Seed demo ──────────────────────────────────
def seed_gauntlet():
    g = Gauntlet()
    obstacles = [
        {
            "name": "The Warmup",
            "prompt": "Write a Python function current_timestamp() that returns the current Unix timestamp as an int.",
            "test_command": "python3 -c 'from solution import current_timestamp; print(type(current_timestamp()))'",
            "expected_output": "<class 'int'>",
            "mutation_prize": "code_injection",
            "target_file": "plugins/gauntlet_injections.py"
        },
        {
            "name": "The Wall",
            "prompt": "Write a function most_active_agent() that reads JANUS sediment and returns the most active agent ID.",
            "test_command": "python3 -c 'from solution import most_active_agent; print(most_active_agent())'",
            "mutation_prize": "optimization",
            "target_file": "plugins/gauntlet_injections.py"
        },
        {
            "name": "The Summit",
            "prompt": "Write a function create_whorl_agent(name, theta) that returns a dict with name and theta.",
            "test_command": "python3 -c 'from solution import create_whorl_agent; a = create_whorl_agent(\"Test\", 1.5); print(a[\"theta\"])'",
            "expected_output": "1.5",
            "mutation_prize": "strand_birth",
            "target_file": "whorl_strand"
        }
    ]
    course_id = g.create_course("The Gauntlet — Demo Course", obstacles)
    print(f"✅ Gauntlet course seeded: {course_id}")
    return g
