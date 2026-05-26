import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from cnc.server import CNCServer  # noqa: E402
from dust_trak.server import DustTrakServer  # noqa: E402
from wtvb01.server import WTVB01Server  # noqa: E402

SERVERS = {
    "dusttrak": DustTrakServer,
    "wtvb01": WTVB01Server,
    "cnc": CNCServer,
}


async def main(selected: list[str], use_virtual: bool):
    servers = {
        name: cls(use_virtual_device=use_virtual) 
        for name, cls in SERVERS.items() 
        if name in selected
    }

    if not servers:
        print(f"No matching servers found. Available: {list(SERVERS.keys())}")
        sys.exit(1)

    print(f"Starting servers: {list(servers.keys())} (Virtual Mode: {use_virtual})")

    try:
        await asyncio.gather(*[s.run() for s in servers.values()])
    except asyncio.CancelledError:
        pass
    finally:
        await asyncio.gather(*[s.stop() for s in servers.values() if hasattr(s, 'stop')])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run OPC-UA adapters")
    parser.add_argument(
        "servers",
        nargs="*",
        default=list(SERVERS.keys()),
        help=f"Servers to run. Available: {list(SERVERS.keys())}",
    )

    parser.add_argument(
        "--virtual",
        action="store_true",
        help="Use virtual devices instead of real hardware",
    )
    args = parser.parse_args()
    
    asyncio.run(main(args.servers, args.virtual))
