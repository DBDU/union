from ruamel.yaml import load, YAMLError
try:
    from ruamel.yaml import CLoader as Loader
except ImportError:
    from ruamel.yaml import Loader

from union import Union


def main():
    """
    Launches the bot
    """
    with open("config.yml", 'r') as stream:
        try:
            config = load(stream, Loader)
        except YAMLError as exc:
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
