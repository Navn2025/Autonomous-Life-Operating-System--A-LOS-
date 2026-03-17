from fastmcp import FastMCP
from pathlib import Path
import shutil

mcp = FastMCP("filesystem-server")

ROOT = Path("C:/Users/navne/Desktop").resolve()


# -----------------------------
# PATH RESOLUTION
# -----------------------------
def resolve_path(path: str) -> Path:
    path = path.replace("\\", "/").strip()

    if path.lower().startswith("desktop/"):
        path = path[8:]

    if path.lower() in ["", ".", "desktop"]:
        return ROOT

    p = (ROOT / path).resolve()

    if not str(p).startswith(str(ROOT)):
        raise ValueError("Access outside root not allowed")

    return p


# -----------------------------
# LIST FILES
# -----------------------------
@mcp.tool()
def list_files(path: str = "") -> list:
    """List files and folders in a directory"""

    try:
        p = resolve_path(path)

        if not p.exists():
            return [f"Path does not exist: {p}"]

        return [f.name for f in p.iterdir()]

    except Exception as e:
        return [f"Error: {str(e)}"]


# -----------------------------
# READ FILE
# -----------------------------
@mcp.tool()
def read_file(path: str) -> str:
    """Read contents of a file"""

    try:
        p = resolve_path(path)

        if not p.exists():
            return f"File not found: {p}"

        return p.read_text()

    except Exception as e:
        return f"Error reading file: {str(e)}"


# -----------------------------
# WRITE FILE
# -----------------------------
@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to a file (creates folders automatically)"""

    try:
        p = resolve_path(path)

        # create directories automatically
        p.parent.mkdir(parents=True, exist_ok=True)

        p.write_text(content)

        return f"File written successfully: {p}"

    except Exception as e:
        return f"Error writing file: {str(e)}"


# -----------------------------
# EDIT FILE
# -----------------------------
@mcp.tool()
def edit_file(path: str, new_content: str) -> str:
    """Replace contents of a file"""

    try:
        p = resolve_path(path)

        if not p.exists():
            return f"File not found: {p}"

        p.write_text(new_content)

        return f"File updated: {p}"

    except Exception as e:
        return f"Error editing file: {str(e)}"


# -----------------------------
# CREATE FOLDER
# -----------------------------
@mcp.tool()
def create_folder(path: str) -> str:
    """Create a new folder"""

    try:
        p = resolve_path(path)

        p.mkdir(parents=True, exist_ok=True)

        return f"Folder created: {p}"

    except Exception as e:
        return f"Error creating folder: {str(e)}"


# -----------------------------
# DELETE FILE / FOLDER
# -----------------------------
@mcp.tool()
def delete_path(path: str) -> str:
    """Delete a file or folder"""

    try:
        p = resolve_path(path)

        if not p.exists():
            return f"Path not found: {p}"

        if p.is_file():
            p.unlink()
        else:
            shutil.rmtree(p)

        return f"Deleted: {p}"

    except Exception as e:
        return f"Error deleting: {str(e)}"


# -----------------------------
# FILE INFO
# -----------------------------
@mcp.tool()
def file_info(path: str) -> dict:
    """Get file or folder information"""

    try:
        p = resolve_path(path)

        if not p.exists():
            return {"error": "Path not found"}

        return {
            "name": p.name,
            "path": str(p),
            "is_file": p.is_file(),
            "is_directory": p.is_dir(),
            "size_bytes": p.stat().st_size
        }

    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# RUN MCP SERVER
# -----------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")