import ruamel.yaml as yaml

from union import Union


def main():
    """
    Launches the bot
    """
    with open("config.yml", 'r') as stream:
        try:
            config = yaml.load(stream, yaml.Loader)
        except yaml.YAMLError as exc:
            print(exc)
            return

    bot = Union(config=config)

    try:
        bot.load_extension("union.core.core")
    except Exception as e:
        print(f"Failed to load core cog.\n{e.__class__.__name__}: {e}")
        return

    bot.run()


if __name__ == "__main__":
    main()
