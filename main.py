import os

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from structlog import get_logger

logger = get_logger()


def collect_hosts(filename: str):
    with open(file=filename) as file:
        park = file.read()
        return park.splitlines()


def check_host(host: str) -> bool:
    status = os.popen(f"ping -c 2 {host} ")
    if ("100.0% packet loss" or "unreachable") in status.read():
        return False
    else:
        return True


def save_to_file(output_filename: str, data: list):
    with open(output_filename, "w") as output:
        for row in data:
            output.write(row)
            output.write("\n")


def print_unreachables_to_table(data: list):
    table = Table(title="unreachable host")
    table.add_column("Hosts", justify="right", style="cyan")
    for row in data:
        table.add_row(row)
    console = Console()
    console.print(table)


def main(
    hosts_file: str = typer.Argument(..., help="File path to hosts to check"),
    save_results_to_file: bool = typer.Option(
        default=True, help="Save results to text file"
    ),
):
    unreachables_list = []
    unreachable_output_file = "unreachable_hosts.txt"
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=f"Collecting hosts from {hosts_file}", total=0)
        hosts = collect_hosts(filename=hosts_file)
        if not hosts:
            logger.error("No hosts was collected")
            raise typer.Exit(1)
        progress.log(f"Collected total {len(hosts)} hosts")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        unreachables: int = 0
        reachables: int = 0

        progress.add_task(description="Pings collected hosts", total=None)
        for ip in hosts:
            progress.log(f"Checking host {ip}")
            if check_host(host=ip):
                reachables += 1
            else:
                unreachables += 1
                unreachables_list.append(ip)
    if save_results_to_file:
        if len(unreachables_list):
            save_to_file(
                output_filename=unreachable_output_file, data=unreachables_list
            )
            logger.info(f"saved unreachables hosts to {unreachable_output_file}")
        else:
            logger.info("All hosts are up!")
    else:
        if len(unreachables_list):
            print_unreachables_to_table(data=unreachables_list)
        else:
            logger.info("All hosts are up!")


if __name__ == "__main__":
    typer.run(main)
