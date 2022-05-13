# -*- coding: utf-8 -*-

#  Copyright (c) 2021, University of Luxembourg / DHARPA project
#
#  Mozilla Public License, version 2.0 (see LICENSE or https://www.mozilla.org/en-US/MPL/2.0/)
import os
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

import orjson
import rich_click as click

# from alembic import command  # type: ignore
# from alembic.config import Config  # type: ignore
from kiara.doc.mkdocs_macros_cli import KIARA_DOC_BUILD_CACHE_DIR
from kiara.interfaces import get_console

# noqa
# type: ignore
from kiara.utils.cli import terminal_print
from rich import box
from rich.console import Group
from rich.table import Table


@click.group("doc")
@click.pass_context
def doc_group(ctx):
    """Documentation helpers."""


@doc_group.command("serve")
@click.option(
    "--dirty-reload",
    "-d",
    help="Only re-build pages that have changed.",
    is_flag=True,
    default=False,
)
@click.option(
    "--fail-on-cmd-error",
    "-f",
    help="Fail if any of the commands in the generation process fail..",
    is_flag=True,
    default=False,
)
@click.pass_context
def serve(ctx, dirty_reload: bool, fail_on_cmd_error: bool):
    """ "Serve a 'live' version of the documentation page using the mkkdocs development server."""

    if fail_on_cmd_error:
        os.environ["FAIL_DOC_BUILD_ON_ERROR"] = "true"
    else:
        os.environ["FAIL_DOC_BUILD_ON_ERROR"] = "false"

    from mkdocs.commands import serve as mkdocs_serve

    config_file = Path.cwd() / "mkdocs.yml"
    watch_folder = Path.cwd() / "docs"

    live_reload = "livereload" if not dirty_reload else "dirty"

    other = {
        "strict": None,
        "theme": None,
        "use_directory_urls": None,
        "watch_theme": False,
    }

    mkdocs_serve.serve(
        config_file=config_file.as_posix(),
        dev_addr="127.0.0.1:8000",
        livereload=live_reload,
        watch=[watch_folder.as_posix()],
        **other,
    )


@doc_group.group("cache")
@click.pass_context
def cache(ctx):
    """Manage documentation cache."""


@cache.command("print")
@click.argument("cmd_id", nargs=1, required=False, type=click.INT)
@click.pass_context
def print_cache(ctx, cmd_id: int = None):
    """Print information about the documentation build cache."""

    infos = get_cmd_infos(folder=KIARA_DOC_BUILD_CACHE_DIR)

    if cmd_id is None:
        console = get_console()

        table = Table(box=box.SIMPLE)
        table.add_column("id", justify="center")
        table.add_column("command", no_wrap=True, max_width=console.size.width - 26)
        table.add_column("runs", no_wrap=True, justify="center")
        table.add_column("success", no_wrap=True, justify="center")

        for cmd_id, details in infos.items():

            all_success = (
                "[green]true[/green]" if details["all_success"] else "[red]false[/red]"
            )
            table.add_row(
                str(cmd_id),
                " ".join(details["cmd"]),
                str(details["no_runs"]),
                all_success,
            )

        terminal_print(table)
    else:
        if cmd_id not in infos.keys():
            terminal_print()
            terminal_print(
                f"Invalid id: '{cmd_id}', run this command without argument to list all valid cached commands/ids."
            )
            sys.exit(1)

        cmd_info = infos[cmd_id]
        cmd_str = " ".join(cmd_info["cmd"])
        terminal_print()
        terminal_print(f"Details for cached cmd: [b i]{cmd_str}[/b i]")
        terminal_print()
        all_outputs = []
        for idx, info in enumerate(cmd_info["infos"]):
            output_file_path = info["output_file"]
            output_file = Path(output_file_path)
            all_outputs.append(
                f"# run {idx} --------------------------------------------------------------------------------"
            )
            all_outputs.append(output_file.read_text())
            all_outputs.append("")

        group = Group(*all_outputs)
        terminal_print(group)


def get_cmd_infos(
    folder: Union[str, Path] = KIARA_DOC_BUILD_CACHE_DIR
) -> Dict[int, Any]:

    if isinstance(folder, str):
        folder = Path(folder)

    infos: Dict[Tuple, Any] = {}
    commands = folder.glob("*.command")
    for cmd_file in commands:
        info = orjson.loads(cmd_file.read_bytes())
        cmd = tuple(info["command"])
        infos.setdefault(cmd, []).append(info)

    result: List[Dict[str, Any]] = []
    for cmd in infos.keys():
        cmd_infos = infos[cmd]
        runs = len(cmd_infos)
        all_success = all(x["success"] for x in cmd_infos)
        result.append(
            {
                "cmd": cmd,
                "no_runs": runs,
                "all_success": all_success,
                "infos": sorted(cmd_infos, key=lambda d: d["started"]),
            }
        )

    sorted_result = sorted(result, key=lambda d: d["infos"][0]["started"])
    result_dict = {idx: d for idx, d in enumerate(sorted_result, start=1)}
    return result_dict


@cache.command()
@click.pass_context
def clear(ctx):
    """Clear the documentation build cache."""

    folder = KIARA_DOC_BUILD_CACHE_DIR
    shutil.rmtree(folder)

    terminal_print()
    terminal_print(f"Cache folder cleared: {folder}")
