{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "4a56e07b",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting langchain-google-genai\n",
      "  Downloading langchain_google_genai-4.2.4-py3-none-any.whl.metadata (2.7 kB)\n",
      "Requirement already satisfied: langgraph in /usr/local/python/3.12.1/lib/python3.12/site-packages (1.2.2)\n",
      "Requirement already satisfied: langchain-core in /usr/local/python/3.12.1/lib/python3.12/site-packages (1.4.0)\n",
      "Collecting filetype<2.0.0,>=1.2.0 (from langchain-google-genai)\n",
      "  Downloading filetype-1.2.0-py2.py3-none-any.whl.metadata (6.5 kB)\n",
      "Collecting google-genai<3.0.0,>=1.65.0 (from langchain-google-genai)\n",
      "  Downloading google_genai-2.7.0-py3-none-any.whl.metadata (52 kB)\n",
      "Requirement already satisfied: pydantic<3.0.0,>=2.0.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langchain-google-genai) (2.13.4)\n",
      "Requirement already satisfied: jsonpatch<2.0.0,>=1.33.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langchain-core) (1.33)\n",
      "Requirement already satisfied: langchain-protocol>=0.0.14 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langchain-core) (0.0.16)\n",
      "Requirement already satisfied: langsmith<1.0.0,>=0.3.45 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langchain-core) (0.8.7)\n",
      "Requirement already satisfied: packaging>=23.2.0 in /home/codespace/.local/lib/python3.12/site-packages (from langchain-core) (26.0)\n",
      "Requirement already satisfied: pyyaml<7.0.0,>=5.3.0 in /home/codespace/.local/lib/python3.12/site-packages (from langchain-core) (6.0.3)\n",
      "Requirement already satisfied: tenacity!=8.4.0,<10.0.0,>=8.1.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langchain-core) (9.1.4)\n",
      "Requirement already satisfied: typing-extensions<5.0.0,>=4.7.0 in /home/codespace/.local/lib/python3.12/site-packages (from langchain-core) (4.15.0)\n",
      "Requirement already satisfied: uuid-utils<1.0,>=0.12.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langchain-core) (0.16.0)\n",
      "Requirement already satisfied: anyio<5.0.0,>=4.8.0 in /home/codespace/.local/lib/python3.12/site-packages (from google-genai<3.0.0,>=1.65.0->langchain-google-genai) (4.12.1)\n",
      "Collecting google-auth<3.0.0,>=2.48.1 (from google-auth[requests]<3.0.0,>=2.48.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai)\n",
      "  Downloading google_auth-2.53.0-py3-none-any.whl.metadata (5.5 kB)\n",
      "Requirement already satisfied: httpx<1.0.0,>=0.28.1 in /home/codespace/.local/lib/python3.12/site-packages (from google-genai<3.0.0,>=1.65.0->langchain-google-genai) (0.28.1)\n",
      "Requirement already satisfied: requests<3.0.0,>=2.28.1 in /home/codespace/.local/lib/python3.12/site-packages (from google-genai<3.0.0,>=1.65.0->langchain-google-genai) (2.32.5)\n",
      "Requirement already satisfied: websockets<17.0,>=13.0.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from google-genai<3.0.0,>=1.65.0->langchain-google-genai) (16.0)\n",
      "Collecting distro<2,>=1.7.0 (from google-genai<3.0.0,>=1.65.0->langchain-google-genai)\n",
      "  Using cached distro-1.9.0-py3-none-any.whl.metadata (6.8 kB)\n",
      "Collecting sniffio (from google-genai<3.0.0,>=1.65.0->langchain-google-genai)\n",
      "  Using cached sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)\n",
      "Requirement already satisfied: idna>=2.8 in /home/codespace/.local/lib/python3.12/site-packages (from anyio<5.0.0,>=4.8.0->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (3.11)\n",
      "Collecting pyasn1-modules>=0.2.1 (from google-auth<3.0.0,>=2.48.1->google-auth[requests]<3.0.0,>=2.48.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai)\n",
      "  Downloading pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)\n",
      "Collecting cryptography>=38.0.3 (from google-auth<3.0.0,>=2.48.1->google-auth[requests]<3.0.0,>=2.48.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai)\n",
      "  Downloading cryptography-48.0.0-cp311-abi3-manylinux_2_34_x86_64.whl.metadata (4.3 kB)\n",
      "Requirement already satisfied: certifi in /home/codespace/.local/lib/python3.12/site-packages (from httpx<1.0.0,>=0.28.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (2026.2.25)\n",
      "Requirement already satisfied: httpcore==1.* in /home/codespace/.local/lib/python3.12/site-packages (from httpx<1.0.0,>=0.28.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (1.0.9)\n",
      "Requirement already satisfied: h11>=0.16 in /home/codespace/.local/lib/python3.12/site-packages (from httpcore==1.*->httpx<1.0.0,>=0.28.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (0.16.0)\n",
      "Requirement already satisfied: jsonpointer>=1.9 in /home/codespace/.local/lib/python3.12/site-packages (from jsonpatch<2.0.0,>=1.33.0->langchain-core) (3.0.0)\n",
      "Requirement already satisfied: orjson>=3.9.14 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langsmith<1.0.0,>=0.3.45->langchain-core) (3.11.9)\n",
      "Requirement already satisfied: requests-toolbelt>=1.0.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langsmith<1.0.0,>=0.3.45->langchain-core) (1.0.0)\n",
      "Requirement already satisfied: xxhash>=3.0.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langsmith<1.0.0,>=0.3.45->langchain-core) (3.7.0)\n",
      "Requirement already satisfied: zstandard>=0.23.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langsmith<1.0.0,>=0.3.45->langchain-core) (0.25.0)\n",
      "Requirement already satisfied: annotated-types>=0.6.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from pydantic<3.0.0,>=2.0.0->langchain-google-genai) (0.7.0)\n",
      "Requirement already satisfied: pydantic-core==2.46.4 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from pydantic<3.0.0,>=2.0.0->langchain-google-genai) (2.46.4)\n",
      "Requirement already satisfied: typing-inspection>=0.4.2 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from pydantic<3.0.0,>=2.0.0->langchain-google-genai) (0.4.2)\n",
      "Requirement already satisfied: charset_normalizer<4,>=2 in /home/codespace/.local/lib/python3.12/site-packages (from requests<3.0.0,>=2.28.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (3.4.5)\n",
      "Requirement already satisfied: urllib3<3,>=1.21.1 in /home/codespace/.local/lib/python3.12/site-packages (from requests<3.0.0,>=2.28.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (2.6.3)\n",
      "Requirement already satisfied: langgraph-checkpoint<5.0.0,>=4.1.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langgraph) (4.1.1)\n",
      "Requirement already satisfied: langgraph-prebuilt<1.2.0,>=1.1.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langgraph) (1.1.0)\n",
      "Requirement already satisfied: langgraph-sdk<0.4.0,>=0.3.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langgraph) (0.3.15)\n",
      "Requirement already satisfied: ormsgpack>=1.12.0 in /usr/local/python/3.12.1/lib/python3.12/site-packages (from langgraph-checkpoint<5.0.0,>=4.1.0->langgraph) (1.12.2)\n",
      "Requirement already satisfied: cffi>=2.0.0 in /home/codespace/.local/lib/python3.12/site-packages (from cryptography>=38.0.3->google-auth<3.0.0,>=2.48.1->google-auth[requests]<3.0.0,>=2.48.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (2.0.0)\n",
      "Requirement already satisfied: pycparser in /home/codespace/.local/lib/python3.12/site-packages (from cffi>=2.0.0->cryptography>=38.0.3->google-auth<3.0.0,>=2.48.1->google-auth[requests]<3.0.0,>=2.48.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai) (3.0)\n",
      "Collecting pyasn1<0.7.0,>=0.6.1 (from pyasn1-modules>=0.2.1->google-auth<3.0.0,>=2.48.1->google-auth[requests]<3.0.0,>=2.48.1->google-genai<3.0.0,>=1.65.0->langchain-google-genai)\n",
      "  Downloading pyasn1-0.6.3-py3-none-any.whl.metadata (8.4 kB)\n",
      "Downloading langchain_google_genai-4.2.4-py3-none-any.whl (68 kB)\n",
      "Downloading filetype-1.2.0-py2.py3-none-any.whl (19 kB)\n",
      "Downloading google_genai-2.7.0-py3-none-any.whl (822 kB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m822.5/822.5 kB\u001b[0m \u001b[31m11.0 MB/s\u001b[0m  \u001b[33m0:00:00\u001b[0m\n",
      "\u001b[?25hUsing cached distro-1.9.0-py3-none-any.whl (20 kB)\n",
      "Downloading google_auth-2.53.0-py3-none-any.whl (246 kB)\n",
      "Downloading cryptography-48.0.0-cp311-abi3-manylinux_2_34_x86_64.whl (4.7 MB)\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m4.7/4.7 MB\u001b[0m \u001b[31m24.1 MB/s\u001b[0m  \u001b[33m0:00:00\u001b[0m\n",
      "\u001b[?25hDownloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)\n",
      "Downloading pyasn1-0.6.3-py3-none-any.whl (83 kB)\n",
      "Using cached sniffio-1.3.1-py3-none-any.whl (10 kB)\n",
      "Installing collected packages: filetype, sniffio, pyasn1, distro, pyasn1-modules, cryptography, google-auth, google-genai, langchain-google-genai\n",
      "\u001b[2K   \u001b[90m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\u001b[0m \u001b[32m9/9\u001b[0m [langchain-google-genai]e-genai]s]\n",
      "\u001b[1A\u001b[2KSuccessfully installed cryptography-48.0.0 distro-1.9.0 filetype-1.2.0 google-auth-2.53.0 google-genai-2.7.0 langchain-google-genai-4.2.4 pyasn1-0.6.3 pyasn1-modules-0.4.2 sniffio-1.3.1\n",
      "\n",
      "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m A new release of pip is available: \u001b[0m\u001b[31;49m26.0.1\u001b[0m\u001b[39;49m -> \u001b[0m\u001b[32;49m26.1.1\u001b[0m\n",
      "\u001b[1m[\u001b[0m\u001b[34;49mnotice\u001b[0m\u001b[1;39;49m]\u001b[0m\u001b[39;49m To update, run: \u001b[0m\u001b[32;49mpip install --upgrade pip\u001b[0m\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    }
   ],
   "source": [
    "\n",
    "%pip install langchain-google-genai langgraph langchain-core"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "3baa9a71",
   "metadata": {},
   "outputs": [],
   "source": [
    "from typing import TypedDict , List\n",
    "from langgraph.graph import StateGraph , START , END\n",
    "from langchain_core.messages import HumanMessage\n",
    "from langchain_google_genai import ChatGoogleGenerativeAI\n",
    "from dotenv import load_dotenv\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "d0170837",
   "metadata": {},
   "outputs": [],
   "source": [
    "load_dotenv()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "2225f711",
   "metadata": {},
   "outputs": [],
   "source": [
    "class AgentState(TypedDict)\n",
    "    messages : list[HumanMessage]\n",
    "llm = ChatGoogleGenerativeAI( model = \"gemini-1.5-flash\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "363644ba",
   "metadata": {},
   "outputs": [],
   "source": [
    "def process(state : AgentState) -> AgentState:\n",
    "    response = llm.invoke(state['messages'])\n",
    "    print(f'/nAI: {response.content}')\n",
    "    return state\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "ba735222",
   "metadata": {},
   "outputs": [],
   "source": [
    "graph = StateGraph(AgentState)\n",
    "graph.add_node(\"process\", process)\n",
    "graph.add_edge(START, \"process\")\n",
    "graph.add_edge(\"process\", END)\n",
    "\n",
    "agent = graph.compile()\n",
    "\n",
    "user_input = input(\"Enter: \")\n",
    "while user_input != \"exit\":\n",
    "    agent.invoke({\"messages\": [HumanMessage(content=user_input)]})\n",
    "    user_input = input(\"Enter: \")\n",
    "\n",
    "                                          "
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
