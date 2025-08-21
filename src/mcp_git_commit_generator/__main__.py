from mcp_git_commit_generator.server import serve


def main() -> None:
    import asyncio

    asyncio.run(serve())

if __name__ == "__main__":
    main()
