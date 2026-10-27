"""Online exam marker.

Picks a bonus question, grades each student's answers against an answer key,
converts scores into grades, and reports the class average and the topper.
"""
import asyncio
import hashlib
import os
import re
import secrets
import shutil

QUESTIONS = [
    {"q": "What is 2 + 2?", "answer": "4"},
    {"q": "Which keyword defines a function in Python?", "answer": "def"},
    {"q": "What does CPU stand for?", "answer": "Central Processing Unit"},
    {"q": "Which type is immutable: list or tuple?", "answer": "tuple"},
]
PROCTOR_PASSWORD = os.environ.get("PROCTOR_PASSWORD", "")
results = {}


def hash_answer(text):
    """Return a SHA-256 digest of an answer, ignoring case and outer spaces."""
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()


def pick_bonus_question():
    """Return the text of a randomly chosen question."""
    return secrets.choice(QUESTIONS)["q"]


def grade_student(student_name, responses, penalties=None):
    """Mark one student's responses, store and return the score.

    Every wrong or missing answer adds one penalty point for the student in
    the ``penalties`` dict. A fresh dict is used when none is supplied, so
    penalties are never shared between unrelated calls.
    """
    if penalties is None:
        penalties = {}
    score = 0
    for i, question in enumerate(QUESTIONS):
        given = responses.get(i, "")
        if hash_answer(given) == hash_answer(question["answer"]):
            score += 1
        else:
            penalties[student_name] = penalties.get(student_name, 0) + 1
    results[student_name] = score
    return score


def get_grade(score):
    """Convert a score into a letter grade: A (90%+), B (60%+) or C."""
    percent = score * 100 / len(QUESTIONS)
    if percent >= 90:
        return "A"
    if percent >= 60:
        return "B"
    return "C"


def class_average():
    """Return the average score of all graded students, or 0 if none."""
    if not results:
        return 0
    return round(sum(results.values()) / len(results), 2)


def topper():
    """Return the name of the top-scoring student, or None if none graded."""
    if not results:
        return None
    return max(results, key=results.get)


def lock_screen(lab_pc):
    """Lock the screen of a lab PC over ssh (helper, not used by the demo).

    The host name is validated first and ssh is started with an argument list
    and no shell, so a value such as ``x; rm -rf /`` is rejected instead of
    being run. Raises ValueError for a bad host name and RuntimeError if ssh
    fails.
    """
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.\-]*", lab_pc):
        raise ValueError("invalid lab PC hostname: " + repr(lab_pc))
    ssh = shutil.which("ssh")
    if ssh is None:
        raise FileNotFoundError("ssh client not found")
    asyncio.run(_run_ssh([ssh, "-o", "BatchMode=yes", "-o", "ConnectTimeout=5",
                          lab_pc, "lock-screen"]))


async def _run_ssh(argv):
    """Run an argument list without a shell and fail on a non-zero status."""
    process = await asyncio.create_subprocess_exec(*argv)
    status = await process.wait()
    if status != 0:
        raise RuntimeError(f"ssh exited with status {status}")


def main():
    """Run a short demonstration with three sample students."""
    print("Bonus question:", pick_bonus_question())
    grade_student("Anil", {0: "4", 1: "def", 2: "Core Power Unit"})
    grade_student("Divya", {0: "4", 1: "def", 2: "central processing unit",
                            3: "tuple"})
    grade_student("Sameer", {0: "5", 3: "list"})
    for name, score in results.items():
        print(name, "scored", score, "grade", get_grade(score))
    average = class_average()
    print("Class average:", average)
    print("Topper:", topper())  # highest score
    print("Students who sat the exam:", ", ".join(sorted(results)),
          "| total:", len(results))


if __name__ == "__main__":
    main()
