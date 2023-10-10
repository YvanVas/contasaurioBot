def build_html(title: str, table: str) -> str:
    html_content = """<!DOCTYPE html>
    <html lang="en">

    <head>
        <meta content="text/html; charset=utf-8">
        <title>"""+title+"""</title>
        <style>
            /* Estilos para la tabla */
            table {
                width: 100%;
                border-collapse: collapse;
            }

            tr,
            th,
            td {
                padding: 8px;
                text-align: center;
                border-bottom: 1px solid #ddd;
            }

            th {
                background-color: #2b7e2c;
                color: white;
            }

            /* Estilos para hacerla responsiva */
            @media screen and (max-width: 600px) {
                table {
                    border: 0;
                }

                table caption {
                    font-size: 1.3em;
                }

                table thead {
                    display: none;
                }

                table tr {
                    margin-bottom: 20px;
                    display: block;
                    border-bottom: 2px solid #ddd;
                }

                table td {
                    display: block;
                    text-align: right;
                    font-size: 13px;
                    border-bottom: 1px dotted #ccc;
                }

                table td::before {
                    content: attr(data-label);
                    float: left;
                    text-transform: uppercase;
                    font-weight: bold;
                }
            }
        </style>
    </head>

    <body>
    <h2 style="text-align: center; margin-top: 2px; margin-bottom: 5px;">
    """+title+"""
    </h2>
    """+table+"""        
    </body>

    </html>"""

    html = html_content.replace('\n', '')

    return html
