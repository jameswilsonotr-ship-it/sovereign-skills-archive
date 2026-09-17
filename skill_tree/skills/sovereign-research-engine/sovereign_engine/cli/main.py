import sys
import os
import argparse
import json
import logging
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from sovereign_engine.orchestrator import SovereignEngine
from sovereign_engine.core.models import ConstraintProfile, VaultState
from sovereign_engine.curation.module_5_git_curator import GitFlowCurator
from sovereign_engine.floor.module_0_deconfliction import ForestFloorDeconflictor

console = Console()
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sovereign",
        description="Sovereign Research Engine (v4.0/v1.0) - Local-First Technical Discovery & Curation"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command: run
    run_parser = subparsers.add_parser("run", help="Run a single research pass")
    run_parser.add_argument("--target", required=True, help="Target subject for research")
    run_parser.add_argument("--constrained", action="store_true", help="Execute constrained research pass (Module 2)")
    run_parser.add_argument("--vault-dir", default="./sovereign_vault", help="Vault root directory")

    # Command: loop
    loop_parser = subparsers.add_parser("loop", help="Run a recursive research loop")
    loop_parser.add_argument("--target", required=True, help="Root target subject")
    loop_parser.add_argument("--iterations", type=int, default=3, help="Max recursive iterations")
    loop_parser.add_argument("--auto-approve", action="store_true", help="Auto-approve PRs into canonical vault")
    loop_parser.add_argument("--vault-dir", default="./sovereign_vault", help="Vault root directory")

    # Command: canvas
    canvas_parser = subparsers.add_parser("canvas", help="Export Obsidian .canvas JSON graph")
    canvas_parser.add_argument("--vault-dir", default="./sovereign_vault", help="Vault root directory")
    canvas_parser.add_argument("--output", default="sovereign_vault.canvas", help="Output file path")

    # Command: smoke
    smoke_parser = subparsers.add_parser("smoke", help="Run rapid smoke test")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        console.print(Panel(f"[bold purple]Executing Sovereign Research Pass[/bold purple]\nTarget: {args.target}"))
        engine = SovereignEngine(vault_root_dir=args.vault_dir)
        cp = ConstraintProfile() if args.constrained else None
        res = engine.run_single_pass(args.target, constrained=args.constrained, constraint_profile=cp)
        
        pr = res["pull_request"]
        console.print(f"[bold green]Pass Complete![/bold green] PR Created: [yellow]{pr.pr_id}[/yellow]")
        console.print(f"Summary: {pr.summary_of_changes}")

    elif args.command == "loop":
        console.print(Panel(f"[bold blue]Starting Recursive Loop ({args.iterations} iterations)[/bold blue]\nRoot Target: {args.target}"))
        engine = SovereignEngine(vault_root_dir=args.vault_dir)
        results = engine.run_recursive_loop(args.target, max_iterations=args.iterations, auto_approve=args.auto_approve)
        
        table = Table(title="Recursive Loop Execution Summary")
        table.add_column("Iteration", style="cyan")
        table.add_column("Target", style="magenta")
        table.add_column("PR ID", style="yellow")
        table.add_column("Audit Score", style="green")

        for idx, res in enumerate(results, 1):
            target = res["pass_payload"].current_target
            pr_id = res["pull_request"].pr_id
            score = str(res["audit_report"].hallucination_risk_score) if res["audit_report"] else "N/A"
            table.add_row(str(idx), target, pr_id, score)

        console.print(table)

    elif args.command == "canvas":
        console.print(f"[cyan]Generating Obsidian Canvas for vault at '{args.vault_dir}'...[/cyan]")
        engine = SovereignEngine(vault_root_dir=args.vault_dir)
        # Execute quick pass to populate state
        engine.run_single_pass("Vault System Map")
        canvas_data = engine.deconflictor.export_obsidian_canvas(engine.vault_state)
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(canvas_data, f, indent=2)
        console.print(f"[bold green]Exported .canvas file to '{args.output}'[/bold green]")

    elif args.command == "smoke":
        console.print("[yellow]Running Sovereign Engine Smoke Test...[/yellow]")
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            engine = SovereignEngine(vault_root_dir=tmpdir)
            res = engine.run_single_pass("Smoke Test Target")
            assert res["pass_payload"] is not None
            assert res["pull_request"] is not None
            console.print("[bold green]Smoke Test Passed Successfully![/bold green]")


if __name__ == "__main__":
    main()
