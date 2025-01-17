import sys
import typer

from pathlib import Path
from typing_extensions import Annotated

from slicer import audio_slicing
from transcript import transcribe_from_paths


__version__ = '0.0.1'

app = typer.Typer()

def version_callback(value: bool):
    if value:
        typer.echo(f"HistoryAIToolKit: {__version__}")
        raise typer.Exit()

@app.command("version")    
def main():
    """Checks the package version"""
    version_callback(sys.argv[1:])

@app.command()
def slice(
    source: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            help="Source audio file",
        ),
    ],
    start: Annotated[str, typer.Argument(help="start time in mins:secs")],
    duration: Annotated[str, typer.Argument(help="duration in mins:secs")],
):
    """Slices an audio file into smaller audio files."""
    audio_slicing(source, start, duration)


@app.command()
def transcribe(
    source: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            readable=True,
            resolve_path=True,
            help="Source audio file",
        ),
    ],
    target: Path,
):
    """Transcribes an audio file into text."""
    if source.suffix not in [".mp3", ".wav"]:
        raise ValueError("File must be an .mp3 or .wav file")
    transcribe_from_paths(source, target)


if __name__ == "__main__":
    app()
