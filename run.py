import sys
import ruamel.yaml as yaml
from union import Union


def main():
    """Launches the bot"""
    # Load the configuration
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream, yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
            return

    bot = Union(config=config)

    bot.run()


if __name__ == "__main__":
    main()
