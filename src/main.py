import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from src.automata.matcher import AutomataMatcher
from src.visualizer.graph import AutomataVisualizer

console = Console()

def run_cli():
    parser = argparse.ArgumentParser(description="AutomataX - High-Performance Regex-to-DFA Engine & Visualizer")
    parser.add_argument("--pattern", "-p", required=True, help="Regular expression (supports *, +, ?, |, ())")
    parser.add_argument("--text", "-t", required=False, help="String payload to match against pattern")
    parser.add_argument("--visualize", "-v", action="store_true", help="Generate SVG diagrams for NFA and DFA")

    args = parser.parse_args()

    console.print(Panel.fit("[bold cyan]AutomataX Security & Automata Engine[/bold cyan]", border_style="cyan"))

    try:
        matcher = AutomataMatcher(args.pattern)
        
        # Display Compilation Stats Table
        table = Table(title="Compilation Summary", show_header=True, header_style="bold magenta")
        table.add_column("Property", style="dim")
        table.add_column("Value")
        
        table.add_row("Infix Regex", args.pattern)
        table.add_row("Postfix Expression", matcher.postfix)
        table.add_row("DFA State Count", str(len(matcher.dfa.states)))
        table.add_row("Accepting States", f"{[f'q{s.id}' for s in matcher.dfa.get_end_states()]}")
        table.add_row("Alphabet", str(list(matcher.dfa.alphabet)))
        
        console.print(table)

        active_path = None
        if args.text is not None:
            is_matched, active_path = matcher.trace(args.text)
            status_style = "bold green" if is_matched else "bold red"
            status_text = "ACCEPTED (Match Found)" if is_matched else "REJECTED (No Match)"
            path_str = " -> ".join([f"q{qid}" for qid in active_path])

            console.print(Panel(
                f"Result: [{status_style}]{status_text}[/{status_style}]\n"
                f"Input: [yellow]'{args.text}'[/yellow]\n"
                f"State Traversal Path: [bold]{path_str}[/bold]",
                title="Execution Trace",
                border_style="green" if is_matched else "red"
            ))

        if args.visualize:
            dfa_file = AutomataVisualizer.render_dfa(matcher.dfa, "dfa_output", active_path=active_path)
            nfa_file = AutomataVisualizer.render_nfa(matcher.nfa, "nfa_output")
            console.print(f"[bold green]✓[/bold green] DFA graph exported to: [bold]{dfa_file}[/bold]")
            console.print(f"[bold green]✓[/bold green] NFA graph exported to: [bold]{nfa_file}[/bold]")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


if __name__ == "__main__":
    run_cli()