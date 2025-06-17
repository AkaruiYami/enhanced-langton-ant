from core.world import World

# TODO: Automatically call the registry
import engine


def main():
    w = World()
    print(w.ants)
    print(w.tiles)


if __name__ == "__main__":
    main()
