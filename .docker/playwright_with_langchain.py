import asyncio
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from langchain_community.tools.playwright.utils import (
    create_async_playwright_browser,  # A synchronous browser is available, though it isn't compatible with jupyter.\n",      },
)
from langchain.agents import AgentType, initialize_agent
from langchain_openai import ChatOpenAI
import nest_asyncio

nest_asyncio.apply()

# await get_elements_tool.arun(
#     {"selector": ".container__headline", "attributes": ["innerText"]}
# )
# await navigate_tool.arun(
#     {"url": "https://web.archive.org/web/20230428131116/https://www.cnn.com/world"}
# )


async def main():
    async_browser = create_async_playwright_browser()
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=async_browser)
    tools = toolkit.get_tools()
    tools

    tools_by_name = {tool.name: tool for tool in tools}
    navigate_tool = tools_by_name["navigate_browser"]
    get_elements_tool = tools_by_name["get_elements"]


    llm = ChatOpenAI(temperature=0)  # or any other LLM, e.g., ChatOpenAI(), OpenAI()
    agent_chain = initialize_agent(
        tools,
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    result = await agent_chain.arun("What are the headers on langchain.com?")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())