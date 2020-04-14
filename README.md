# RDHTMLResolve
A script that recursively embeds HTML parts in an HTML file.

The HTML content and JS are moved from HTML_SRC to the HTML folder. At this time, the HTML file's #include is recursively resolved.

```html
    <!--#include virtual="/modal.html" -->
```

## How it's run.

Enter the settings and run the script.
```python
# Setting
debuglog = True
distFolderName = "html/"
srcFolderName = "html_src/"
basePath = "./"

reg_pattern = r'<!--\s*#include\s*virtual="(.*?)"\s*-->'
reg_fileName_pattern = r'.*\.(html|css|md)'
reg_copy_fileName_pattern = r'.*\.(png)'
```