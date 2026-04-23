import logging

logging.basicConfig(
    filename="mcp_server_activity.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("mcp_server")
