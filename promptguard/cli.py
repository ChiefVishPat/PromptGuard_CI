import typer
app = typer.Typer()

@app.command()
def test():
    """Run promptguard tests."""
    typer.echo("Running tests…")
