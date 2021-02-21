import requests
from bs4 import BeautifulSoup
from CSVmodule import *
import click


@click.command()
@click.argument('filename')
def main(filename):
    print('Данные по \"' + filename + '\" загружены.\n')


if __name__ == "__main__":
    main()
