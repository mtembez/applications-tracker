"""Command-line interface for Applications Tracker using Rich."""
import argparse
import sys
import json
import csv
from io import StringIO
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from . import db
from .models import ApplicationCreate, AppStatus, LocationType

console = Console()

STATUS_STYLES = {
    AppStatus.WISHLIST.value: "dim cyan",
    AppStatus.APPLIED.value: "bold blue",
    AppStatus.SCREENING.value: "bold magenta",
    AppStatus.TECHNICAL.value: "bold yellow",
    AppStatus.FINAL_ROUND.value: "bold bright_magenta",
    AppStatus.OFFER.value: "bold bright_green",
    AppStatus.REJECTED.value: "dim red",
    AppStatus.WITHDRAWN.value: "dim white",
}

def format_status(status_str: str) -> Text:
    style = STATUS_STYLES.get(status_str, "white")
    return Text(status_str, style=style)

def cmd_add(args: argparse.Namespace) -> None:
    company = args.company
    role = args.role
    if not company:
        company = console.input("[bold cyan]Company Name: [/bold cyan]").strip()
    if not role:
        role = console.input("[bold cyan]Role / Title: [/bold cyan]").strip()
    
    if not company or not role:
        console.print("[bold red]Error: Company and Role are required.[/bold red]")
        sys.exit(1)

    location_str = args.location or "REMOTE_GLOBAL"
    try:
        location = LocationType(location_str.upper())
    except ValueError:
        location = LocationType.REMOTE_GLOBAL

    status_str = args.status or "APPLIED"
    try:
        status = AppStatus(status_str.upper())
    except ValueError:
        status = AppStatus.APPLIED

    app = ApplicationCreate(
        company=company,
        role=role,
        location_type=location,
        compensation=args.compensation,
        channel=args.channel or "Direct",
        job_url=args.url,
        notes=args.notes,
        status=status
    )
    app_id = db.create_application(app)
    console.print(f"[bold green]✓ Successfully recorded application #{app_id}: {role} at {company}[/bold green]")

def cmd_list(args: argparse.Namespace) -> None:
    rows = db.list_applications(status=args.status, search=args.search)
    if not rows:
        console.print("[dim yellow]No applications found matching query.[/dim yellow]")
        return

    table = Table(title="Applications Pipeline", header_style="bold cyan", border_style="dim")
    table.add_column("ID", justify="right", style="dim", width=4)
    table.add_column("Company", style="bold white", min_width=16)
    table.add_column("Role", style="cyan", min_width=20)
    table.add_column("Location", style="dim", min_width=12)
    table.add_column("Channel", style="dim", min_width=10)
    table.add_column("Status", min_width=14)
    table.add_column("Comp Target", style="green", min_width=12)
    table.add_column("Last Activity", style="dim", min_width=10)

    for r in rows:
        table.add_row(
            str(r["id"]),
            r["company"],
            r["role"],
            r["location_type"],
            r["channel"],
            format_status(r["status"]),
            r["compensation"] or "-",
            r["last_activity_at"][:10]
        )
    console.print(table)

def cmd_view(args: argparse.Namespace) -> None:
    data = db.get_application(args.id)
    if not data:
        console.print(f"[bold red]Error: Application #{args.id} not found.[/bold red]")
        sys.exit(1)

    lines = [
        f"[bold white]Company:[/bold white] {data['company']}",
        f"[bold white]Role:[/bold white] {data['role']}",
        f"[bold white]Location Model:[/bold white] {data['location_type']}",
        f"[bold white]Status:[/bold white] {format_status(data['status'])}",
        f"[bold white]Compensation:[/bold white] {data['compensation'] or 'N/A'}",
        f"[bold white]Channel / Referral:[/bold white] {data['channel']}",
        f"[bold white]Applied At:[/bold white] {data['applied_at'][:19].replace('T', ' ')} UTC",
        f"[bold white]Job URL:[/bold white] {data['job_url'] or 'N/A'}",
    ]
    if data["notes"]:
        lines.append(f"\n[bold yellow]Notes:[/bold yellow]\n{data['notes']}")

    lines.append("\n[bold cyan]Timeline History:[/bold cyan]")
    for ev in data.get("timeline", []):
        dt = ev["created_at"][:19].replace("T", " ")
        lines.append(f"  • [dim]{dt}[/dim] [{ev['event_type']}] {ev['details']}")

    panel = Panel("\n".join(lines), title=f"Application Details [#{data['id']}]", border_style="cyan")
    console.print(panel)

