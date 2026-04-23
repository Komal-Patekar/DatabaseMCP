from db import load_procedure_metadata, execute_procedure_call
from intelligence_engine import build_procedure_metadata
from ratelimiter import check_rate_limit
from logger import logger


def register_database_tools(mcp):

    procedures = load_procedure_metadata()

    for proc_name, params in procedures.items():

        metadata = build_procedure_metadata(proc_name, params)

        description = f"""
Category: {metadata['category']}

Description:
{metadata['description']}
"""

        cleaned_params = metadata["parameters"]

        # build signature
        param_signature = ", ".join([f"{p}: str" for p in cleaned_params])

        args_list = ", ".join(cleaned_params)

        if param_signature:
            func_code = f"""
@mcp.tool(name="{proc_name}", description=\"\"\"{description}\"\"\")
def {proc_name}({param_signature}):
    check_rate_limit()
    logger.info("Calling procedure {proc_name}")
    return call_procedure("{proc_name}", [{args_list}])
"""
        else:
            func_code = f"""
@mcp.tool(name="{proc_name}", description=\"\"\"{description}\"\"\")
def {proc_name}():
    check_rate_limit()
    logger.info("Calling procedure {proc_name}")
    return call_procedure("{proc_name}", [])
"""

        exec(func_code, {
            "mcp": mcp,
            "call_procedure": call_procedure,
            "check_rate_limit": check_rate_limit,
            "logger": logger
        })

    logger.info(f"Registered {len(procedures)} procedure tools")