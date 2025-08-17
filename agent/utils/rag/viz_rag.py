from langchain_core.runnables import Runnable, RunnablePassthrough

def save_chain_graph(
    chain: Runnable,
    file_path: str,
    method: str = "png"
) -> None:
    """
    將 LangChain Runnable graph 存成圖檔或文字檔。

    Args:
        chain (Runnable): 你的 Runnable chain
        file_path (str): 儲存檔案的路徑，例如 "rag_graph.png"
        method (str): "png", "ascii", or "mermaid"
    """
    try:
        graph = chain.get_graph()
        if method == "png":
            content = graph.draw_mermaid_png()
            with open(file_path, "wb") as f:
                f.write(content)
        elif method == "ascii":
            content = graph.draw_ascii()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        elif method == "mermaid":
            content = graph.draw_mermaid()
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            print(f"[Error] Unsupported method: {method}")
        print(f"[Saved] Graph saved to {file_path}")
    except Exception as e:
        print(f"[Error] Failed to save graph: {e}")


