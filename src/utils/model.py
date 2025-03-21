import os
import openai
import load_dotenv
from typing import List
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI

load_dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


class Intention(BaseModel):
    """Model for the category of the problem"""

    id: int = Field(..., title="Id", description="Id of the description")

    category: str = Field(..., title="Category", description="Category of the problem")
    subcategory: str = Field( ..., title="Subcategory", description="Subcategory of the problem")
    reason: str = Field(..., title="Reason", description="Reason of the problem")


class IntentionList(BaseModel):
    """Model for the category of the problem"""

    intentions: List[Intention]


class GPTIntentions:
    """Clase para obtener la causa raiz de un problema"""

    def __init__(
        self,
        pydantic_object: BaseModel,
        prompt: str,
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.3,
    ):
        self.model = ChatOpenAI(model_name=model_name, temperature=temperature)

        self.parser = PydanticOutputParser(pydantic_object=pydantic_object)

        self.prompt = PromptTemplate(
            template=prompt,
            input_variables=["descriptions"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.prompt_and_model = self.prompt | self.model.with_structured_output(
            schema=IntentionList
        )

    def get_intentions(self, text: str):
        output = self.prompt_and_model.invoke({"descriptions_with_subcategories": text})
        return output
