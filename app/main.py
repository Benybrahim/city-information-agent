"""Main entry point for the City Information Assistant API."""

import json
import logging
from uuid import uuid4

from agents import Runner, SQLiteSession
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.cores.agent import CityAssistantAgent
from app.schemas.schemas import ChatRequest, ChatResponse

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="City Information Assistant API")

# Initialize agent and session globally
session = SQLiteSession(session_id=str(uuid4()))
agent = CityAssistantAgent().get()


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch all unhandled exceptions and return as JSON."""
    logger.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)},
    )


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest) -> ChatResponse | None:
    """
    Handles incoming chat requests and returns structured agent responses.

    :param req: User chat request
    :return: Structured agent output
    """
    try:
        result = await Runner.run(agent, req.message, session=session)
        logger.info(f"Output: {result}")
        data = json.loads(result.final_output)
        return ChatResponse(**data)
    except Exception as exc:
        logger.exception(f"Error running agent: {exc}")
        raise HTTPException(status_code=500, detail="Assistant failed to process request.")
