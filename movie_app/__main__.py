import argparse
import pwd

from aiohttp.web import run_app
from aiomisc import bind_socket
from aiomisc.log import LogFormat, basic_config
from configargparse import ArgumentParser
from dotenv import load_dotenv
from yarl import URL

from movie_app.api.app import create_app
from movie_app.utils.argparse import positive_int
from movie_app.utils.pg import DEFAULT_PG_URL

load_dotenv()

ENV_VAR_PREFIX = "MESSENGER_"


parser = ArgumentParser(
    auto_env_var_prefix=ENV_VAR_PREFIX,
    allow_abbrev=False,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)
parser.add_argument(
    "--user", required=False, type=pwd.getpwnam, help="Change process UID"
)

group = parser.add_argument_group("API Options")
group.add_argument(
    "--api-address",
    default="0.0.0.0",
    help="IPv4/IPv6 address API server would listen on",
)
group.add_argument(
    "--api-port",
    type=positive_int,
    default=8081,
    help="TCP port API server would listen on",
)

group = parser.add_argument_group("PostgreSQL options")
group.add_argument(
    "--pg-url",
    type=URL,
    default=URL(DEFAULT_PG_URL),
    help="URL to use to connect to the database",
)
group.add_argument(
    "--pg-pool-min-size", type=int, default=10, help="Minimum database connections"
)
group.add_argument(
    "--pg-pool-max-size", type=int, default=10, help="Maximum database connections"
)

group = parser.add_argument_group("Logging options")
group.add_argument(
    "--log-level",
    default="info",
    choices=("debug", "info", "warning", "error", "fatal"),
)
group.add_argument("--log-format", choices=LogFormat.choices(), default="color")


def main():
    args = parser.parse_args()
    # Конфигурируем логгер
    basic_config(args.log_level, args.log_format, buffered=True)
    sock = bind_socket(address=args.api_address, port=args.api_port, proto_name="http")
    app = create_app(args)
    run_app(app, sock=sock)


if __name__ == "__main__":
    main()
