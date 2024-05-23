from mentorlib_sme import app, Base, db
from waitress import serve
import click

@click.command()
@click.option("--debug", is_flag=True, help="Enable debug mode.")

def main(debug):
    if(debug):
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        serve(app, host='0.0.0.0', port=5000, url_scheme='https', debug=debug)

if __name__ == "__main__":
    main()