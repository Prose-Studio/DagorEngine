"""make_serve_cpp.py <stringify.py> <ServeFiles.cpp> <file>...: the web view plugin table (webui::webview_files_http_plugins)
serving each file, which stringify.py embeds as a byte array <name>.inl next to ServeFiles.cpp"""
import os
import subprocess
import sys

stringify_py, out_cpp, src_files = sys.argv[1], sys.argv[2], sys.argv[3:]

function_template = """static void serve_file_{name}(webui::RequestInfo *params) {{
  static uint8_t inlinedData[] = {{
#include "{name}.inl"
  }};
  webui::html_response_raw(params->conn, "{mime}", (const char *)inlinedData, sizeof(inlinedData) - 1);
}}
"""

ext_to_mime_type = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.ico': 'image/x-icon',
}

root_dir = os.path.dirname(os.path.abspath(__file__))
dst_dir = os.path.abspath(os.path.dirname(out_cpp))


def inl_name(src):
  return os.path.basename(src).replace('.', '_').replace('-', '_')


with open(out_cpp, 'wt') as f:
  f.write('#include <webui/httpserver.h>\n#include <webui/helpers.h>\n\n')
  for src in src_files:
    name = inl_name(src)
    subprocess.check_call([sys.executable, stringify_py, '--array', os.path.join(root_dir, src),
                           os.path.join(dst_dir, name + '.inl')])
    f.write(function_template.format(name=name, mime=ext_to_mime_type.get(os.path.splitext(src)[1], 'text/plain')))
  f.write('webui::HttpPlugin webui::webview_files_http_plugins[] = {\n')
  for src in src_files:
    f.write('  {{ "{0}", NULL, NULL, serve_file_{1} }},\n'.format(src, inl_name(src)))
  f.write('  {NULL}\n};\n')
