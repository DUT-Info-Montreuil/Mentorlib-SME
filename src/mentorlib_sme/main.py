from mentorlib_sme import app
import click

@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode.")

def main(debug):
    app.run(debug=debug)

if __name__ == "__main__":
    main()