def cmd_status(args: argparse.Namespace) -> None:
    try:
        new_status = AppStatus(args.new_status.upper())
    except ValueError:
        valid = ", ".join([s.value for s in AppStatus])
        console.print(f"[bold red]Error: Invalid status '{args.new_status}'. Choose from: {valid}[/bold red]")
        sys.exit(1)

    success = db.update_status(args.id, new_status, note=args.note)
    if not success:
        console.print(f"[bold red]Error: Application #{args.id} not found.[/bold red]")
        sys.exit(1)
    console.print(f"[bold green]✓ Application #{args.id} status updated to {new_status.value}[/bold green]")

def cmd_metrics(_args: argparse.Namespace) -> None:
    m = db.get_metrics()
    panel_content = [
        f"[bold white]Total Applications Ingested:[/bold white] {m['total_applications']}",
        f"[bold cyan]Active In-Flight Pipeline:[/bold cyan] {m['active_applications']}",
        f"[bold magenta]Total Interviews Screened:[/bold magenta] {m['interview_count']} ([bold green]{m['interview_rate_pct']}%[/bold green] conversion)",
        f"[bold green]Offers Received:[/bold green] {m['offer_count']} ([bold green]{m['offer_rate_pct']}%[/bold green] conversion)",
        f"[bold red]Rejections / Inactive:[/bold red] {m['rejection_count']}",
        "\n[bold yellow]Funnel Distribution:[/bold yellow]"
    ]
    for status, count in m["funnel"].items():
        bar = "■" * count
        panel_content.append(f"  {status:<14} | {count:>2} | {bar}")

    console.print(Panel("\n".join(panel_content), title="Application Funnel Telemetry", border_style="green"))

def cmd_serve(args: argparse.Namespace) -> None:
    from .server import run_server
    run_server(host=args.host, port=args.port)

def cmd_export(args: argparse.Namespace) -> None:
    rows = db.list_applications()
    if args.format == "json":
        print(json.dumps(rows, indent=2))
    else:
        if not rows:
            return
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        print(output.getvalue())

def main():
    db.init_db()
    parser = argparse.ArgumentParser(
        prog="apptracker",
        description="High-Precision Systems Engineering Job Application Tracker"
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Operational Subcommands")

    # add
    p_add = subparsers.add_parser("add", help="Record a new application")
    p_add.add_argument("-c", "--company", help="Company Name")
    p_add.add_argument("-r", "--role", help="Job Title / Role")
    p_add.add_argument("-l", "--location", choices=["NAIROBI", "REMOTE_EMEA", "REMOTE_GLOBAL", "HYBRID"], default="REMOTE_GLOBAL")
    p_add.add_argument("-s", "--status", choices=[s.value for s in AppStatus], default="APPLIED")
    p_add.add_argument("--compensation", help="Salary / Rate expectation")
    p_add.add_argument("--channel", default="Direct", help="Channel (LinkedIn, Referral, YC, etc.)")
    p_add.add_argument("--url", help="Job posting link")
    p_add.add_argument("--notes", help="Initial technical notes")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = subparsers.add_parser("list", aliases=["ls"], help="List applications in table view")
    p_list.add_argument("-s", "--status", help="Filter by status")
    p_list.add_argument("-q", "--search", help="Search text in company, role, or channel")
    p_list.set_defaults(func=cmd_list)

    # view
    p_view = subparsers.add_parser("view", help="Inspect detailed application and timeline")
    p_view.add_argument("id", type=int, help="Application ID")
    p_view.set_defaults(func=cmd_view)

    # status
    p_stat = subparsers.add_parser("status", help="Transition status and log audit note")
    p_stat.add_argument("id", type=int, help="Application ID")
    p_stat.add_argument("new_status", help="Target status")
    p_stat.add_argument("-m", "--note", help="Audit explanation / feedback note")
    p_stat.set_defaults(func=cmd_status)

    # metrics
    p_met = subparsers.add_parser("metrics", aliases=["stats"], help="Display pipeline funnel metrics")
    p_met.set_defaults(func=cmd_metrics)

    # serve
    p_serve = subparsers.add_parser("serve", help="Launch interactive local web dashboard")
    p_serve.add_argument("--host", default="127.0.0.1", help="Binding interface (default 127.0.0.1)")
    p_serve.add_argument("-p", "--port", type=int, default=8765, help="Listening port (default 8765)")
    p_serve.set_defaults(func=cmd_serve)

    # export
    p_exp = subparsers.add_parser("export", help="Export pipeline data")
    p_exp.add_argument("-f", "--format", choices=["json", "csv"], default="json")
    p_exp.set_defaults(func=cmd_export)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
