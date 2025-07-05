from django.shortcuts import render
from .langchain_backend.agent import build_agent


agent = build_agent()

def index(request):
    response = ""
    if request.method == "POST":
        query = request.POST.get("query")
        if query:
            try:
                response = agent.run(query)
            except Exception as e:
                response = f"Error: {e}"

    return render(request, "index.html", {"response": response})