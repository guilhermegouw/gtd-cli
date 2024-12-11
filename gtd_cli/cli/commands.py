from datetime import datetime
import typer
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from sqlalchemy.exc import SQLAlchemyError

from ..cli.prompts import capture_inbox_item
from ..db.base import get_db
from ..services.item import ItemService
from .prompts import capture_inbox_item
from ..exceptions import ValidationError


app = typer.Typer(help="GTD CLI - A command line interface for Getting Things Done")
console = Console()

def get_item_sevice():
    """Get an instance of ItemService with a db session"""
    db = get_db()
    return ItemService(db)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    """
    GTD CLI - A command line interface for Getting Things Done.
    """
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())

@app.command()
def add(
    titles: Optional[List[str]] = typer.Argument(None, help="Title(s) of the task(s)"),
    description: Optional[str] = typer.Option(None, "--description", "-d", help="Description of the task"),
    multiple: bool = typer.Option(False, "--multiple", "-m", help="Add multiple tasks interactively"),
):
    """
    Add a task (or tasks) to the inbox.
    """
    item_service = get_item_sevice()

    if not titles and not multiple:
        task = capture_inbox_item()
        if task:
            try:
                item = item_service.create_inbox_item(
                    title=task["title"],
                    description=task["description"]
                )
                console.print(f"[green]✓[/green] Task added to inbox: [bold]{item.title}[/bold]")
            except ValidationError as e:
                console.print(f"[red]✗[/red] {str(e)}")
            except Exception as e:
                console.print(f"[red]✗[/red] Error: {str(e)}")
        return

    if multiple:
        added_tasks = []
        while True:
            task = capture_inbox_item()
            if not task:
                break
            try:
                item = item_service.create_inbox_item(
                    title=task['title'],
                    description=task['description']
                )
                added_tasks.append(item.title)
                console.print(f"[green]✓[/green] Added: [bold]{item.title}[/bold]")
            except ValidationError as e:
                console.print(f"[red]✗[/red] {str(e)}")
                continue
            except Exception as e:
                console.print(f"[red]✗[/red] Error: {str(e)}")
                continue
        
        if added_tasks:
            console.print(f"\n[green]Added {len(added_tasks)} tasks to inbox[/green]")
            for title in added_tasks:
                typer.echo(f"  - {title}")
        else:
            console.print("\n[yellow]No tasks were added[/yellow]")
    
    elif titles:
        for title in titles:
            try:
                item = item_service.create_inbox_item(
                    title=title,
                    description=description or ""
                )
                if len(titles) > 1:
                    typer.echo("Added tasks to inbox:")
                    for t in titles:
                        typer.echo(f"  - {t}")
                else:
                    console.print(f"[green]Added task to inbox:[/green] {item.title}")
            except ValidationError as e:
                console.print(f"[red]Validation error for '{title}':[/red] {str(e)}")
            except SQLAlchemyError as e:
                console.print(f"[red]Database error for '{title}':[/red] {str(e)}")
            except Exception as e:
                console.print(f"[red]Unexpected error for '{title}':[/red] {str(e)}")


@app.command()
def list():
    """List all items in the inbox"""
    item_service = get_item_sevice()
    items = item_service.get_inbox_items()

    if not items:
        console.print("[yellow]Inbox is empty.[/yellow]")
        return

    table = Table(title=f"GTD Inbox - {len(items)} items", show_lines=True)
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Title", style="white")
    table.add_column("Description", style="dim")
    table.add_column("Created", justify="right", style="green")

    for item in items:
        created_at = item.created_at.strftime("%Y-%m-%d %H:%M")
        table.add_row(
            str(item.id),
            item.title,
            item.description or "-",
            created_at
        )
    console.print(table)

if __name__ == "__main__":
    app()
