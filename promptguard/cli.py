import typer

app = typer.Typer()


@app.command()
def test(spec: str = typer.Argument(..., help="Path to your YAML test spec")):
    """
    Run promptguard tests defined in a YAML spec.
    """
    typer.echo(f"Running tests on spec: {spec}")
    raise typer.Exit(code=0)


if __name__ == "__main__":
    app()
