# RDHTMLResolve
A script that recursively embeds HTML parts in an HTML file.

The HTML content and JS are moved from HTML_SRC to the HTML folder. At this time, the HTML file's #include is recursively resolved.

```html
    <!--#include virtual="/modal.html" -->
```

