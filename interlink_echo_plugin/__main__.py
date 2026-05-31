import uvicorn


def main():
    uvicorn.run(
        "interlink_echo_plugin:app",
        host="0.0.0.0",
        port=4000,
    )


if __name__ == "__main__":
    main()
