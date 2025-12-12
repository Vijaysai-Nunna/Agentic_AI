from fastapi import FastAPI
from app.api.chain import router


app = FastAPI(title = "Prompt Changing API",
              version = "1.0.0")
app.include_router(router,prefix = "/api" , tags = ["PromptChain"])