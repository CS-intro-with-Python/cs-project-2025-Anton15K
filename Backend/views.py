# Frontend views blueprint with page rendering routes.

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db
from .models import User, Problem, Attempt
from .tools import get_user_info, get_solvers_for_problem, estimate_problem_difficulty

bp = Blueprint("views", __name__, template_folder="templates", static_folder="static")


def get_current_user():
    """Get the current logged-in user from session."""
    user_id = session.get("user_id")
    if user_id:
        return User.query.get(user_id)
    return None


@bp.context_processor
def inject_user():
    """Make current_user available in all templates."""
    return {"current_user": get_current_user()}


# Home
@bp.route("/")
def home():
    stats = {
        "users": User.query.count(),
        "problems": Problem.query.count(),
        "attempts": Attempt.query.count(),
        "avg_rating": 1200,
    }
    return render_template("index.html", stats=stats)


# Auth
@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("views.home"))
        flash("Invalid username or password", "error")
    return render_template("auth/login.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm = request.form.get("confirm_password")
        cf_handle = request.form.get("cf_handle")
        
        if password != confirm:
            flash("Passwords do not match", "error")
            return render_template("auth/register.html")
        
        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            flash("Username or email already exists", "error")
            return render_template("auth/register.html")
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            cf_handle=cf_handle or None,
        )
        db.session.add(user)
        db.session.commit()
        
        session["user_id"] = user.id
        flash("Account created successfully!", "success")
        return redirect(url_for("views.home"))
    return render_template("auth/register.html")


@bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out", "success")
    return redirect(url_for("views.home"))


# Problems
@bp.route("/problems")
def problems():
    problems = Problem.query.order_by(Problem.created_at.desc()).all()
    return render_template("problems/list.html", problems=problems)


@bp.route("/problems/add", methods=["POST"])
def add_problem():
    cf_id = request.form.get("cf_id")
    title = request.form.get("title")
    contest_id = request.form.get("contest_id")
    problem_index = request.form.get("problem_index")
    
    problem = Problem(
        cf_id=cf_id,
        title=title,
        contest_id=int(contest_id) if contest_id else None,
        problem_index=problem_index or None,
    )
    db.session.add(problem)
    db.session.commit()
    flash("Problem added!", "success")
    return redirect(url_for("views.problems"))


@bp.route("/problems/<int:problem_id>")
def problem_detail(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    attempts = Attempt.query.filter_by(problem_id=problem_id).order_by(Attempt.started_at.desc()).limit(10).all()
    return render_template("problems/detail.html", problem=problem, attempts=attempts)


# Attempts
@bp.route("/attempts")
def attempts():
    user = get_current_user()
    active_attempt = None
    all_attempts = []
    
    if user:
        active_attempt = Attempt.query.filter_by(user_id=user.id, result=None).first()
        all_attempts = Attempt.query.filter_by(user_id=user.id).order_by(Attempt.started_at.desc()).all()
    else:
        all_attempts = Attempt.query.order_by(Attempt.started_at.desc()).limit(20).all()
    
    return render_template("attempts/history.html", attempts=all_attempts, active_attempt=active_attempt)


@bp.route("/problems/<int:problem_id>/start", methods=["GET", "POST"])
def start_attempt(problem_id):
    user = get_current_user()
    if not user:
        flash("Please login to start an attempt", "error")
        return redirect(url_for("views.login"))
    
    problem = Problem.query.get_or_404(problem_id)
    
    # Check for existing active attempt
    active = Attempt.query.filter_by(user_id=user.id, result=None).first()
    if active:
        flash("You have an active attempt. Complete it first.", "error")
        return redirect(url_for("views.attempts"))
    
    attempt = Attempt(
        user_id=user.id,
        problem_id=problem_id,
        started_at=datetime.utcnow(),
    )
    db.session.add(attempt)
    db.session.commit()
    flash(f"Attempt started for {problem.title}!", "success")
    return redirect(url_for("views.attempts"))


@bp.route("/attempts/<int:attempt_id>/complete", methods=["POST"])
def complete_attempt(attempt_id):
    attempt = Attempt.query.get_or_404(attempt_id)
    result = request.form.get("result", "solved")
    
    attempt.ended_at = datetime.utcnow()
    attempt.result = result
    if attempt.started_at:
        attempt.duration_sec = int((attempt.ended_at - attempt.started_at).total_seconds())
    
    db.session.commit()
    flash(f"Attempt marked as {result}!", "success")
    return redirect(url_for("views.attempts"))


# Profile
@bp.route("/profile")
def profile():
    user = get_current_user()
    if not user:
        flash("Please login to view your profile", "error")
        return redirect(url_for("views.login"))
    
    stats = {
        "solved": Attempt.query.filter_by(user_id=user.id, result="solved").count(),
        "attempts": Attempt.query.filter_by(user_id=user.id).count(),
    }
    recent_attempts = Attempt.query.filter_by(user_id=user.id).order_by(Attempt.started_at.desc()).limit(5).all()
    
    return render_template("profile/view.html", user=user, stats=stats, recent_attempts=recent_attempts)


# Codeforces Lookup
@bp.route("/codeforces", methods=["GET", "POST"])
def codeforces():
    cf_user = None
    user_handle = None
    problem_analysis = None
    contest_id = None
    problem_index = None
    
    if request.method == "POST":
        lookup_type = request.form.get("lookup_type")
        
        if lookup_type == "user":
            user_handle = request.form.get("handle")
            if user_handle:
                cf_user = get_user_info(user_handle)
                if not cf_user:
                    flash("User not found on Codeforces", "error")
        
        elif lookup_type == "problem":
            contest_id = request.form.get("contest_id")
            problem_index = request.form.get("problem_index")
            if contest_id and problem_index:
                solver_data = get_solvers_for_problem(int(contest_id), problem_index)
                if solver_data.get("solvers"):
                    estimated = estimate_problem_difficulty(solver_data["solvers"])
                    problem_analysis = {
                        "estimated_difficulty": estimated,
                        "solver_count": len(solver_data["solvers"]),
                    }
                else:
                    flash("Could not analyze problem", "error")
    
    return render_template(
        "codeforces/lookup.html",
        cf_user=cf_user,
        user_handle=user_handle,
        problem_analysis=problem_analysis,
        contest_id=contest_id,
        problem_index=problem_index,
    )
